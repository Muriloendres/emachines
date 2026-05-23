# MEC User Guide — Building Your Own Magnetic Equivalent Circuit

This guide explains how to use the `emachines.mec` solver to model any magnetic device
or motor from scratch. No prior knowledge of the solver internals is needed — just a
sketch of your magnetic geometry and some basic reluctance formulas.

---

## 1. The Mental Model

A Magnetic Equivalent Circuit (MEC) is the magnetic dual of an electrical circuit.

| Electrical | Magnetic |
|---|---|
| Voltage source (V) | MMF source (A·turns) |
| Current (A) | Flux Φ (Wb) |
| Resistance (Ω) | Reluctance R (A·turns/Wb) |
| Conductance (S) | Permeance P = 1/R (Wb/A·turns) |
| KVL (Σ V = 0) | KVL (Σ MMF = 0 around a loop) |
| KCL (Σ I = 0) | KCL (Σ Φ = 0 at a node) |

**Kirchhoff's Voltage Law (KVL)** applied to a magnetic loop:

```
Σ (R_i · Φ_i) = Σ MMF_sources
```

Every coil winding carrying current `I` with `N` turns contributes an MMF source of
`F = N·I` [A·turns] into the loop it encircles.

---

## 2. The Four Building Blocks

The solver has four branch types. Every MEC is assembled from these.

### 2.1 Mesh Branch — `add_mesh_branch(branch, mesh, mmf)`

One per independent loop. Acts as the "loop variable" — its flux IS the loop flux Φₘ.
Optionally carries an MMF source (a coil winding).

```python
mec.add_mesh_branch(branch=1, mesh=1, mmf=N * I)
```

- `branch`: unique integer ID for this branch
- `mesh`: which loop this branch belongs to (1, 2, 3, …)
- `mmf`: MMF source in this loop [A·turns] — typically `N × current`

**Rule:** You need exactly one mesh branch per independent loop in your circuit.

---

### 2.2 Nonlinear Branch — `add_nonlinear_branch(branch, length, area, model, meshes, orientations)`

For ferromagnetic material (steel, ferrite). The solver uses Newton-Raphson to handle
the nonlinear B-H relationship.

```python
from emachines.mec import ShanesudhoffModel, SplinePermeabilityModel

mec.add_nonlinear_branch(
    branch=2,
    length=0.05,        # mean flux path length [m]
    area=4e-4,          # cross-sectional area [m²]
    model=ShanesudhoffModel.ferrite_3C90(),
    meshes=[1, 2],      # this branch is shared by loops 1 and 2
    orientations=[+1, -1],  # flux in loop 1 is +ve, in loop 2 is -ve
)
```

- `length`: mean flux path length through the material [m]
- `area`: cross-sectional area perpendicular to flux [m²]
- `model`: a `PermeabilityModel` — see Section 4
- `meshes`: list of loop IDs that flux passes through this branch
- `orientations`: `+1` or `-1` per mesh (sign convention — follows right-hand rule
  relative to your chosen loop direction)

---

### 2.3 Linear Branch — `add_linear_branch(branch, permeance, meshes, orientations)`

For air gaps or any region with constant permeability. You supply the permeance
directly instead of length/area/material.

```python
P_gap = mu0 * area / gap_length   # [Wb/A·turns]

mec.add_linear_branch(
    branch=5,
    permeance=P_gap,
    meshes=[1],
    orientations=[+1],
)
```

Use this for:
- Air gaps: `P = μ₀ · A / g`
- Fringing paths: more complex geometry formulas (see Section 5)
- Any region where μ is constant

---

### 2.4 Nodal Branch — `add_nodal_branch(branch, permeance, node_from, node_to, meshes, orientations)`

For T-junctions and pole-symmetry boundaries where flux splits between paths.
Introduces a node-potential (magnetic scalar potential) unknown.

