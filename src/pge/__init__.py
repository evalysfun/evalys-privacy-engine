"""
Evalys Privacy Gradient Engine

The Privacy Gradient Engine (PGE) is the core orchestrator for privacy modes
in the Evalys ecosystem. It manages three privacy levels:
- Normal: Basic unlinkability
- Stealth: Timing unpredictability
- Max Ghost: Full camouflage
"""

from .privacy_level import PrivacyLevel, PrivacyMode
from .mode_selector import ModeSelector
from .orchestrator import PrivacyGradientEngine

__all__ = [
    "PrivacyLevel",
    "PrivacyMode",
    "ModeSelector",
    "PrivacyGradientEngine",
]

__version__ = "0.1.0"

