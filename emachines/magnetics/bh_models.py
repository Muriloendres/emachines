"""
BH curve models for soft magnetic materials.

Provides analytical fits to measured BH data and standard
approximation models used in motor design.

References:
    Jiles, D.C., Atherton, D.L. (1986). Theory of ferromagnetic hysteresis.
        Journal of Magnetism and Magnetic Materials, 61(1-2), 48-60.
    Frölhich, O. (1881). Investigations of dynamoelectric machines.
        Elektrotechnische Zeitschrift.
"""

import numpy as np
from scipy.optimize import curve_fit

__all__ = ["frolich", "fit_frolich", "linear_region"]


def frolich(H: np.ndarray, a: float, b: float) -> np.ndarray:
    r"""
    Fröhlich-Kennelly analytical BH approximation.

    .. math::
        B = \frac{H}{a + b \cdot |H|}

    Simple two-parameter model. Accurate for moderate flux densities.
    Breaks down near and above saturation.

    Args:
        H: Magnetic field intensity (A/m), array-like
        a: Model parameter (dimensionless)
        b: Model parameter (m/A)

    Returns:
        Flux density B (T)

    References:
        Fröhlich (1881); see also Hanselman (2003), §3.2
    """
    H = np.asarray(H, dtype=float)
    return H / (a + b * np.abs(H))


def fit_frolich(H: np.ndarray, B: np.ndarray) -> tuple[float, float]:
    """
    Fit Fröhlich model parameters (a, b) to measured BH data.

    Args:
        H: Measured field intensity values (A/m)
        B: Measured flux density values (T)

    Returns:
        Tuple (a, b) of fitted parameters
    """
    H = np.asarray(H, dtype=float)
    B = np.asarray(B, dtype=float)
    (a, b), _ = curve_fit(frolich, H, B, p0=[1.0, 1.0], maxfev=5000)
    return float(a), float(b)


def linear_region(H: np.ndarray, mu_r: float) -> np.ndarray:
    r"""
    Linear BH approximation: B = μ₀ · μr · H

    Valid for low flux densities well below saturation.

    Args:
        H:    Magnetic field intensity (A/m)
        mu_r: Relative permeability

    Returns:
        Flux density B (T)
    """
    MU_0 = 4 * np.pi * 1e-7
    return MU_0 * mu_r * np.asarray(H, dtype=float)