```python
mec.add_nodal_branch(
    branch=10,
    permeance=P,
    node_from=1,
    node_to=0,   # 0 = reference (ground)
    meshes=[2],
    orientations=[+1],
)
```

Most simple models (series/parallel circuits) don't need nodal branches.
Use them when your circuit has T-junctions that the mesh loops alone cannot capture.

---

## 3. Step-by-Step Process

Follow these steps to build an MEC for any device:

```
Step 1 — Draw the flux path diagram
Step 2 — Choose independent loops
Step 3 — Assign branch IDs and types
Step 4 — Calculate reluctances / permeances
Step 5 — Wire it up in Python
Step 6 — Register windings for flux linkage
Step 7 — Solve and extract results
```

---

## 4. Permeability Models

Three models are available out of the box:

```python
from emachines.mec import LinearPermeabilityModel, SplinePermeabilityModel, ShanesudhoffModel

# Constant μ = μ₀ · μr  (steel in linear region, or air with μr=1)
model = LinearPermeabilityModel(mu_r=1000)

# From measured B-H data (e.g. M19 silicon steel)
# H_data [A/m], B_data [T], starting from (0, 0)
model = SplinePermeabilityModel(H_data=[0, 500, 1000, 5000, 10000],
                                B_data=[0, 0.5, 0.9,  1.5,  1.8])

# From a SteelGrade object in emachines.magnetics
from emachines.magnetics import SteelGrade
grade = SteelGrade.m19()
model = SplinePermeabilityModel.from_steel_grade(grade)

# Shane-Sudhoff analytical model (3C90 ferrite built in)
model = ShanesudhoffModel.ferrite_3C90()

# Custom Shane-Sudhoff parameters
model = ShanesudhoffModel(mu_r=5000, a=[...], b=[...], gamma=[...])
```

---

## 5. Reluctance / Permeance Formulas for Common Flux Tubes

These are the formulas you'll use to translate geometry into R or P values.

### Rectangular flux tube (uniform cross-section)
```
R = l / (μ₀ · μr · A)     [A·turns/Wb]
P = μ₀ · μr · A / l       [Wb/A·turns]

where:
  l  = mean flux path length [m]
  A  = cross-sectional area [m²]
  μr = relative permeability of the material
```

### Air gap (uniform)
```
P_gap = μ₀ · A / g

where:
  A = pole face area = width × stack_length  [m²]
  g = physical air gap length [m]
```

### Fringing around an air gap (empirical)
```
P_fringe ≈ μ₀ · l · (2/π) · ln(1 + π·w / (2g))

where:
  l = stack length [m]
  w = tooth/pole width [m]
  g = gap length [m]
```

### Stator tooth (rectangular)
```
R_tooth = d_tooth / (μ · w_tooth · l_stk)

where:
  d_tooth = tooth depth (≈ slot depth) [m]
  w_tooth = tooth width = slot_pitch - slot_width [m]
  l_stk   = axial stack length [m]
```

### Stator yoke segment (per slot pitch)
```
R_yoke = (π · r_yoke / N_slots) / (μ · h_yoke · l_stk)

where:
  r_yoke  = mean yoke radius [m]
  N_slots = total number of stator slots
  h_yoke  = yoke height [m]
```

### Slot leakage (flux crossing the slot opening)
```
P_slot_leak = μ₀ · l_stk · d_slot / w_slot
```

---

## 6. Worked Example — EI Core Inductor

This is the same circuit as `example1.m` in the MEC 3.2 toolbox, translated to Python.

```
      ___________________________
     |                           |
     |     Left  |  Centre  | Right
  Winding       Gap         
     |___________________________| 
```

**Geometry** (from Cale et al., IEEE Trans. Magnetics, 2006):

