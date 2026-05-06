"""
Permanent Magnet Synchronous Machine (PMSM) — dq-frame model.

Covers steady-state torque, power, back-EMF, and per-unit
dq-axis equations for surface-mount (SPM) and interior (IPM) variants.

References:
    Hanselman, D.C. (2003). Brushless Permanent Magnet Motor Design. 2nd ed.
    Mohan, N. (2011). Advanced Electric Drives. Wiley.
    Pyrhönen, J. et al. (2008). Design of Rotating Electrical Machines.
"""

import numpy as np

__all__ = ["back_emf", "torque", "dq_currents", "PMSMParams"]


class PMSMParams:
    """
    Container for PMSM parameters.

    Attributes:
        p:      Number of pole pairs
        Ld:     d-axis inductance (H)
        Lq:     q-axis inductance (H)
        psi_m:  Permanent magnet flux linkage (Wb)
        Rs:     Stator resistance per phase (Ω)
        J:      Rotor inertia (kg·m²)
    """

    def __init__(
        self,
        p: int,
        Ld: float,
        Lq: float,
        psi_m: float,
        Rs: float = 0.0,
        J: float = 0.0,
    ):
        self.p = p
        self.Ld = Ld
        self.Lq = Lq
        self.psi_m = psi_m
        self.Rs = Rs
        self.J = J

    @property
    def is_spm(self) -> bool:
        """True if surface-mount (Ld ≈ Lq, no reluctance torque)."""
        return np.isclose(self.Ld, self.Lq, rtol=0.05)


def back_emf(omega_e: float, psi_m: float) -> float:
    r"""
    Peak phase back-EMF for a PMSM.

    .. math::
        E = \omega_e \cdot \psi_m

    Args:
        omega_e: Electrical angular velocity (rad/s)
        psi_m:   PM flux linkage (Wb)

    Returns:
        Peak back-EMF (V)

    References:
        Hanselman (2003), eq. 7.3
    """
    return omega_e * psi_m


def torque(
    params: PMSMParams,
    id: float,
    iq: float,
) -> float:
    r"""
    Electromagnetic torque from dq-frame currents.

    .. math::
        T_e = \frac{3}{2} p \left[\psi_m i_q + (L_d - L_q) i_d i_q \right]

    First term: excitation (alignment) torque.
    Second term: reluctance torque (zero for SPM where Ld = Lq).

    Args:
        params: PMSMParams instance
        id:     d-axis current (A)
        iq:     q-axis current (A)

    Returns:
        Electromagnetic torque Te (N·m)

    References:
        Hanselman (2003), eq. 7.10; Mohan (2011), §5.4
    """
    T_excitation = params.psi_m * iq
    T_reluctance = (params.Ld - params.Lq) * id * iq
    return 1.5 * params.p * (T_excitation + T_reluctance)


def dq_currents(
    params: PMSMParams,
    omega_e: float,
    Vd: float,
    Vq: float,
) -> tuple[float, float]:
    r"""
    Steady-state dq currents from applied dq voltages.

    Solves the steady-state voltage equations:

    .. math::
        V_d = R_s i_d - \omega_e L_q i_q

    .. math::
        V_q = R_s i_q + \omega_e (L_d i_d + \psi_m)

    Args:
        params:  PMSMParams instance
        omega_e: Electrical angular velocity (rad/s)
        Vd:      d-axis voltage (V)
        Vq:      q-axis voltage (V)

    Returns:
        Tuple (id, iq) in amperes

    References:
        Pyrhönen et al. (2008), §7.3
    """
    Rs = params.Rs
    Ld = params.Ld
    Lq = params.Lq
    psi_m = params.psi_m
    we = omega_e

    # 2x2 linear system: [Rs, -we*Lq; we*Ld, Rs] · [id; iq] = [Vd; Vq - we*psi_m]
    A = np.array([[Rs, -we * Lq],
                  [we * Ld, Rs]])
    b = np.array([Vd, Vq - we * psi_m])
    id_, iq_ = np.linalg.solve(A, b)
    return float(id_), float(iq_)
