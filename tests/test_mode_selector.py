"""
Tests for mode selector
"""

import pytest
from src.pge.mode_selector import ModeSelector
from src.pge.privacy_level import PrivacyMode


def test_mode_selector_init():
    """Test mode selector initialization"""
    selector = ModeSelector()
    assert selector.default_mode == PrivacyMode.NORMAL


def test_select_mode_user_preference():
    """Test mode selection with user preference"""
    selector = ModeSelector()
    
    # User preference should be respected
    mode = selector.select_mode(user_preference="max_ghost")
    assert mode == PrivacyMode.MAX_GHOST
    
    mode = selector.select_mode(user_preference="stealth")
    assert mode == PrivacyMode.STEALTH
    
    mode = selector.select_mode(user_preference="normal")
    assert mode == PrivacyMode.NORMAL


def test_select_mode_risk_level():
    """Test mode selection based on risk level"""
    selector = ModeSelector()
    
    # High risk should select max_ghost
    mode = selector.select_mode(risk_level=0.9)
    assert mode == PrivacyMode.MAX_GHOST
    
    # Medium risk should select stealth
    mode = selector.select_mode(risk_level=0.6)
    assert mode == PrivacyMode.STEALTH
    
    # Low risk should select normal
    mode = selector.select_mode(risk_level=0.2)
    assert mode == PrivacyMode.NORMAL


def test_select_mode_transaction_amount():
    """Test mode selection based on transaction amount"""
    selector = ModeSelector()
    
    # Large transaction should select stealth
    mode = selector.select_mode(transaction_amount=15.0)
    assert mode == PrivacyMode.STEALTH
    
    # Very large transaction should select max_ghost
    mode = selector.select_mode(transaction_amount=60.0)
    assert mode == PrivacyMode.MAX_GHOST


def test_select_mode_curve_conditions():
    """Test mode selection based on curve conditions"""
    selector = ModeSelector()
    
    # High sniper activity should select max_ghost
    mode = selector.select_mode(curve_conditions={"sniper_activity": 0.8})
    assert mode == PrivacyMode.MAX_GHOST
    
    # Medium sniper activity should select stealth
    mode = selector.select_mode(curve_conditions={"sniper_activity": 0.5})
    assert mode == PrivacyMode.STEALTH


def test_select_mode_default():
    """Test default mode selection"""
    selector = ModeSelector()
    
    # No parameters should return default
    mode = selector.select_mode()
    assert mode == PrivacyMode.NORMAL


def test_adjust_mode_for_context():
    """Test dynamic mode adjustment"""
    selector = ModeSelector()
    
    # Normal mode with high risk should escalate
    adjusted = selector.adjust_mode_for_context(
        PrivacyMode.NORMAL,
        {"risk_level": 0.8, "sniper_activity": 0.7}
    )
    assert adjusted == PrivacyMode.STEALTH
    
    # Stealth mode with very high risk should escalate
    adjusted = selector.adjust_mode_for_context(
        PrivacyMode.STEALTH,
        {"risk_level": 0.95, "sniper_activity": 0.9}
    )
    assert adjusted == PrivacyMode.MAX_GHOST