```python
import numpy as np
from emachines.mec import MEC, ShanesudhoffModel

mu0 = 4e-7 * np.pi

mm  = 1e-3
we  = 28.7 * mm   # outer leg width
wc  = 57.4 * mm   # centre leg width
ws  = 37.0 * mm   # window width
ds  = 48.8 * mm   # window height
wb  = 27.3 * mm   # bottom yoke width
wi  = 30.5 * mm   # top yoke (I-piece) width
g   = 2.96 * mm   # air gap (on centre leg)
d   = 119.8 * mm  # stack depth (into page)
N   = 40           # winding turns
I   = 50.0         # coil current [A]
```

**Step 1 — Draw the flux path:**

Two loops share the centre leg. Loop 1 is the left window, Loop 2 is the right window.

**Step 2 — Assign branches:**

| Branch | Type | Path |
|--------|------|------|
| 1 | Nonlinear (mesh) | Centre leg, upper half — carries MMF source; shared by loops 1 & 2 |
| 2 | Nonlinear | Left outer leg, upper half — loop 1 only |
| 3 | Nonlinear | Right outer leg, upper half — loop 2 only |
| 4 | Nonlinear | Centre leg, lower half — shared by loops 1 & 2 |
| 5 | Nonlinear | Left outer leg, lower half — loop 1 only |
| 6 | Nonlinear | Right outer leg, lower half — loop 2 only |
| 7 | Nonlinear | Left bottom yoke — loop 1 only |
| 8 | Nonlinear | Right bottom yoke — loop 2 only |
| 9 | Nonlinear | Left top yoke (I-piece) — loop 1 only |
| 10 | Nonlinear | Right top yoke (I-piece) — loop 2 only |
| 11 | Linear | Centre air gap — shared by loops 1 & 2 |
| 12 | Linear | Left outer air gap — loop 1 only |
| 13 | Linear | Right outer air gap — loop 2 only |

**Step 3 — Build the MEC:**

```python
mat = ShanesudhoffModel.ferrite_3C90()

mec = MEC()

# Branch 1: centre leg upper half — mesh branch with MMF source, shared by loops 1 & 2
# orientation: +1 for loop 1 (flux flows in same direction), -1 for loop 2 (opposite)
mec.add_nonlinear_branch(
    branch=1, length=(wb/2 + ds/2), area=wc*d, model=mat,
    mmf=N * I,              # MMF source lives here
    meshes=[1, 2], orientations=[+1, -1]
)
# One mesh branch per loop to declare the loop variables
mec.add_mesh_branch(branch=101, mesh=1, mmf=0.0)
mec.add_mesh_branch(branch=102, mesh=2, mmf=0.0)

# Remaining steel branches
mec.add_nonlinear_branch(branch=2,  length=(wb/2+ds/2), area=we*d, model=mat, meshes=[1],    orientations=[+1])
mec.add_nonlinear_branch(branch=3,  length=(wb/2+ds/2), area=we*d, model=mat, meshes=[2],    orientations=[+1])
mec.add_nonlinear_branch(branch=4,  length=ds/2,         area=wc*d, model=mat, meshes=[1, 2], orientations=[+1, -1])
mec.add_nonlinear_branch(branch=5,  length=ds/2,         area=we*d, model=mat, meshes=[1],    orientations=[+1])
mec.add_nonlinear_branch(branch=6,  length=ds/2,         area=we*d, model=mat, meshes=[2],    orientations=[+1])
mec.add_nonlinear_branch(branch=7,  length=(wc/2+ws+we/2), area=wb*d, model=mat, meshes=[1], orientations=[+1])
mec.add_nonlinear_branch(branch=8,  length=(wc/2+ws+we/2), area=wb*d, model=mat, meshes=[2], orientations=[+1])
mec.add_nonlinear_branch(branch=9,  length=(wc/2+ws+we/2), area=wi*d, model=mat, meshes=[1], orientations=[+1])
mec.add_nonlinear_branch(branch=10, length=(wc/2+ws+we/2), area=wi*d, model=mat, meshes=[2], orientations=[+1])

# Air gap branches (linear)
R_gap_c = g / (mu0 * wc * d)
R_gap_e = g / (mu0 * we * d)
mec.add_linear_branch(branch=11, permeance=1/R_gap_c, meshes=[1, 2], orientations=[+1, -1])
mec.add_linear_branch(branch=12, permeance=1/R_gap_e, meshes=[1],    orientations=[+1])
mec.add_linear_branch(branch=13, permeance=1/R_gap_e, meshes=[2],    orientations=[+1])

# Register winding for flux-linkage output
mec.add_winding('coil', {1: N})   # winding links branch 1 with N turns

# Solve
sol = mec.solve()
print(sol)
print(f"Flux linkage λ = {sol.flux_linkage('coil')*1000:.4f} mWb·turns")
print(f"Field energy  = {sol.field_energy*1000:.4f} mJ")
```

