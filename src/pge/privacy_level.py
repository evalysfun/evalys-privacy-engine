"""
Privacy Level Definitions

Defines the three privacy modes and their characteristics.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional


class PrivacyMode(str, Enum):
    """Privacy mode enumeration"""
    NORMAL = "normal"
    STEALTH = "stealth"
    MAX_GHOST = "max_ghost"


@dataclass
class PrivacyLevel:
    """
    Privacy level configuration
    
    Attributes:
        mode: Privacy mode (normal, stealth, max_ghost)
        burner_count: Number of burner wallets to use
        timing_jitter_ms: Random timing jitter in milliseconds
        order_slicing: Whether to slice orders
        fragmentation_level: Level of order fragmentation (1-10)
        use_mev_protection: Whether to use MEV protection
        rotation_frequency: How often to rotate wallets (in transactions)
    """
    mode: PrivacyMode
    burner_count: int
    timing_jitter_ms: int
    order_slicing: bool
    fragmentation_level: int
    use_mev_protection: bool
    rotation_frequency: int = 1
    
    def __post_init__(self):
        """Validate privacy level configuration"""
        if self.fragmentation_level < 1 or self.fragmentation_level > 10:
            raise ValueError("fragmentation_level must be between 1 and 10")
        
        if self.burner_count < 1:
            raise ValueError("burner_count must be at least 1")
        
        if self.timing_jitter_ms < 0:
            raise ValueError("timing_jitter_ms must be non-negative")


# Predefined privacy levels
NORMAL_PRIVACY = PrivacyLevel(
    mode=PrivacyMode.NORMAL,
    burner_count=1,
    timing_jitter_ms=100,
    order_slicing=False,
    fragmentation_level=1,
    use_mev_protection=False,
    rotation_frequency=5
)

STEALTH_PRIVACY = PrivacyLevel(
    mode=PrivacyMode.STEALTH,
    burner_count=3,
    timing_jitter_ms=500,
    order_slicing=True,
    fragmentation_level=3,
    use_mev_protection=True,
    rotation_frequency=2
)

MAX_GHOST_PRIVACY = PrivacyLevel(
    mode=PrivacyMode.MAX_GHOST,
    burner_count=5,
    timing_jitter_ms=2000,
    order_slicing=True,
    fragmentation_level=8,
    use_mev_protection=True,
    rotation_frequency=1
)


def get_privacy_level(mode: PrivacyMode) -> PrivacyLevel:
    """
    Get predefined privacy level for a mode
    
    Args:
        mode: Privacy mode
        
    Returns:
        PrivacyLevel configuration
    """
    levels = {
        PrivacyMode.NORMAL: NORMAL_PRIVACY,
        PrivacyMode.STEALTH: STEALTH_PRIVACY,
        PrivacyMode.MAX_GHOST: MAX_GHOST_PRIVACY,
    }
    return levels[mode]

