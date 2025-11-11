"""
Privacy Gradient Engine Orchestrator

Main orchestrator that coordinates privacy operations.
"""

from typing import Optional, Dict, Any
from .privacy_level import PrivacyMode, PrivacyLevel, get_privacy_level
from .mode_selector import ModeSelector
from ..utils.logger import get_logger

logger = get_logger(__name__)


class PrivacyGradientEngine:
    """
    Privacy Gradient Engine - Main orchestrator for privacy operations
    
    This engine manages privacy modes and coordinates privacy-preserving
    operations across the Evalys ecosystem.
    """
    
    def __init__(self, default_mode: PrivacyMode = PrivacyMode.NORMAL):
        """
        Initialize Privacy Gradient Engine
        
        Args:
            default_mode: Default privacy mode to use
        """
        self.mode_selector = ModeSelector()
        self.default_mode = default_mode
        self.current_mode: Optional[PrivacyMode] = None
        self.current_level: Optional[PrivacyLevel] = None
        
        logger.info(f"Privacy Gradient Engine initialized with default mode: {default_mode}")
    
    def select_mode(
        self,
        user_preference: Optional[str] = None,
        risk_level: Optional[float] = None,
        transaction_amount: Optional[float] = None,
        curve_conditions: Optional[Dict[str, Any]] = None
    ) -> PrivacyLevel:
        """
        Select and configure privacy mode
        
        Args:
            user_preference: User's preferred mode
            risk_level: Risk assessment (0.0 to 1.0)
            transaction_amount: Transaction amount in SOL
            curve_conditions: Curve analysis results
        
        Returns:
            Configured PrivacyLevel
        """
        # Select mode
        selected_mode = self.mode_selector.select_mode(
            user_preference=user_preference,
            risk_level=risk_level,
            transaction_amount=transaction_amount,
            curve_conditions=curve_conditions
        )
        
        # Get privacy level configuration
        privacy_level = get_privacy_level(selected_mode)
        
        # Store current state
        self.current_mode = selected_mode
        self.current_level = privacy_level
        
        logger.info(
            f"Privacy mode selected: {selected_mode.value} "
            f"(burners: {privacy_level.burner_count}, "
            f"jitter: {privacy_level.timing_jitter_ms}ms, "
            f"slicing: {privacy_level.order_slicing})"
        )
        
        return privacy_level
    
    def get_current_level(self) -> Optional[PrivacyLevel]:
        """
        Get current privacy level configuration
        
        Returns:
            Current PrivacyLevel or None if not set
        """
        return self.current_level
    
    def adjust_privacy_level(self, context: Dict[str, Any]) -> PrivacyLevel:
        """
        Dynamically adjust privacy level based on context
        
        Args:
            context: Execution context with risk indicators
        
        Returns:
            Adjusted PrivacyLevel
        """
        if not self.current_mode:
            # No current mode, select based on context
            return self.select_mode(
                risk_level=context.get("risk_level"),
                curve_conditions=context
            )
        
        # Adjust current mode
        adjusted_mode = self.mode_selector.adjust_mode_for_context(
            self.current_mode,
            context
        )
        
        # If mode changed, update level
        if adjusted_mode != self.current_mode:
            logger.info(
                f"Privacy mode adjusted: {self.current_mode.value} -> {adjusted_mode.value}"
            )
            self.current_mode = adjusted_mode
            self.current_level = get_privacy_level(adjusted_mode)
        
        return self.current_level
    
    def get_privacy_config(self) -> Dict[str, Any]:
        """
        Get current privacy configuration as dictionary
        
        Returns:
            Dictionary with privacy configuration
        """
        if not self.current_level:
            return {}
        
        return {
            "mode": self.current_level.mode.value,
            "burner_count": self.current_level.burner_count,
            "timing_jitter_ms": self.current_level.timing_jitter_ms,
            "order_slicing": self.current_level.order_slicing,
            "fragmentation_level": self.current_level.fragmentation_level,
            "use_mev_protection": self.current_level.use_mev_protection,
            "rotation_frequency": self.current_level.rotation_frequency,
        }
    
    def reset(self):
        """Reset to default mode"""
        self.current_mode = None
        self.current_level = None
        logger.info("Privacy Gradient Engine reset to default")

