"""
Tests for privacy level definitions
"""

import pytest
from src.pge.privacy_level import (
    PrivacyMode,
    PrivacyLevel,
    get_privacy_level,
    NORMAL_PRIVACY,
    STEALTH_PRIVACY,
    MAX_GHOST_PRIVACY
)


def test_privacy_mode_enum():
    """Test PrivacyMode enum"""
    assert PrivacyMode.NORMAL == "normal"
    assert PrivacyMode.STEALTH == "stealth"
    assert PrivacyMode.MAX_GHOST == "max_ghost"


def test_privacy_level_creation():
    """Test creating privacy level"""
    level = PrivacyLevel(
        mode=PrivacyMode.NORMAL,
        burner_count=1,
        timing_jitter_ms=100,
        order_slicing=False,
        fragmentation_level=1,
        use_mev_protection=False
    )
    
    assert level.mode == PrivacyMode.NORMAL
    assert level.burner_count == 1
    assert level.timing_jitter_ms == 100


def test_privacy_level_validation():
    """Test privacy level validation"""
    # Invalid fragmentation level
    with pytest.raises(ValueError):
        PrivacyLevel(
            mode=PrivacyMode.NORMAL,
            burner_count=1,
            timing_jitter_ms=100,
            order_slicing=False,
            fragmentation_level=0,  # Invalid
            use_mev_protection=False
        )
    
    # Invalid burner count
    with pytest.raises(ValueError):
        PrivacyLevel(
            mode=PrivacyMode.NORMAL,
            burner_count=0,  # Invalid
            timing_jitter_ms=100,
            order_slicing=False,
            fragmentation_level=1,
            use_mev_protection=False
        )


def test_predefined_levels():
    """Test predefined privacy levels"""
    assert NORMAL_PRIVACY.mode == PrivacyMode.NORMAL
    assert STEALTH_PRIVACY.mode == PrivacyMode.STEALTH
    assert MAX_GHOST_PRIVACY.mode == PrivacyMode.MAX_GHOST
    
    # Check that stealth has more privacy than normal
    assert STEALTH_PRIVACY.burner_count > NORMAL_PRIVACY.burner_count
    assert STEALTH_PRIVACY.timing_jitter_ms > NORMAL_PRIVACY.timing_jitter_ms
    
    # Check that max_ghost has most privacy
    assert MAX_GHOST_PRIVACY.burner_count >= STEALTH_PRIVACY.burner_count
    assert MAX_GHOST_PRIVACY.timing_jitter_ms >= STEALTH_PRIVACY.timing_jitter_ms


def test_get_privacy_level():
    """Test get_privacy_level function"""
    normal = get_privacy_level(PrivacyMode.NORMAL)
    assert normal.mode == PrivacyMode.NORMAL
    
    stealth = get_privacy_level(PrivacyMode.STEALTH)
    assert stealth.mode == PrivacyMode.STEALTH
    
    max_ghost = get_privacy_level(PrivacyMode.MAX_GHOST)
    assert max_ghost.mode == PrivacyMode.MAX_GHOST

