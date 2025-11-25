"""
Tests for risk model behavior

Tests threshold behavior, monotonicity, and deterministic config.
"""

import pytest
from src.pge.mode_selector import ModeSelector
from src.pge.privacy_level import PrivacyMode, PrivacyLevel, get_privacy_level


def test_mode_thresholds():
    """Test that mode selection respects risk thresholds"""
    selector = ModeSelector()
    
    # Low risk should select Normal
    mode = selector.select_mode(risk_level=0.2)
    assert mode == PrivacyMode.NORMAL
    
    # Medium risk should select Stealth
    mode = selector.select_mode(risk_level=0.5)
    assert mode == PrivacyMode.STEALTH
    
    # High risk should select Max Ghost
    mode = selector.select_mode(risk_level=0.9)
    assert mode == PrivacyMode.MAX_GHOST
    
    # Boundary tests
    mode = selector.select_mode(risk_level=0.35)
    assert mode in [PrivacyMode.NORMAL, PrivacyMode.STEALTH]  # At boundary
    
    mode = selector.select_mode(risk_level=0.7)
    assert mode in [PrivacyMode.STEALTH, PrivacyMode.MAX_GHOST]  # At boundary


def test_config_values_stable():
    """Test that privacy config values are stable and deterministic"""
    from src.pge.orchestrator import PrivacyGradientEngine
    
    engine = PrivacyGradientEngine()
    
    # Normal mode config
    level = engine.select_mode(user_preference="normal")
    assert level.burner_count >= 1
    assert level.timing_jitter_ms >= 0
    assert level.fragmentation_level >= 1
    assert level.fragmentation_level <= 10
    
    # Stealth mode config
    level = engine.select_mode(user_preference="stealth")
    assert level.burner_count >= 2
    assert level.timing_jitter_ms > 0
    assert level.order_slicing is True
    assert level.use_mev_protection is True
    
    # Max Ghost mode config
    level = engine.select_mode(user_preference="max_ghost")
    assert level.burner_count >= 3
    assert level.timing_jitter_ms > 100  # Significant jitter
    assert level.order_slicing is True
    assert level.fragmentation_level >= 5  # Heavy fragmentation
    assert level.use_mev_protection is True


def test_monotonicity():
    """Test that increasing risk never decreases privacy mode"""
    selector = ModeSelector()
    
    # Test risk escalation
    modes = []
    for risk in [0.1, 0.3, 0.4, 0.6, 0.8, 0.9]:
        mode = selector.select_mode(risk_level=risk)
        modes.append(mode)
    
    # Convert to numeric for comparison
    mode_values = {
        PrivacyMode.NORMAL: 1,
        PrivacyMode.STEALTH: 2,
        PrivacyMode.MAX_GHOST: 3,
    }
    
    # Check monotonicity: mode should never decrease as risk increases
    for i in range(1, len(modes)):
        prev_mode_val = mode_values[modes[i-1]]
        curr_mode_val = mode_values[modes[i]]
        assert curr_mode_val >= prev_mode_val, \
            f"Privacy mode decreased from {modes[i-1]} to {modes[i]} as risk increased"


def test_deterministic_config():
    """Test that same inputs produce same config"""
    from src.pge.orchestrator import PrivacyGradientEngine
    
    engine1 = PrivacyGradientEngine()
    engine2 = PrivacyGradientEngine()
    
    # Same inputs
    level1 = engine1.select_mode(
        user_preference="stealth",
        risk_level=0.6,
        transaction_amount=20.0
    )
    
    level2 = engine2.select_mode(
        user_preference="stealth",
        risk_level=0.6,
        transaction_amount=20.0
    )
    
    # Should produce identical configs
    assert level1.mode == level2.mode
    assert level1.burner_count == level2.burner_count
    assert level1.timing_jitter_ms == level2.timing_jitter_ms
    assert level1.fragmentation_level == level2.fragmentation_level


def test_risk_override_safety():
    """Test that user preference doesn't override safety limits"""
    selector = ModeSelector()
    
    # User wants normal, but high risk should escalate
    mode = selector.select_mode(
        user_preference="normal",
        risk_level=0.8
    )
    # Should escalate to at least Stealth (safety override)
    assert mode in [PrivacyMode.STEALTH, PrivacyMode.MAX_GHOST]
    
    # User wants stealth, but very high risk should escalate
    mode = selector.select_mode(
        user_preference="stealth",
        risk_level=0.95
    )
    # Should escalate to Max Ghost
    assert mode == PrivacyMode.MAX_GHOST


def test_sniper_activity_escalation():
    """Test that high sniper activity escalates mode"""
    selector = ModeSelector()
    
    # Low sniper activity
    mode = selector.select_mode(curve_conditions={"sniper_activity": 0.2})
    assert mode == PrivacyMode.NORMAL
    
    # Medium sniper activity
    mode = selector.select_mode(curve_conditions={"sniper_activity": 0.5})
    assert mode == PrivacyMode.STEALTH
    
    # High sniper activity
    mode = selector.select_mode(curve_conditions={"sniper_activity": 0.8})
    assert mode == PrivacyMode.MAX_GHOST


def test_transaction_amount_escalation():
    """Test that large transactions escalate mode"""
    selector = ModeSelector()
    
    # Small transaction
    mode = selector.select_mode(transaction_amount=1.0)
    assert mode == PrivacyMode.NORMAL
    
    # Medium transaction
    mode = selector.select_mode(transaction_amount=15.0)
    assert mode == PrivacyMode.STEALTH
    
    # Large transaction
    mode = selector.select_mode(transaction_amount=60.0)
    assert mode == PrivacyMode.MAX_GHOST

