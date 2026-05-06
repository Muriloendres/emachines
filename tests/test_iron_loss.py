"""Tests for iron loss models."""

import numpy as np
from emachines.magnetics.iron_loss import steinmetz, bertotti


def test_steinmetz_scales_with_frequency():
    """Loss increases with frequency."""
    p1 = steinmetz(50, 1.0, k_h=0.01, alpha=1.5, beta=2.0)
    p2 = steinmetz(100, 1.0, k_h=0.01, alpha=1.5, beta=2.0)
    assert p2 > p1


def test_steinmetz_scales_with_flux():
    """Loss increases with flux density."""
    p1 = steinmetz(50, 1.0, k_h=0.01, alpha=1.5, beta=2.0)
    p2 = steinmetz(50, 1.5, k_h=0.01, alpha=1.5, beta=2.0)
    assert p2 > p1


def test_bertotti_total_equals_sum_of_components():
    """Total loss = hysteresis + eddy + excess."""
    result = bertotti(50, 1.5, k_h=0.02, k_e=1e-4, k_a=1e-3)
    expected = result["hysteresis"] + result["eddy"] + result["excess"]
    assert np.isclose(result["total"], expected)


def test_bertotti_all_components_positive():
    result = bertotti(400, 1.0, k_h=0.01, k_e=5e-5, k_a=5e-4)
    assert result["hysteresis"] > 0
    assert result["eddy"] > 0
    assert result["excess"] > 0
