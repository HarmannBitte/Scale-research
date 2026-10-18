# Open items: status after the final pass (2026-10-18)

Scope: every open item recorded in the session memory and the pass-5 series. No hardware, no maintainer contact, no purchases, no pushes without a token.

## Closed in this pass

| Item | Result | Evidence |
|---|---|---|
| MAX30009 DAC_OSR bit width | 2 bits, bits 7:6 | Datasheet summary text `BIOZ_DAC_OSR[7:6]`; driver mask GENMASK(7,6); vendor worked example (14,208 Hz) |
| MAX30009 ADC_OSR table (F05) | Field mapping confirmed (enum = register value) | Driver enum; datasheet SR examples |
| MAX30001 CNFG_BIOZ RATE | D[23] = 0 gives 64 sps (fMSTR 32,768 Hz) | MAX30001 datasheet page 57, Table 38 (alldatasheet mirror) |
| MAX30001 BioZ word layout (D[3]) | D[3] = 0; BTAG = D[2:0] | Datasheet page 67 (BIOZ FIFO data structure, Table 50) |
| MAX30001 ECG empty/overflow tags | Empty = 110, overflow = 111 (ETAG = D[5:3]) | Datasheet page 66 |
| OKOK test failure | Test bug (missing `height_cm` argument). Fix verified in scratch copy: 5 passed | `research-pass-6/okok-test-fix.patch`; applied to a scratch copy only |
| melazab/AD5940-BIOZ licence (F26), repo level | No top-level licence file | GitHub API: `license: null`; no LICENSE at root |
| OpenView `pubspec.lock` (F24) | Missing upstream too, so the collection did not drop it | GitHub tree of `Protocentral/protocentral_openview` (372 entries, not truncated): no `pubspec.lock` |
| Public upload verified at tip | Public `main` = `7b44432`; tree matches local `7b44432` exactly | Anonymous clone of `HarmannBitte/Scale-research`; tree hash `0606729…` on both sides |

## Partly closed

| Item | Status | What remains |
|---|---|---|
| F24 assets | Assets are in the upstream repo but were not collected | Re-collect `assets/` (fonts, logos). Not done. |
| MAX30001 official PDF | Text read from a third-party mirror; Analog Devices and Maxim PDF URLs failed in the fetch tool | Confirm the pages against the official PDF |
| Expanded candidate triage | Metadata triage for 18 repos (licence, last push, stars, archive status). Functional triage not done | Run tests for the candidates that matter. `robzarry/healthtrack` returned Not Found: the name or URL needs checking |

## Still open: needs your decision or a token

| Item | Blocker | What is needed |
|---|---|---|
| Push of 4 local commits to `Scale-research` (`2686199`, `e1b7c16`, `eabde99`, `df7d776`) | Needs a token in chat | A new token. Both tokens you pasted earlier are exposed and should be revoked |
| ADI-licensed AD5940 library in the public repo | Licence decision | 16 files under `ad5940lib/` carry an ADI licence limited to ADI products and forbidding combination with other code under different terms. The upload includes them. Options: keep as-is with a note, remove, or replace |
| F20 OpenView HR/RR contract | Maintainer contact not authorised | Authorisation to contact the maintainer |
| F22 FIFO semantics on silicon | Bench not authorised | Authorisation for a bench check |
| F34 AD5933 sign bug on silicon | Bench not authorised | Same |
| F35 I2C failure path on silicon | Bench not authorised | Same |
| F01 reachability, F08, F09 | Bench not authorised | Same |
| F31, F33 (BioZ FIFO overflow, empty-word handling) on silicon | Bench not authorised | Same |

## Not done in this pass

- Literature full-text verification (pass 6, item b). The 9 abstracts are verified; the full texts are not. Substantial work, and not started this pass.
- Write-up of this pass's literature corrections into the pass-6 notes (section 8). Pending. The notes file is not changed in this pass.

## Corrections to the session memory

- The public `main` is `7b44432`, not `79f2543`. `79f2543` is its parent. `7b44432` was pushed by the same upload tooling and matches the local tree.
- There are four unpushed local commits, not two: `2686199`, `e1b7c16`, `eabde99`, `df7d776`.
- The 256-word FIFO figure from earlier passes applies to the MAX30009. The MAX30001 BioZ FIFO holds 8 words.

## Files from this pass

- `research-pass-6/okok-test-fix.patch`: the verified test fix, for when a push is authorised.
- `deep-impedance-audit/pass5/`: all pass-5 work, including `DEEP-INVESTIGATION-PASS5E.md`, `findings-update-5e.json`, and the models and probes.
- `open-source-survey/` triage metadata is in `deep-impedance-audit/pass5/openitems/` (`meta_*.json`, `triage_meta.sh`).
