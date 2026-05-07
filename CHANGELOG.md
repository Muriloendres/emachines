# Changelog

All notable changes to `emachines` will be documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/).

## [Unreleased]
- FSCW winding factors via star-of-slots phasor method (migration from emdesigner)
- `emachines.winding.sos`: star-of-slots module
- `emachines.winding.mmf`: MMF harmonic spectrum
- PyPI registration

## [0.1.0] — 2026-05-07
### Added
- `emachines.winding.factors`: pitch factor (kp), distribution factor (kd), winding factor (kw)
  - Integer-slot windings (q ≥ 1) fully supported
  - FSCW (q < 1) raises ValueError with clear message — star-of-slots pending
- `emachines.magnetics.bh_models`: Fröhlich analytical BH model and curve fitting
- `emachines.magnetics.iron_loss`: Steinmetz and Bertotti three-term separation models
- `emachines.motors.pmsm`: PMSMParams dataclass, back-EMF, torque (excitation + reluctance), steady-state dq current solver
- 18 passing tests, 4 xfailed (FSCW — by design, pending star-of-slots migration)
- `pyproject.toml`: hatchling build, PyPI metadata, Python ≥ 3.9
- `settings.ini`: nbdev-ready configuration
- MIT License

### Fixed
- Corrected GitHub username in project URLs (`vnaveendeepak` → `NaveenDeepak`)
- Lowered minimum Python from 3.10 to 3.9 to match emdesigner Docker environment
