# emachines

**Analytical electromechanical machine design library.**

`emachines` is the core physics and mathematics engine behind [emdesignlabs.com](https://emdesignlabs.com). It provides well-documented, tested, and citable implementations of the analytical models used in electric motor design.

## Scope

- **Winding analysis** — winding factors (kp, kd, kw), MMF harmonic spectra, slot/pole geometry
- **Magnetics** — BH curve models (Fröhlich, Jiles-Atherton), iron loss (Steinmetz, Bertotti)
- **Motor models** — PMSM dq-frame, DC motor, surface-PM analytical design

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
from emachines.magnetics.iron_loss import bertotti
from emachines.motors.pmsm import PMSMParams, torque

# Winding factor for 12s/10p, fundamental harmonic
kw1 = winding_factor(nu=1, Q=12, p=5, coil_span=1)
print(f"kw1 = {kw1:.4f}")  # → 0.9330

# Bertotti iron loss at 400 Hz, 1.5 T
loss = bertotti(f=400, B_peak=1.5, k_h=0.02, k_e=1e-4, k_a=1e-3)
print(f"Total loss = {loss['total']:.2f} W/kg")

# PMSM torque from dq currents
motor = PMSMParams(p=3, Ld=5e-3, Lq=8e-3, psi_m=0.15)
Te = torque(motor, id=-3.0, iq=10.0)
print(f"Torque = {Te:.2f} N·m")
```

## Design Philosophy

- **Equations first** — every function documents the formula it implements with LaTeX notation
- **Cited** — every formula traces back to a specific reference (textbook, paper, standard)
- **Tested** — validated against published datasets and reference tools (emetor, SWAT-EM)
- **Dependency-light** — only numpy and scipy required

## Status

`0.1.x` — Alpha. API may change between minor versions.

## License

MIT
