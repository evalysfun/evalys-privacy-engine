"""
API Routes for Privacy Gradient Engine

REST API endpoints for the Privacy Gradient Engine.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from ..pge.orchestrator import PrivacyGradientEngine
from ..pge.privacy_level import PrivacyMode
from ..config.settings import Settings

router = APIRouter(prefix="/api/v1/privacy", tags=["privacy"])

# Global engine instance (in production, use dependency injection)
engine = PrivacyGradientEngine(default_mode=Settings.get_default_mode())


class ModeSelectionRequest(BaseModel):
    """Request model for mode selection"""
    user_preference: Optional[str] = Field(None, description="Preferred mode: normal, stealth, max_ghost")
    risk_level: Optional[float] = Field(None, ge=0.0, le=1.0, description="Risk level (0.0 to 1.0)")
    transaction_amount: Optional[float] = Field(None, ge=0.0, description="Transaction amount in SOL")
    curve_conditions: Optional[Dict[str, Any]] = Field(None, description="Curve analysis conditions")


class PrivacyConfigResponse(BaseModel):
    """Response model for privacy configuration"""
    mode: str
    burner_count: int
    timing_jitter_ms: int
    order_slicing: bool
    fragmentation_level: int
    use_mev_protection: bool
    rotation_frequency: int


@router.post("/select-mode", response_model=PrivacyConfigResponse)
async def select_mode(request: ModeSelectionRequest):
    """
    Select privacy mode based on parameters
    
    Returns privacy configuration for the selected mode.
    """
    try:
        level = engine.select_mode(
            user_preference=request.user_preference,
            risk_level=request.risk_level,
            transaction_amount=request.transaction_amount,
            curve_conditions=request.curve_conditions
        )
        
        return PrivacyConfigResponse(
            mode=level.mode.value,
            burner_count=level.burner_count,
            timing_jitter_ms=level.timing_jitter_ms,
            order_slicing=level.order_slicing,
            fragmentation_level=level.fragmentation_level,
            use_mev_protection=level.use_mev_protection,
            rotation_frequency=level.rotation_frequency,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/current-config", response_model=PrivacyConfigResponse)
async def get_current_config():
    """Get current privacy configuration"""
    config = engine.get_privacy_config()
    if not config:
        raise HTTPException(status_code=404, detail="No privacy mode selected yet")
    return PrivacyConfigResponse(**config)


@router.post("/adjust", response_model=PrivacyConfigResponse)
async def adjust_privacy(context: Dict[str, Any]):
    """
    Adjust privacy level based on context
    
    Context should include risk indicators like:
    - risk_level: float
    - sniper_activity: float
    - etc.
    """
    try:
        level = engine.adjust_privacy_level(context)
        return PrivacyConfigResponse(
            mode=level.mode.value,
            burner_count=level.burner_count,
            timing_jitter_ms=level.timing_jitter_ms,
            order_slicing=level.order_slicing,
            fragmentation_level=level.fragmentation_level,
            use_mev_protection=level.use_mev_protection,
            rotation_frequency=level.rotation_frequency,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reset")
async def reset_engine():
    """Reset engine to default mode"""
    engine.reset()
    return {"message": "Engine reset to default mode"}


@router.get("/modes")
async def get_available_modes():
    """Get list of available privacy modes"""
    return {
        "modes": [mode.value for mode in PrivacyMode],
        "descriptions": {
            "normal": "Basic unlinkability - single burner, minimal jitter",
            "stealth": "Timing unpredictability - multiple burners, moderate jitter",
            "max_ghost": "Full camouflage - many burners, maximum jitter and slicing"
        }
    }

