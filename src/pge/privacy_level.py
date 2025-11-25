"""
Privacy Level Definitions

Defines the three privacy modes and their characteristics.

This module provides:
- PrivacyMode enum: NORMAL, STEALTH, MAX_GHOST, CONFIDENTIAL
- PrivacyLevel dataclass: Configuration for each mode
- Predefined privacy levels with specific parameters

See docs/threat-model.md for threat coverage of each mode.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional


class PrivacyMode(str, Enum):
    """
    Privacy mode enumeration.
    
    Values:
        NORMAL: Basic unlinkability (1 burner, minimal jitter)
        STEALTH: Timing unpredictability (3 burners, moderate jitter)
        MAX_GHOST: Highest mitigation profile (5+ burners, high jitter)
        CONFIDENTIAL: Arcium-powered confidential computation mode
    """
    NORMAL = "normal"
    STEALTH = "stealth"
    MAX_GHOST = "max_ghost"
    CONFIDENTIAL = "confidential"  # Arcium-powered confidential mode


@dataclass
class PrivacyLevel:
    """
    Privacy level configuration.
    
    This dataclass defines all parameters for a privacy mode.
    Instances are validated in __post_init__.
    
    Attributes:
        mode: Privacy mode (normal, stealth, max_ghost, confidential)
        burner_count: Number of burner wallets to use (>= 1)
        timing_jitter_ms: Random timing jitter in milliseconds (>= 0)
        order_slicing: Whether to slice orders into fragments
        fragmentation_level: Level of order fragmentation (1-10)
        use_mev_protection: Whether to use MEV protection (Jito bundles, relays)
        rotation_frequency: How often to rotate wallets (in transactions)
        use_arcium: Whether to use Arcium confidential computation (for confidential mode)
        arcium_plan_id: Plan ID from Arcium MXE (if using confidential mode)
    
    Invariants (enforced in __post_init__):
        - fragmentation_level in [1, 10]
        - burner_count >= 1
        - timing_jitter_ms >= 0
    
    Side effects: None (immutable dataclass)
    
    Examples:
        >>> level = PrivacyLevel(
        ...     mode=PrivacyMode.STEALTH,
        ...     burner_count=3,
        ...     timing_jitter_ms=500,
        ...     order_slicing=True,
        ...     fragmentation_level=3,
        ...     use_mev_protection=True
        ... )
        >>> level.mode
        PrivacyMode.STEALTH
    """
    mode: PrivacyMode
    burner_count: int
    timing_jitter_ms: int
    order_slicing: bool
    fragmentation_level: int
    use_mev_protection: bool
    rotation_frequency: int = 1
    use_arcium: bool = False
    arcium_plan_id: Optional[str] = None
    
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


CONFIDENTIAL_PRIVACY = PrivacyLevel(
    mode=PrivacyMode.CONFIDENTIAL,
    burner_count=5,  # Will be adjusted by Arcium plan
    timing_jitter_ms=2000,  # Will be adjusted by Arcium plan
    order_slicing=True,
    fragmentation_level=8,  # Will be adjusted by Arcium plan
    use_mev_protection=True,
    rotation_frequency=1,
    use_arcium=True,
)


def get_privacy_level(mode: PrivacyMode) -> PrivacyLevel:
    """
    Get predefined privacy level for a mode.
    
    Returns a pre-configured PrivacyLevel instance for the given mode.
    These are the default configurations used by the orchestrator.
    
    Args:
        mode: Privacy mode (NORMAL, STEALTH, MAX_GHOST, or CONFIDENTIAL)
    
    Returns:
        PrivacyLevel configuration with predefined parameters
    
    Side effects: None (pure function)
    
    Raises:
        KeyError: If mode is not in the predefined levels
    
    Examples:
        >>> level = get_privacy_level(PrivacyMode.STEALTH)
        >>> level.burner_count
        3
        >>> level.timing_jitter_ms
        500
    """
    levels = {
        PrivacyMode.NORMAL: NORMAL_PRIVACY,
        PrivacyMode.STEALTH: STEALTH_PRIVACY,
        PrivacyMode.MAX_GHOST: MAX_GHOST_PRIVACY,
        PrivacyMode.CONFIDENTIAL: CONFIDENTIAL_PRIVACY,
    }
    return levels[mode]

