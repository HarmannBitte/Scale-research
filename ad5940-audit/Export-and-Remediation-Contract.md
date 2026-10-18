# Proposed bench-logger remediation and export contract

**Design proposal only. No firmware patch, vendor-file parser or hardware qualification is supplied.** Intended for development targeting the ADI AFE; review all licenses before implementation/distribution.

## 1. Data path

```text
AFE interrupt/status snapshot
  -> bounded FIFO read into original-word buffer
  -> complete-frame assembly with provenance
  -> signed 18-bit decode in separate storage
  -> checked calibration + complex arithmetic
  -> measurement/invalid event enqueue
  -> framed local transport
  -> immutable host archive and derived tables
```

Do not call the stock in-place processor and then attempt to reconstruct the original FIFO payload from its output. For calibration, capture the original calibration-channel DFT measurements at the library boundary as well as the derived RTIA values; the normal application measurement frame is not a fresh RCAL measurement.

## 2. Fix-first work packages

### P0-A: memory/count/error discipline

- Set output count to zero before every possible early return.
- Check all initialization/start/ISR/calibration results at their call sites.
- Enforce caller capacity before any FIFO transfer. Respect four-word frames; handle partial frames explicitly.
- Choose bounded drains/chunking or explicit acquisition stop-and-invalidate behavior. Test sustained backlog, full FIFO, capacity 0, capacity below one frame, and count above capacity.
- Preserve the fact and extent of known loss. An overflow means no silent continuation with supposedly contiguous valid samples.
- Do not clear a diagnostic flag before preserving it in a fault/event record.

### P0-B: calibration and numerical validity

- Calibration success requires a successful return, finite positive magnitude, finite phase, applicable settings/reference and valid provenance.
- A failed recalibration must not leave a previously valid-looking coefficient silently usable for the new configuration.
- Reject zero or near-noise-floor current magnitude before division; define the threshold from noise/range characterization, not an arbitrary count copied from another gain/frequency.
- Require finite derived values and check physically intended range separately. Do not interpret zero current as infinite body impedance or a physiological score.
- Keep source phase and explicitly wrapped canonical phase; signed capacitive X should be negative in the canonical engineering convention.
- Tie calibration identity to routing, actual frequency settings, gain/filter/ADC/DFT/window/drive state and applicable temperature/time conditions.

### P0-C: configuration validation and timeouts

- Validate frequency interval/count, table capacity and supported clock/ADC/drive combinations before generating sequences or touching calibration arrays.
- Export requested and effective ODR. Remove hidden hardcoded timing assumptions when changing clocks.
- Bound SPI/UART/DFT/sequencer waits, add a fault state and explicit recovery/reset/session transition.
- Treat a frequency/path change as a transition with settling data invalid until evidence supports a stable measurement window.

### P1: framed raw export

- Separate acquisition from UART formatting with a bounded queue and high-water/loss counters. Avoid lengthy blocking printf in the acquisition service path.
- Choose documented binary framing or a bounded structured text protocol with record type, payload length and checksum/CRC. Escape/framing rules must handle resets and debug text; never mix unframed debug lines into a measurement payload.
- Define payload limits and bandwidth at 230400 baud (8N1 theoretical maximum about 23,040 bytes/s before additional protocol/host overhead). Measure sustained throughput; do not infer it from this calculation.
- Attach frequency/configuration/calibration identity to each record, even when batching. Define exactly which acquisition pair each timestamp and status snapshot describes.
- Validate with dropped, duplicated, truncated, reordered, corrupted and restart-interrupted captures. A CRC does not establish analog correctness or detect every upstream acquisition loss.

## 3. Required record types

### Session record

`schema_version`, `record_type=session`, unique run/session ID, firmware commit/build identity, board/AFE revision/serial identifiers where available, host parser version, intended passive fixture purpose, UTC/session mapping, monotonic timer description and rollover rules, source kind (`hardware` or `synthetic`), and hash-linked configuration/calibration records.

### Configuration record

Complete relevant register snapshot and application settings; routing/path; requested frequency; frequency word; silicon mode; clock source and assumed/measured clock separately; **derived frequency estimate** and independently measured frequency as different fields; requested/effective ODR; ADC/filter/DFT/window settings; stimulus amplitude/gains and units; power/temperature state.

Do not label the nominal configured frequency or clock-derived estimate as an independently measured value.

### Calibration record

Calibration ID and applicable configuration hash; reference-plane/path description; measured RCAL value and uncertainty/certificate linkage; raw calibration DFT words and signed values; RTIA magnitude/phase with units; return codes; timing; operator/setup; validity limits and failure reason. Archive each attempted calibration, including failure, not just the most recent successful coefficients.

### Measurement record

- Session/sequence/frame ID; device monotonic acquisition timing or documented estimate and uncertainty; host receive timestamp separately.
- Fixture/path/configuration/calibration IDs and frequency identity.
- Original four FIFO words, plus decoded signed current-related and load-voltage DFT real/imaginary values.
- Explicit channel units: **DFT counts**, not amperes or volts merely because the channels are named current/voltage.
- Calibrated R/X in ohms, magnitude in ohms, phase in radians/degrees with clear field names and convention.
- Raw interrupt/status snapshots and decoded diagnostics, their observation scope/timing, FIFO count, transport/queue counters and transition/settling state.
- Numerical validity and a separate qualification-eligibility decision, with machine-readable reasons.

### Fault / end-of-run record

Failed operation/status, configuration/frequency, outstanding FIFO/queue state, known lost records, unknown loss extent, last sequence ID, recovery/session transition and final totals. Counter mismatches must be reported rather than silently repaired.

## 4. Unknown is not clear

Use tri-state diagnostics such as `true`, `false`, and `null/unknown`, plus a coverage declaration. Missing ADC threshold configuration is not a false clipping flag. Unknown contact/compliance status must remain unknown until a validated diagnostic supports it.

A record may be numerically finite yet ineligible for the bench acceptance checker because required quality evidence is missing. Do not fill its mandatory zero/one flags with fabricated zeroes just to satisfy the CSV schema.

## 5. Release criteria for the patched logger

1. Rebuild exact embedded target under recorded tools/packs/licenses; archive binary and configuration hashes.
2. Re-run corrected regression tests expecting faults to be caught, not merely reproducing stock failures.
3. Validate parser/framing on real raw captures, preserving source bytes and metadata.
4. Compare on-device derived results against independent host arithmetic using identical raw frames and calibration.
5. Complete passive-load calibration, held-out fixture, drift, settling, cable/contact, fault and data-integrity tests from the bench plan.
6. Independently review uncertainty and all unsupported diagnostic conditions.

These gates qualify only the stated passive bench measurements. They provide no authorization for human connection or clinical claims.
