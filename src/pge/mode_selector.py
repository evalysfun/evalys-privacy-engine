"""
Mode Selector

Selects the appropriate privacy mode based on user preference and risk assessment.

This module implements rule-based mode selection using risk thresholds:
- Normal: risk < 0.35
- Stealth: 0.35 <= risk < 0.7
- Max Ghost: risk >= 0.7

See docs/risk-model.md for detailed risk scoring formula.
"""

from typing import Optional
from .privacy_level import PrivacyMode, PrivacyLevel, get_privacy_level


class ModeSelector:
    """
    Selects privacy mode based on various factors.
    
    This is a pure function class - no side effects, deterministic output.
    
    Attributes:
        default_mode: Default privacy mode (PrivacyMode.NORMAL)
    
    Invariants:
        - Always returns a valid PrivacyMode
        - Increasing risk_level never decreases privacy mode (monotonicity)
        - User preference can override, but safety limits apply
    """
    
    def __init__(self):
        """
        Initialize mode selector.
        
        Side effects: None
        """
        self.default_mode = PrivacyMode.NORMAL
    
    def select_mode(
        self,
        user_preference: Optional[str] = None,
        risk_level: Optional[float] = None,
        transaction_amount: Optional[float] = None,
        curve_conditions: Optional[dict] = None
    ) -> PrivacyMode:
        """
        Select privacy mode based on multiple factors.
        
        Selection logic (priority order):
        1. User preference (with risk-based safety override)
        2. Risk level thresholds (if provided)
        3. Curve conditions (sniper_activity)
        4. Transaction amount thresholds
        5. Default mode
        
        Args:
            user_preference: User's preferred mode ("normal", "stealth", "max_ghost")
            risk_level: Risk level (0.0 to 1.0, higher = more risk)
            transaction_amount: Transaction amount in SOL
            curve_conditions: Dictionary with curve conditions:
                - sniper_activity: float (0.0 to 1.0)
        
        Returns:
            Selected PrivacyMode (NORMAL, STEALTH, or MAX_GHOST)
        
        Side effects: None (pure function)
        
        Examples:
            >>> selector = ModeSelector()
            >>> selector.select_mode(risk_level=0.2)
            PrivacyMode.NORMAL
            >>> selector.select_mode(risk_level=0.6)
            PrivacyMode.STEALTH
            >>> selector.select_mode(risk_level=0.9)
            PrivacyMode.MAX_GHOST
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
        Dynamically adjust mode based on execution context.
        
        Escalates privacy mode if conditions worsen, but never decreases it.
        This ensures monotonicity: increasing risk never reduces privacy.
        
        Args:
            current_mode: Current privacy mode
            context: Execution context dictionary:
                - risk_level: float (0.0 to 1.0)
                - sniper_activity: float (0.0 to 1.0)
        
        Returns:
            Adjusted PrivacyMode (may be same as current_mode if no escalation needed)
        
        Side effects: None (pure function)
        
        Escalation rules:
            - NORMAL -> STEALTH: if risk > 0.7 or sniper_activity > 0.6
            - STEALTH -> MAX_GHOST: if risk > 0.9 or sniper_activity > 0.8
        
        Examples:
            >>> selector = ModeSelector()
            >>> selector.adjust_mode_for_context(
            ...     PrivacyMode.NORMAL,
            ...     {"risk_level": 0.8, "sniper_activity": 0.7}
            ... )
            PrivacyMode.STEALTH
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

