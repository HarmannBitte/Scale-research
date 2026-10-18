"""Fitdays / Lefu 8-electrode scale: BLE protocol codec and body composition."""

from .protocol import (
    FITDAYS_DESCRIPTOR,
    SEGMENTS,
    FitdaysAdapter,
    ScaleProfile,
    build_c0,
    build_c1,
    checksum,
    make_frame,
    plan_writes,
    split_frame,
)
from .wla37 import compute_wla37, engine_status

__all__ = [
    "FITDAYS_DESCRIPTOR", "SEGMENTS", "FitdaysAdapter", "ScaleProfile", "build_c0", "build_c1",
    "checksum", "make_frame", "plan_writes", "split_frame", "compute_wla37", "engine_status",
]