**Key outputs:**
```python
sol.flux('branch_id')           # flux through any branch [Wb]
sol.mmf('branch_id')            # MMF drop across any branch [A·turns]
sol.flux_linkage('coil')        # total flux linkage [Wb·turns]
sol.field_energy                # stored magnetic energy [J]
sol.converged                   # True if Newton-Raphson converged
sol.n_iterations                # number of NR iterations taken
```

---

## 7. Orientation Sign Convention

Getting orientations right is the most common source of errors. Follow this rule:

1. Pick a **positive flux direction** for each loop (e.g. clockwise).
2. For each branch shared by multiple loops, ask: "does this loop's flux flow
   through this branch in the same direction as my positive branch flux convention?"
   - Yes → `orientation = +1`
   - No  → `orientation = -1`

**Visual check:** if two loops share a branch and their fluxes flow in opposite
directions through it (which is the normal case for adjacent loops), their
orientations for that branch should have opposite signs.

```
  Loop 1 (CW)    Loop 2 (CW)
  ___________    ___________
 |           |  |           |
 |   →→→→   |  |   →→→→   |    ← shared branch (centre)
 |___________|  |___________|
 
In the shared centre branch:
  Loop 1 flux flows →  (say, +1)
  Loop 2 flux flows ←  (opposite, so -1)
  
orientations=[+1, -1] for the shared centre branch.
```

---

## 8. Extending to a Simple Motor Topology

For a simple radial-flux motor (e.g. SPM or induction motor), the topology follows
the same pattern — just more loops and more branches.

**Per-pole single-phase model (conceptual):**

```
Loops:
  - 1 stator loop per slot (one per tooth pair)
  - 1 rotor loop (for rotor flux path)
  - 1 airgap loop per stator-rotor alignment pair

Branches:
  - Stator tooth reluctance (nonlinear, steel)  — 1 per tooth
  - Stator yoke reluctance (nonlinear, steel)   — 1 per yoke segment
  - Air gap permeance (linear)                  — depends on rotor position
  - Rotor pole reluctance (nonlinear, steel)    — 1 per rotor pole section
  - Rotor yoke reluctance (nonlinear, steel)    — 1 per segment
```

**Airgap permeance for a single tooth-pole overlap:**
```python
def airgap_permeance(overlap_angle, r_stator, gap, stack_length):
    """
    Linear (straight-through) airgap permeance for a stator tooth
    overlapping a rotor section by angle `overlap_angle` [rad].
    """
    mu0 = 4e-7 * np.pi
    overlap_width = overlap_angle * r_stator  # arc length at stator bore
    return mu0 * overlap_width * stack_length / gap
```

**Position sweep pattern (from Horvath 2018):**
```python
# Pre-define all possible airgap branches at maximum overlap
for j in range(N_rotor_sections):
    mec.add_linear_branch(branch=1000+j, permeance=P_max, meshes=[...], orientations=[...])

# At each rotor position:
for theta in rotor_positions:
    for j in range(N_rotor_sections):
        P_new = airgap_permeance(overlap(theta, j), ...)
        mec.update_permeance(1000+j, P_new)   # approach 0 when not aligned
    
    sol = mec.solve()
    torque[theta] = compute_torque(sol, ...)
```

