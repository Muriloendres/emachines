"""
Tests for winding factor calculations.

Reference values validated against emetor.com and SWAT-EM.
"""

import pytest
import numpy as np
from emachines.winding.factors import pitch_factor, distribution_factor, winding_factor


class TestPitchFactor:
    def test_full_pitch_fundamental(self):
        """Full-pitch coil: kp1 = 1.0"""
        assert np.isclose(pitch_factor(1, 3, 3.0), 1.0)

    def test_chorded_coil(self):
        """5/6 chording: kp1 = sin(5π/12) ≈ 0.9659"""
        assert np.isclose(pitch_factor(1, 5, 6.0), np.sin(5 * np.pi / 12), atol=1e-4)

    def test_third_harmonic_elimination(self):
        """2/3 chording eliminates 3rd harmonic: kp3 = 0"""
        assert np.isclose(pitch_factor(3, 4, 6.0), 0.0, atol=1e-10)


class TestDistributionFactor:
    def test_q1_concentrated(self):
        """q=1: kd1 = 1.0"""
        # Q=6, p=1, m=3 → q=1
        assert np.isclose(distribution_factor(1, 6, 1, m=3), 1.0)

    def test_q2_distributed(self):
        """q=2: kd1 ≈ 0.9659"""
        # Q=12, p=1, m=3 → q=2
        assert np.isclose(distribution_factor(1, 12, 1, m=3), 0.9659, atol=1e-3)

    def test_fscw_raises(self):
        """FSCW (q < 1) raises ValueError — star-of-slots not yet implemented."""
        # Q=12, p=5, m=3 → q=0.4
        with pytest.raises(ValueError, match="star-of-slots"):
            distribution_factor(1, 12, 5, m=3)


class TestWindingFactorIntegerSlot:
    @pytest.mark.parametrize("Q,p,coil_span,expected_kw1", [
        (24, 2, 5, 0.9330),   # 24s/4p, 5/6 chording: kp=0.9659, kd=0.9659
        (36, 3, 5, 0.9330),   # 36s/6p, 5/6 chording: same q=2, same result
        (12, 1, 6, 0.9659),   # 12s/2p, full pitch (coil_span=pole_pitch=6): kp=1.0, kd=0.9659
    ])
    def test_integer_slot_kw1(self, Q, p, coil_span, expected_kw1):
        kw = winding_factor(1, Q, p, coil_span)
        assert np.isclose(kw, expected_kw1, atol=0.001), \
            f"Q={Q}, p={p}, coil_span={coil_span}: kw1={kw:.4f}, expected≈{expected_kw1}"


class TestWindingFactorFSCW:
    @pytest.mark.xfail(
        reason="FSCW requires star-of-slots phasor method — "
               "to be migrated from emdesigner.winding_engine",
        raises=ValueError,
        strict=True,
    )
    @pytest.mark.parametrize("Q,P,expected_kw1", [
        (12, 10, 0.933),
        (12,  8, 0.866),
        ( 9,  8, 0.945),
        (12, 14, 0.933),
    ])
    def test_fscw_kw1(self, Q, P, expected_kw1):
        """FSCW winding factors — xfail until star-of-slots is ported."""
        p = P // 2
        pole_pitch = Q / P
        coil_span = max(1, round(pole_pitch))
        kw = winding_factor(1, Q, p, coil_span)
        assert np.isclose(kw, expected_kw1, atol=0.01)
