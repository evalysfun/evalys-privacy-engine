"""
Example usage of Evalys Privacy Gradient Engine
"""

from src.pge.orchestrator import PrivacyGradientEngine
from src.pge.privacy_level import PrivacyMode


def main():
    """Example usage"""
    print("=" * 60)
    print("Evalys Privacy Gradient Engine - Example")
    print("=" * 60)
    
    # Initialize engine
    engine = PrivacyGradientEngine(default_mode=PrivacyMode.NORMAL)
    print("\n✅ Engine initialized")
    
    # Example 1: Select mode with user preference
    print("\n📋 Example 1: User preference")
    level = engine.select_mode(user_preference="max_ghost")
    config = engine.get_privacy_config()
    print(f"   Selected mode: {config['mode']}")
    print(f"   Burner count: {config['burner_count']}")
    print(f"   Timing jitter: {config['timing_jitter_ms']}ms")
    print(f"   Order slicing: {config['order_slicing']}")
    
    # Example 2: Auto-select based on risk
    print("\n📋 Example 2: Risk-based selection")
    engine.reset()
    level = engine.select_mode(risk_level=0.85)
    config = engine.get_privacy_config()
    print(f"   Risk level: 0.85")
    print(f"   Auto-selected mode: {config['mode']}")
    
    # Example 3: Adjust based on context
    print("\n📋 Example 3: Dynamic adjustment")
    engine.select_mode(user_preference="normal")
    print(f"   Initial mode: {engine.get_privacy_config()['mode']}")
    
    adjusted = engine.adjust_privacy_level({
        "risk_level": 0.9,
        "sniper_activity": 0.8
    })
    print(f"   After adjustment: {adjusted.mode.value}")
    print(f"   New burner count: {adjusted.burner_count}")
    
    # Example 4: Transaction amount based
    print("\n📋 Example 4: Transaction amount based")
    engine.reset()
    level = engine.select_mode(transaction_amount=25.0)
    config = engine.get_privacy_config()
    print(f"   Transaction amount: 25 SOL")
    print(f"   Selected mode: {config['mode']}")
    
    # Example 5: Curve conditions
    print("\n📋 Example 5: Curve conditions")
    engine.reset()
    level = engine.select_mode(curve_conditions={
        "sniper_activity": 0.75,
        "liquidity_depth": 0.5
    })
    config = engine.get_privacy_config()
    print(f"   Sniper activity: 0.75")
    print(f"   Selected mode: {config['mode']}")
    
    print("\n" + "=" * 60)
    print("✅ Examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()

