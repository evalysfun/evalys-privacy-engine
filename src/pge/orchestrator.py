"""
Privacy Gradient Engine Orchestrator

Main orchestrator that coordinates privacy operations.
"""

from typing import Optional, Dict, Any
from .privacy_level import PrivacyMode, PrivacyLevel, get_privacy_level
from .mode_selector import ModeSelector
from ..utils.logger import get_logger

logger = get_logger(__name__)

# Optional Arcium bridge client (lazy import to avoid circular dependencies)
_arcium_client = None
_gmcp_client = None


def _get_arcium_client():
    """Lazy import of Arcium bridge client"""
    global _arcium_client
    if _arcium_client is None:
        try:
            # Import here to avoid requiring arcium-bridge as a hard dependency
            import sys
            import os
            # Add parent directory to path to import from evalys-arcium-bridge-service
            bridge_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                      "..", "evalys-arcium-bridge-service", "src")
            if os.path.exists(bridge_path):
                sys.path.insert(0, os.path.dirname(bridge_path))
                from bridge.arcium_client import ArciumBridgeClient
                from bridge.models import UserPreferences, UserHistory, CurveState
                _arcium_client = {
                    "client": ArciumBridgeClient,
                    "models": {
                        "UserPreferences": UserPreferences,
                        "UserHistory": UserHistory,
                        "CurveState": CurveState,
                    }
                }
        except ImportError:
            logger.warning("Arcium bridge service not available. Confidential mode will use fallback.")
            _arcium_client = False
    return _arcium_client


