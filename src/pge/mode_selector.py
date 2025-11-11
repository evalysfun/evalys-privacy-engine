"""
Mode Selector

Selects the appropriate privacy mode based on user preference and risk assessment.
"""

from typing import Optional
from .privacy_level import PrivacyMode, PrivacyLevel, get_privacy_level


class ModeSelector:
    """
    Selects privacy mode based on various factors
    """
    
    def __init__(self):
        """Initialize mode selector"""
        self.default_mode = PrivacyMode.NORMAL
    
    def select_mode(
        self,
        user_preference: Optional[str] = None,
        risk_level: Optional[float] = None,
        transaction_amount: Optional[float] = None,
        curve_conditions: Optional[dict] = None
    ) -> PrivacyMode:
        """
        Select privacy mode based on multiple factors
        
        Args:
            user_preference: User's preferred mode ("normal", "stealth", "max_ghost")
            risk_level: Risk level (0.0 to 1.0, higher = more risk)
            transaction_amount: Transaction amount in SOL
            curve_conditions: Dictionary with curve conditions (sniper_activity, etc.)
        
        Returns:
            Selected PrivacyMode
        """
        # If user explicitly prefers a mode, use it (with risk override)
        if user_preference:
            try:
                preferred_mode = PrivacyMode(user_preference.lower())
                
                # Override to higher privacy if risk is high
                if risk_level and risk_level > 0.7:
                    if preferred_mode == PrivacyMode.NORMAL:
                        return PrivacyMode.STEALTH
                    elif preferred_mode == PrivacyMode.STEALTH:
                        return PrivacyMode.MAX_GHOST
                
                return preferred_mode
            except ValueError:
                # Invalid preference, fall through to auto-selection
                pass
        
        # Auto-select based on risk and conditions
        if risk_level is not None:
            if risk_level > 0.8:
                return PrivacyMode.MAX_GHOST
            elif risk_level > 0.5:
                return PrivacyMode.STEALTH
            elif risk_level > 0.3:
                return PrivacyMode.NORMAL
        
        # Check curve conditions
        if curve_conditions:
            sniper_activity = curve_conditions.get("sniper_activity", 0.0)
            if sniper_activity > 0.7:
                return PrivacyMode.MAX_GHOST
            elif sniper_activity > 0.4:
                return PrivacyMode.STEALTH
        
        # Check transaction amount
        if transaction_amount:
            if transaction_amount > 10.0:  # Large transaction
                return PrivacyMode.STEALTH
            elif transaction_amount > 50.0:  # Very large transaction
                return PrivacyMode.MAX_GHOST
        
        # Default to normal
        return self.default_mode
    
    def adjust_mode_for_context(
        self,
        current_mode: PrivacyMode,
        context: dict
    ) -> PrivacyMode:
        """
        Dynamically adjust mode based on execution context
        
        Args:
            current_mode: Current privacy mode
            context: Execution context (risk, conditions, etc.)
        
        Returns:
            Adjusted PrivacyMode
        """
        risk = context.get("risk_level", 0.0)
        sniper_activity = context.get("sniper_activity", 0.0)
        
        # Escalate if conditions worsen
        if current_mode == PrivacyMode.NORMAL:
            if risk > 0.7 or sniper_activity > 0.6:
                return PrivacyMode.STEALTH
        
        if current_mode == PrivacyMode.STEALTH:
            if risk > 0.9 or sniper_activity > 0.8:
                return PrivacyMode.MAX_GHOST
        
        return current_mode

