"""
Tests for Privacy Gradient Engine orchestrator
"""

import pytest
from src.pge.orchestrator import PrivacyGradientEngine
from src.pge.privacy_level import PrivacyMode, PrivacyLevel


def test_engine_initialization():
    """Test engine initialization"""
    engine = PrivacyGradientEngine()
    assert engine.default_mode == PrivacyMode.NORMAL
    assert engine.current_mode is None
    assert engine.current_level is None


def test_engine_initialization_custom_mode():
    """Test engine initialization with custom mode"""
    engine = PrivacyGradientEngine(default_mode=PrivacyMode.STEALTH)
    assert engine.default_mode == PrivacyMode.STEALTH


def test_select_mode():
    """Test mode selection"""
    engine = PrivacyGradientEngine()
    
    level = engine.select_mode(user_preference="max_ghost")
    
    assert isinstance(level, PrivacyLevel)
    assert level.mode == PrivacyMode.MAX_GHOST
    assert engine.current_mode == PrivacyMode.MAX_GHOST
    assert engine.current_level == level


def test_get_current_level():
    """Test getting current level"""
    engine = PrivacyGradientEngine()
    
    # No level selected yet
    assert engine.get_current_level() is None
    
    # Select a mode
    engine.select_mode(user_preference="stealth")
    
    # Should have current level
    level = engine.get_current_level()
    assert level is not None
    assert level.mode == PrivacyMode.STEALTH


def test_adjust_privacy_level():
    """Test privacy level adjustment"""
    engine = PrivacyGradientEngine()
    
    # Select initial mode
    engine.select_mode(user_preference="normal")
    assert engine.current_mode == PrivacyMode.NORMAL
    
    # Adjust with high risk
    adjusted = engine.adjust_privacy_level({
        "risk_level": 0.9,
        "sniper_activity": 0.8
    })
    
    # Should escalate to higher privacy
    assert adjusted.mode in [PrivacyMode.STEALTH, PrivacyMode.MAX_GHOST]


def test_get_privacy_config():
    """Test getting privacy configuration"""
    engine = PrivacyGradientEngine()
    
    # No config yet
    config = engine.get_privacy_config()
    assert config == {}
    
    # Select mode
    engine.select_mode(user_preference="max_ghost")
    
    # Should have config
    config = engine.get_privacy_config()
    assert config["mode"] == "max_ghost"
    assert "burner_count" in config
    assert "timing_jitter_ms" in config
    assert "order_slicing" in config


def test_reset():
    """Test engine reset"""
    engine = PrivacyGradientEngine()
    
    # Select a mode
    engine.select_mode(user_preference="stealth")
    assert engine.current_mode is not None
    
    # Reset
    engine.reset()
    
    assert engine.current_mode is None
    assert engine.current_level is None

