"""Complete weigh-in from a computer: live weight, impedance sweep, composition.

    pip install -e ".[ble,engine]"
    python examples/scan_bleak.py --height 175 --age 40 --sex female --name Ann

Stand on the scale barefoot BEFORE it connects and keep still until it finishes.
Close the Fitdays app first — the scale accepts one connection at a time.
"""

from __future__ import annotations

import argparse
import asyncio
import json

from bleak import BleakClient, BleakScanner

from fitdays_scale import FITDAYS_DESCRIPTOR as D
from fitdays_scale import FitdaysAdapter, ScaleProfile, compute_wla37, engine_status


async def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--height", type=int, required=True, help="cm")
    ap.add_argument("--age", type=int, required=True)
    ap.add_argument("--sex", choices=["male", "female"], required=True)
    ap.add_argument("--name", default="", help="up to 3 letters, shown on the scale")
    ap.add_argument("--timeout", type=float, default=90)
    args = ap.parse_args()

    profile = ScaleProfile(height_cm=args.height, sex=args.sex, name=args.name)
    adapter, frames, state = FitdaysAdapter(), [], {}

    print("Scanning — step on the scale to wake it…")
    device = await BleakScanner.find_device_by_filter(
        lambda d, ad: (d.name or "").startswith(tuple(D.name_prefixes)), timeout=30)
    if device is None:
        raise SystemExit("Scale not found. Step on it to wake it, and close the Fitdays app.")

    async with BleakClient(device) as client:
        await client.start_notify(D.indicate_uuid, lambda _c, b: frames.append(bytes(b)))
        await client.start_notify(D.notify_uuid, lambda _c, b: frames.append(bytes(b)))
        print(f"Connected to {device.name}. Keep still…")

        loop = asyncio.get_running_loop()
        deadline = loop.time() + args.timeout
        while loop.time() < deadline:
            for frame in adapter.plan_writes(frames, state, profile):
                await client.write_gatt_char(D.write_uuid, frame, response=True)
                await asyncio.sleep(0.15)
            reading = adapter.decode(frames)
            if reading and reading.stable:
                break
            if reading:
                print(f"  {reading.weight_kg:.2f} kg", end="\r")
            await asyncio.sleep(0.3)
        else:
            raise SystemExit("Timed out without a settled result.")

        for frame in adapter.plan_writes(frames, state, profile):  # acknowledge the result
            await client.write_gatt_char(D.write_uuid, frame, response=True)
            await asyncio.sleep(0.15)

    print(f"\nWeight: {reading.weight_kg:.2f} kg")
    raw = reading.extras.get("impedance_raw")
    if not raw:
        print("No impedance (no electrode contact) — stand barefoot with dry feet.")
        return
    print("Impedance (ohm, f1/f2):", json.dumps(reading.extras["impedance_segments_ohm"]))
    result = compute_wla37(reading.weight_kg, args.height, args.age, args.sex, raw)
    if result is None:
        print("Body composition skipped:", engine_status()["error"])
    else:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
