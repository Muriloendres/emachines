"""
Winding factor calculations.

Covers pitch factor (kp), distribution factor (kd), and combined
winding factor kw = kp · kd for the ν-th harmonic.

Current scope:
    - Integer-slot windings (q ≥ 1): full support
    - Fractional-slot concentrated windings (FSCW, q < 1):
      requires the star-of-slots method — to be migrated from emdesigner.
      Attempting to use distribution_factor() with q < 1 raises ValueError.

References:
    Hanselman, D.C. (2003). Brushless Permanent Magnet Motor Design. 2nd ed.
    Pyrhönen, J., Jokinen, T., Hrabovcová, V. (2008). Design of Rotating Electrical Machines.
"""

import numpy as np

__all__ = ["pitch_factor", "distribution_factor", "winding_factor"]


def pitch_factor(nu: int, coil_span: int, pole_pitch: float) -> float:
    r"""
    Pitch (chording) factor kp for the ν-th harmonic.

    .. math::
        k_{p\nu} = \sin\!\left(\nu \cdot \frac{\pi}{2} \cdot \frac{y}{\tau_p}\right)

    Args:
        nu:         Harmonic order ν (1 = fundamental)
        coil_span:  Coil span in slots (y)
        pole_pitch: Pole pitch in slots (τp = Q / P)

    Returns:
        Pitch factor kp ∈ [0, 1]

    References:
        Hanselman (2003), eq. 4.5
    """
    return float(np.abs(np.sin(nu * np.pi / 2 * coil_span / pole_pitch)))


def distribution_factor(nu: int, Q: int, p: int, m: int = 3) -> float:
    r"""
    Distribution (belt) factor kd for the ν-th harmonic.

    Valid for integer-slot windings only (q = Q/(2mp) ≥ 1).
    For FSCW (q < 1), use the star-of-slots phasor method instead
    (not yet implemented — tracked for migration from emdesigner).

    .. math::
        k_{d\nu} = \frac{\sin(\nu \cdot \pi / (2m))}{q \cdot \sin(\nu \cdot \pi / (2mq))}

    Args:
        nu: Harmonic order ν
        Q:  Total number of slots
        p:  Number of pole pairs
        m:  Number of phases (default 3)

    Returns:
        Distribution factor kd ∈ (0, 1]

    Raises:
        ValueError: If q < 1 (FSCW — use star-of-slots method instead)

    References:
        Pyrhönen et al. (2008), eq. 2.15
    """
    q = Q / (2 * m * p)
    if q < 1.0 - 1e-9:
        raise ValueError(
            f"distribution_factor() requires q ≥ 1 (integer-slot winding). "
            f"Got q = {q:.4f} (Q={Q}, p={p}, m={m}). "
            f"For FSCW use the star-of-slots method (coming soon in emachines.winding.sos)."
        )
    num = np.sin(nu * np.pi / (2 * m))
    den = q * np.sin(nu * np.pi / (2 * m * q))
    if np.abs(den) < 1e-12:
        return 1.0
    return float(np.abs(num / den))


def winding_factor(nu: int, Q: int, p: int, coil_span: int, m: int = 3) -> float:
    r"""
    Combined winding factor kw = kp · kd for the ν-th harmonic.

    Integer-slot windings only. For FSCW (Q/(2mp) < 1) this raises
    ValueError — the star-of-slots method is needed and will be
    provided in emachines.winding.sos once migrated from emdesigner.

    Args:
        nu:         Harmonic order ν (1 = fundamental)
        Q:          Total number of slots
        p:          Number of pole pairs
        coil_span:  Coil span in slots
        m:          Number of phases (default 3)

    Returns:
        Winding factor kw ∈ [0, 1]
    """
    pole_pitch = Q / (2 * p)
    kp = pitch_factor(nu, coil_span, pole_pitch)
    kd = distribution_factor(nu, Q, p, m)
    return kp * kd
