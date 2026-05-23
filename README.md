# emachines

**Analytical electromechanical machine design library.**

`emachines` is the core physics and mathematics engine behind [emdesignlabs.com](https://emdesignlabs.com). It provides well-documented, tested, and citable implementations of the analytical models used in electric motor design.

## Scope

- **Winding analysis** — winding factors (kp, kd, kw), star-of-slots phasor method, slot/pole geometry, coil matrix
- **Magnetics** — BH curve models (Fröhlich), iron loss (Steinmetz, Modified Steinmetz, Bertotti), electrical steel database
- **Motor models** — PMSM dq-frame, surface-PM analytical design

Every function documents the equation it implements and its bibliographic source.

## Installation

```bash
pip install emachines
```

For development (editable install alongside emdesignlabs):

```bash
pip install -e path/to/emachines
```

## Quick Start

```python
from emachines.winding.factors import winding_factor
from emachines.winding.sos import (
    get_basic_params, build_coil_matrix, winding_factor_sos,
    check_symmetry, get_valid_coil_spans
)
from emachines.magnetics.iron_loss import bertotti, fit_loss_model
from emachines.magnetics.electrical_steel import SteelDatabase, SAMPLE_LOSS
from emachines.motors.pmsm import PMSMParams, torque

# ── Winding factors ───────────────────────────────────────────────────────────

# Integer-slot: 24s/4p, 5/6 chording (closed-form kp × kd)
kw1 = winding_factor(nu=1, Q=24, p=2, coil_span=5)
print(f"kw1 (24s/4p chorded) = {kw1:.4f}")   # → 0.9330

# FSCW: 12s/10p, tooth-coil (star-of-slots phasor, auto-dispatched)
kw1 = winding_factor(nu=1, Q=12, p=5, coil_span=1)
print(f"kw1 (12s/10p FSCW)   = {kw1:.4f}")   # → 0.9330

# FSCW: 9s/8p
kw1 = winding_factor(nu=1, Q=9, p=4, coil_span=1)
print(f"kw1 (9s/8p FSCW)     = {kw1:.4f}")   # → 0.9452

# Winding geometry: classify a slot/pole combination
params = get_basic_params(Q=12, P=10)
print(params['winding_type'])    # → 'concentrated'
print(params['q'])               # → Fraction(2, 5)
print(check_symmetry(12, 10))   # → True

# Slot-conductor occupancy matrix (2 layers, tooth-coil span)
matrix = build_coil_matrix(Q=12, P=10, m=3, layers=2, w=1)
# matrix[layer, slot] = ±phase_index (1-indexed), shape (2, 12)

# Full harmonic spectrum via phasor method
from emachines.winding.sos import winding_factor_sos
for nu in [1, 3, 5, 7]:
    kw = winding_factor_sos(nu, Q=12, P=10, layers=2, w=1)
    print(f"  kw(ν={nu}) = {kw:.4f}")

# ── Iron loss ─────────────────────────────────────────────────────────────────

# Bertotti forward model at 400 Hz, 1.5 T
loss = bertotti(f=400, B_peak=1.5, k_h=0.02, k_e=1e-4, k_a=1e-3)
print(f"Total loss = {loss['total']:.2f} W/kg")
print(f"  Hysteresis: {loss['hysteresis']:.2f}  Eddy: {loss['eddy']:.2f}  Anomalous: {loss['anomalous']:.2f}")

# Fit Bertotti coefficients from measured data
import numpy as np
f_arr    = np.array([50, 100, 200, 400])
B_arr    = np.array([1.0, 1.0, 1.0, 1.0])
loss_arr = np.array([1.2, 2.8, 6.5, 15.1])
result = fit_loss_model(f_arr, B_arr, loss_arr, model="Bertotti")
print(f"k_h={result['k_h']:.4f}, k_e={result['k_e']:.2e}, R²={result['r2']:.4f}")

# ── Electrical steel database ─────────────────────────────────────────────────

# Load from manufacturer datasheets (data_dir is your local folder)
db = SteelDatabase("path/to/datasheets")
grade = db.load("M270-50A")
print(grade.loss_at(freq=200, B=1.5))   # W/kg interpolated from datasheet

# Built-in reference data — no files required
print(SAMPLE_LOSS["M-19"])   # DataFrame: loss vs frequency and flux density

# ── PMSM motor model ──────────────────────────────────────────────────────────

motor = PMSMParams(p=3, Ld=5e-3, Lq=8e-3, psi_m=0.15, Rs=0.1)
Te = torque(motor, id=-3.0, iq=10.0)
print(f"Torque = {Te:.2f} N·m")
```

## Modules

### `emachines.winding`

| Module | Contents |
|---|---|
| `winding.factors` | `pitch_factor`, `distribution_factor`, `winding_factor` — integer-slot (closed-form) and FSCW (auto-dispatch to sos) |
| `winding.sos` | `build_star_of_slots`, `build_coil_matrix`, `assign_phases`, `winding_factor_sos` — star-of-slots phasor method for all winding types; `get_basic_params`, `check_symmetry`, `get_valid_coil_spans`, `is_valid_combination` |

**Winding factor dispatch in `winding_factor()`:**
- q ≥ 1 (integer-slot) → closed-form kp × kd
- q < 1 (FSCW) → star-of-slots phasor sum, double-layer convention (matches emetor.com)

### `emachines.magnetics`

| Module | Contents |
|---|---|
| `magnetics.bh_models` | Fröhlich analytical BH model and curve fitting |
| `magnetics.iron_loss` | `steinmetz`, `modified_steinmetz`, `bertotti` forward models; `fit_steinmetz`, `fit_modified_steinmetz`, `fit_bertotti`, `fit_loss_model` dispatcher |
| `magnetics.electrical_steel` | `SteelGrade` dataclass, `SteelDatabase` (Voestalpine Excel + ThyssenKrupp/SURA pickle loaders, LRU-cached), `SAMPLE_BH` and `SAMPLE_LOSS` reference data |

### `emachines.motors`

| Module | Contents |
|---|---|
| `motors.pmsm` | `PMSMParams`, `back_emf`, `torque` (excitation + reluctance), `dq_currents` |

## Design Philosophy

- **Equations first** — every function documents the formula it implements with LaTeX notation
- **Cited** — every formula traces back to a specific reference (textbook, paper, standard)
- **Tested** — validated against published datasets and reference tools (emetor, SWAT-EM)
- **Dependency-light** — only numpy, scipy, and pandas required

## Test Coverage

| Release | Tests | Status |
|---|---|---|
| 0.3.0 | 92 | ✅ All passing |
| 0.2.0 | 36 | ✅ All passing |
| 0.1.0 | 18 | ✅ All passing |

## Changelog

### [0.3.0] — 2026-05-09
- `winding.sos`: complete star-of-slots module — `build_star_of_slots`, `build_coil_matrix`,
  `assign_phases`, `winding_factor_sos`, `get_basic_params`, `check_symmetry`,
  `get_valid_coil_spans`, `is_valid_combination`
- `winding.factors`: `winding_factor()` now dispatches to star-of-slots for FSCW (q < 1)
- `winding/__init__.py`: all sos symbols exported at package level
- 92 passing tests, 0 xfailed — FSCW winding factors fully supported
- Validated against emetor.com: 12s/10p → 0.933, 9s/8p → 0.945, 12s/8p → 0.866

### [0.2.0] — 2026-05-08
- `magnetics.electrical_steel`: `SteelGrade`, `SteelDatabase`, `SAMPLE_BH`, `SAMPLE_LOSS`
- `magnetics.iron_loss`: `fit_bertotti`, `fit_steinmetz`, `fit_modified_steinmetz`, `fit_loss_model`
- `pandas>=1.5` added as runtime dependency

### [0.1.0] — 2026-05-07
- `winding.factors`: `pitch_factor`, `distribution_factor`, `winding_factor` (integer-slot)
- `magnetics.bh_models`: Fröhlich BH model and fitting
- `magnetics.iron_loss`: `steinmetz`, `modified_steinmetz`, `bertotti`
- `motors.pmsm`: `PMSMParams`, `back_emf`, `torque`, `dq_currents`

## Status

`0.3.x` — Alpha. API may change between minor versions.

## License

MIT

## Publishing to PyPI

Use Docker so twine and build tools are always available regardless of the local Python environment:

```bash
cd /Users/nd/Documents/NewLight/emachines

docker run --rm -v "$(pwd):/src" -w /src python:3.12-slim bash -c "
  pip install twine build --quiet &&
  python -m build &&
  TWINE_USERNAME=__token__ TWINE_PASSWORD=pypi-<your-token> twine upload dist/emachines-<version>*
"
```

> **Note:** Pass credentials inside the `bash -c` string (not via Docker `-e` flags) — this avoids interactive token prompts.

Replace `<your-token>` with your PyPI API token and `<version>` with the version in `pyproject.toml` (e.g. `0.4.0`).

Steps before running:
1. Bump `version` in `pyproject.toml`
2. Add a release entry to `CHANGELOG.md`
3. Commit and push to git
4. Run the Docker command above