The key insight: **never restructure the circuit topology**. Pre-define all possible
connections at the start and drive non-overlapping airgap permeances to zero.

---

## 9. Computing Torque

Torque is computed from the rate of change of field energy (co-energy) with
mechanical position, at constant current:

```python
# Virtual work method — solve at two nearby positions
dtheta = 1e-5   # [rad]

mec.update_permeance(gap_branch, P(theta))
sol1 = mec.solve()

mec.update_permeance(gap_branch, P(theta + dtheta))
sol2 = mec.solve()

# co-energy ≈ field_energy for linear regions; use finite difference
dWf = sol2.field_energy - sol1.field_energy
torque = dWf / dtheta   # [N·m], at constant current
```

For accurate torque in nonlinear machines, use co-energy (integral of Φ dF) rather
than field energy. The solver returns `field_energy = ½ Σ R_eff · Φ²` which is
exact in the linear case.

---

## 10. Per-Unit Scaling (for motors with large airgaps)

When the airgap permeance is orders of magnitude different from the steel reluctance,
supply `phi_base` and `F_base` to keep the Newton-Raphson Jacobian well-conditioned:

```python
mu0   = 4e-7 * np.pi
B_base = 1.6          # T (near saturation knee)
A_base = gap_area     # largest airgap cross-section [m²]
g      = gap_length   # [m]

phi_base = B_base * A_base
P_base   = mu0 * A_base / g
F_base   = phi_base / P_base

mec = MEC(phi_base=phi_base, F_base=F_base)
```

Without this, the solver still works (heuristic scaling is applied automatically),
but convergence may be slower for highly saturated machines.

---

## 11. Quick Reference Checklist

Before calling `mec.solve()`, verify:

- [ ] **One mesh branch per independent loop** — exactly `N_loops` mesh branches
- [ ] **Every reluctance branch lists all loops it belongs to** — missing a mesh in
  `meshes=[...]` breaks KVL for that loop
- [ ] **Orientations are consistent** — adjacent loops sharing a branch get opposite signs
- [ ] **No floating permeances** — every linear branch has `permeance > 0` (even a tiny
  value; zero permeance = infinite reluctance, which is fine, but `None` will error)
- [ ] **MMF sources are in A·turns** — not just current; multiply by turn count
- [ ] **Areas and lengths are in SI** — metres and square metres, not mm

---

## 12. API Summary

```python
from emachines.mec import MEC, MECSolution
from emachines.mec import (LinearPermeabilityModel,
                            SplinePermeabilityModel,
                            ShanesudhoffModel)

# Build
mec = MEC(phi_base=None, F_base=None, rtol=1e-6, atol=1e-12, max_iter=200)

mec.add_mesh_branch(branch, mesh, mmf=0.0)
mec.add_nonlinear_branch(branch, length, area, model, mmf=0.0,
                         meshes=(), orientations=(), phi_source=0.0)
mec.add_linear_branch(branch, permeance, mmf=0.0,
                      meshes=(), orientations=(), phi_source=0.0)
mec.add_nodal_branch(branch, permeance, mmf=0.0,
                     node_from=0, node_to=0, meshes=(), orientations=())
mec.add_winding(winding_id, {branch_id: N_turns, ...})

# Update between solves (motion simulation)
mec.update_permeance(branch, new_permeance)
mec.update_mmf(branch, new_mmf)

# Solve
sol: MECSolution = mec.solve(phi0=None)

# Results
sol.flux(branch)              # [Wb]
sol.mmf(branch)               # [A·turns]
sol.flux_linkage(winding_id)  # [Wb·turns]
sol.field_energy              # [J]
sol.converged                 # bool
sol.n_iterations              # int
sol.residual                  # float
```