def _get_gmcp_client():
    """Lazy import of gMPC bridge client"""
    global _gmcp_client
    if _gmcp_client is None:
        try:
            import sys
            import os
            # Add parent directory to path to import from evalys-arcium-gMCP
            gmcp_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                     "..", "evalys-arcium-gMCP", "src")
            if os.path.exists(gmcp_path):
                sys.path.insert(0, os.path.dirname(gmcp_path))
                from bridge.gmcp_client import GMPCClient
                from bridge.models import IntentInput, MarketSnapshot, HistoricalStats
                _gmcp_client = {
                    "client": GMPCClient,
                    "models": {
                        "IntentInput": IntentInput,
                        "MarketSnapshot": MarketSnapshot,
                        "HistoricalStats": HistoricalStats,
                    }
                }
        except ImportError:
            logger.warning("gMPC bridge service not available. gMPC mode will use fallback.")
            _gmcp_client = False
    return _gmcp_client


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
        curve_conditions: Optional[Dict[str, Any]] = None,
        enable_arcium: bool = False,
        arcium_inputs: Optional[Dict[str, Any]] = None,
        use_gmcp: bool = False,
        gmcp_inputs: Optional[Dict[str, Any]] = None,
    ) -> PrivacyLevel:
        """
        Select and configure privacy mode
        
        Args:
            user_preference: User's preferred mode
            risk_level: Risk assessment (0.0 to 1.0)
            transaction_amount: Transaction amount in SOL
            curve_conditions: Curve analysis results
            enable_arcium: Whether to use Arcium confidential computation
            arcium_inputs: Optional inputs for Arcium (user_prefs, user_history, curve_state)
            use_gmcp: Whether to use gMPC for encrypted intent processing
            gmcp_inputs: Optional inputs for gMPC (intent, market_snapshot, historical_stats)
        
        Returns:
            Configured PrivacyLevel
        """
        # If gMPC requested (takes priority for encrypted intent processing)
        if use_gmcp or user_preference == "gmcp":
            gmcp_client_info = _get_gmcp_client()
            if gmcp_client_info and gmcp_inputs:
                try:
                    return self._select_mode_with_gmcp_sync(gmcp_inputs, gmcp_client_info)
                except Exception as e:
                    logger.warning(f"gMPC computation failed, falling back to standard mode: {e}")
                    # Fall through to standard mode selection
        
        # If confidential mode requested and Arcium is available
        if enable_arcium or user_preference == "confidential":
            arcium_client_info = _get_arcium_client()
            if arcium_client_info and arcium_inputs:
                try:
                    return self._select_mode_with_arcium_sync(arcium_inputs, arcium_client_info)
                except Exception as e:
                    logger.warning(f"Arcium computation failed, falling back to standard mode: {e}")
                    # Fall through to standard mode selection
        
        # Select mode (standard flow)
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
    
    async def _select_mode_with_arcium(
        self,
        arcium_inputs: Dict[str, Any],
        arcium_client_info: Dict[str, Any]
    ) -> PrivacyLevel:
        """
        Select mode using Arcium confidential computation
        
        Args:
            arcium_inputs: Inputs for Arcium computation
            arcium_client_info: Arcium client and models
            
        Returns:
            PrivacyLevel configured from Arcium plan
        """
        import asyncio
        
        client_class = arcium_client_info["client"]
        models = arcium_client_info["models"]
        
        client = client_class()
        
        # Build input models
        user_prefs = models["UserPreferences"](**arcium_inputs.get("user_preferences", {}))
        user_history = models["UserHistory"](**arcium_inputs.get("user_history", {}))
        curve_state = models["CurveState"](**arcium_inputs.get("curve_state", {}))
        
        # Get confidential plan from Arcium
        plan = await client.get_confidential_plan(
            user_preferences=user_prefs,
            user_history=user_history,
            curve_state=curve_state,
        )
        
        # Map Arcium plan to PrivacyLevel
        mode_map = {
            "normal": PrivacyMode.NORMAL,
            "stealth": PrivacyMode.STEALTH,
            "max_ghost": PrivacyMode.MAX_GHOST,
        }
        
        selected_mode = mode_map.get(plan.recommended_mode, PrivacyMode.MAX_GHOST)
        base_level = get_privacy_level(selected_mode)
        
        # Override with Arcium plan values
        privacy_level = PrivacyLevel(
            mode=PrivacyMode.CONFIDENTIAL,
            burner_count=base_level.burner_count,  # Could be adjusted by plan
            timing_jitter_ms=plan.timing_window_sec * 1000,  # Convert to ms
            order_slicing=True,
            fragmentation_level=plan.num_slices,
            use_mev_protection=True,
            rotation_frequency=1,
            use_arcium=True,
            arcium_plan_id=plan.plan_id,
        )
        
        await client.close()
        
        self.current_mode = PrivacyMode.CONFIDENTIAL
        self.current_level = privacy_level
        
        logger.info(
            f"Privacy mode selected via Arcium: CONFIDENTIAL "
            f"(plan_id: {plan.plan_id}, risk: {plan.risk_level}, "
            f"slices: {plan.num_slices}, timing: {plan.timing_window_sec}s)"
        )
        
        return privacy_level
    
    def _select_mode_with_arcium_sync(
        self,
        arcium_inputs: Dict[str, Any],
        arcium_client_info: Dict[str, Any]
    ) -> PrivacyLevel:
        """Synchronous wrapper for async Arcium call"""
        import asyncio
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop.run_until_complete(
            self._select_mode_with_arcium(arcium_inputs, arcium_client_info)
        )
    
    async def _select_mode_with_gmcp(
        self,
        gmcp_inputs: Dict[str, Any],
        gmcp_client_info: Dict[str, Any]
    ) -> PrivacyLevel:
        """
        Select mode using gMPC encrypted intent processing
        
        Args:
            gmcp_inputs: Inputs for gMPC computation
            gmcp_client_info: gMPC client and models
            
        Returns:
            PrivacyLevel configured from gMPC plan
        """
        import asyncio
        
        client_class = gmcp_client_info["client"]
        models = gmcp_client_info["models"]
        
        client = client_class()
        
        # Build intent input model
        IntentInput = models["IntentInput"]
        MarketSnapshot = models["MarketSnapshot"]
        HistoricalStats = models["HistoricalStats"]
        
        intent = IntentInput(
            trader_profile_id=gmcp_inputs.get("trader_profile_id", "anon-default"),
            token_mint=gmcp_inputs.get("token_mint", ""),
            launchpad=gmcp_inputs.get("launchpad", "pumpfun"),
            max_size_sol=gmcp_inputs.get("max_size_sol", 1.0),
            risk_level=gmcp_inputs.get("risk_level", "normal"),
            privacy_priority=gmcp_inputs.get("privacy_priority", "max_privacy"),
            market_snapshot=MarketSnapshot(**gmcp_inputs.get("market_snapshot", {})),
            historical_stats=HistoricalStats(**gmcp_inputs.get("historical_stats", {})),
        )
        
        # Get confidential plan from gMPC
        plan = await client.execute_gmpc_strategy(intent)
        
        # Map gMPC plan to PrivacyLevel
        mode_map = {
            "NORMAL": PrivacyMode.NORMAL,
            "STEALTH": PrivacyMode.STEALTH,
            "MAX_GHOST": PrivacyMode.MAX_GHOST,
        }
        
        selected_mode = mode_map.get(plan.privacy_mode, PrivacyMode.MAX_GHOST)
        base_level = get_privacy_level(selected_mode)
        
        # Override with gMPC plan values
        privacy_level = PrivacyLevel(
            mode=PrivacyMode.CONFIDENTIAL,
            burner_count=base_level.burner_count,
            timing_jitter_ms=plan.time_window_sec * 1000,  # Convert to ms
            order_slicing=True,
            fragmentation_level=plan.slice_count,
            use_mev_protection=True,
            rotation_frequency=1,
            use_arcium=True,
            arcium_plan_id=plan.plan_id,
        )
        
        await client.close()
        
        self.current_mode = PrivacyMode.CONFIDENTIAL
        self.current_level = privacy_level
        
        logger.info(
            f"Privacy mode selected via gMPC: CONFIDENTIAL "
            f"(plan_id: {plan.plan_id}, risk: {plan.risk_class}, "
            f"slices: {plan.slice_count}, timing: {plan.time_window_sec}s)"
        )
        
        return privacy_level
    
    def _select_mode_with_gmcp_sync(
        self,
        gmcp_inputs: Dict[str, Any],
        gmcp_client_info: Dict[str, Any]
    ) -> PrivacyLevel:
        """Synchronous wrapper for async gMPC call"""
        import asyncio
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop.run_until_complete(
            self._select_mode_with_gmcp(gmcp_inputs, gmcp_client_info)
        )
    
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

