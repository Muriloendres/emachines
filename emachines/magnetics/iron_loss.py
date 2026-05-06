"""
Iron (core) loss models.

Covers the classical Steinmetz equation, the improved generalized
Steinmetz equation (iGSE), and Bertotti's three-term separation model.

References:
    Steinmetz, C.P. (1892). On the law of hysteresis.
        AIEE Transactions, 9, 3-64.
    Bertotti, G. (1988). General properties of power losses in soft
        ferromagnetic materials. IEEE Trans. Magnetics, 24(1), 621-630.
    Venkatachalam, K. et al. (2002). Accurate prediction of ferrite core
        loss with nonsinusoidal waveforms. COMPEL, 21(4).
"""

import numpy as np

__all__ = ["steinmetz", "bertotti"]


def steinmetz(
    f: float,
    B_peak: float,
    k_h: float,
    alpha: float,
    beta: float,
) -> float:
    r"""
    Classical Steinmetz core loss model (per unit mass).

    .. math::
        P_{core} = k_h \cdot f^{\alpha} \cdot \hat{B}^{\beta}

    Valid for sinusoidal excitation. Parameters k_h, α, β are
    material-specific and typically obtained by curve fitting to
    manufacturer loss data.

    Args:
        f:      Electrical frequency (Hz)
        B_peak: Peak flux density (T)
        k_h:    Hysteresis loss coefficient
        alpha:  Frequency exponent (typically 1.0–1.6)
        beta:   Flux density exponent (typically 1.6–2.2)

    Returns:
        Core loss power density (W/kg)

    References:
        Steinmetz (1892); Bertotti (1988)
    """
    return k_h * (f ** alpha) * (B_peak ** beta)


def bertotti(
    f: float,
    B_peak: float,
    k_h: float,
    k_e: float,
    k_a: float,
    alpha: float = 1.0,
    beta: float = 2.0,
) -> dict[str, float]:
    r"""
    Bertotti three-term iron loss separation model (per unit mass).

    Separates total loss into hysteresis, classical eddy current,
    and excess (anomalous) loss components:

    .. math::
        P_{total} = \underbrace{k_h f \hat{B}^{\beta}}_{hysteresis}
                  + \underbrace{k_e f^2 \hat{B}^2}_{eddy}
                  + \underbrace{k_a f^{1.5} \hat{B}^{1.5}}_{excess}

    Args:
        f:      Electrical frequency (Hz)
        B_peak: Peak flux density (T)
        k_h:    Hysteresis loss coefficient (W·s/kg)
        k_e:    Eddy current loss coefficient (W·s²/kg)
        k_a:    Excess loss coefficient (W·s^1.5/kg)
        alpha:  Frequency exponent for hysteresis (default 1.0)
        beta:   Flux density exponent for hysteresis (default 2.0)

    Returns:
        Dict with keys: 'hysteresis', 'eddy', 'excess', 'total' (W/kg)

    References:
        Bertotti (1988), eq. 6
    """
    p_hyst = k_h * (f ** alpha) * (B_peak ** beta)
    p_eddy = k_e * (f ** 2) * (B_peak ** 2)
    p_exc  = k_a * (f ** 1.5) * (B_peak ** 1.5)
    return {
        "hysteresis": p_hyst,
        "eddy":       p_eddy,
        "excess":     p_exc,
        "total":      p_hyst + p_eddy + p_exc,
    }
