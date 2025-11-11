"""
Configuration settings
"""

import os
from typing import Optional
from ..pge.privacy_level import PrivacyMode


class Settings:
    """Application settings"""
    
    # Default privacy mode
    DEFAULT_PRIVACY_MODE: PrivacyMode = PrivacyMode.NORMAL
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # API settings (if running as API)
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    API_DEBUG: bool = os.getenv("API_DEBUG", "false").lower() == "true"
    
    @classmethod
    def get_default_mode(cls) -> PrivacyMode:
        """Get default privacy mode from env or default"""
        mode_str = os.getenv("DEFAULT_PRIVACY_MODE", cls.DEFAULT_PRIVACY_MODE.value)
        try:
            return PrivacyMode(mode_str.lower())
        except ValueError:
            return cls.DEFAULT_PRIVACY_MODE

