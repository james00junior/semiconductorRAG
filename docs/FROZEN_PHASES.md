# Frozen Phase Baselines

This file records immutable engineering baselines used for regression and auditability.

| Phase | Branch | Commit | Status |
|---|---|---|---|
| 0 | `phase-0-frozen` | `6ebab32819562fba28528748107cdff774f15fe6` | Frozen |
| 1 | `phase-1-frozen` | `ac7709fdf0d10df6961ce040115466379c0c2e64` | Frozen |
| 2 | `phase-2-frozen` | `272935bbb2cd7168c56869db5a8ddfff33882b75` | Frozen |

## Freeze policy

- Frozen branches are regression references and must not be rewritten.
- Production development continues from `main` through phase branches.
- Historical research notebooks remain preserved unless a later phase explicitly removes or archives them.
- A phase is complete only after implementation, tests, documentation and the corresponding merge commit are verified.
- CI must pass on every supported Python version before a phase is frozen.
