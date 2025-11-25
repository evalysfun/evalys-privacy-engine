#!/usr/bin/env python3
"""
Quick demo of Privacy Gradient Engine

This script demonstrates the Privacy Gradient Engine API in action.
Run the API server first: python -m src.api.server
"""

import requests
import json
import time

API_BASE = "http://localhost:8000/api/v1/privacy"


def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(json.dumps(response, indent=2))


def demo_mode_selection():
    """Demonstrate mode selection with different risk levels"""
    print("\n" + "="*60)
    print("DEMO: Mode Selection")
    print("="*60)
    
    # Low risk trade
    print("\n1. Low Risk Trade (5 SOL, low sniper activity)")
    response = requests.post(
        f"{API_BASE}/select-mode",
        json={
            "user_preference": None,
            "risk_level": 0.2,
            "transaction_amount": 5.0,
            "curve_conditions": {"sniper_activity": 0.1}
        }
    )
    print_response("Response:", response.json())
    
    time.sleep(1)
    
    # Medium risk trade
    print("\n2. Medium Risk Trade (30 SOL, moderate sniper activity)")
    response = requests.post(
        f"{API_BASE}/select-mode",
        json={
            "user_preference": None,
            "risk_level": 0.6,
            "transaction_amount": 30.0,
            "curve_conditions": {"sniper_activity": 0.5}
        }
    )
    print_response("Response:", response.json())
    
    time.sleep(1)
    
    # High risk trade
    print("\n3. High Risk Trade (80 SOL, high sniper activity)")
    response = requests.post(
        f"{API_BASE}/select-mode",
        json={
            "user_preference": None,
            "risk_level": 0.9,
            "transaction_amount": 80.0,
            "curve_conditions": {"sniper_activity": 0.9}
        }
    )
    print_response("Response:", response.json())


def demo_user_preference():
    """Demonstrate user preference override"""
    print("\n" + "="*60)
    print("DEMO: User Preference")
    print("="*60)
    
    print("\nUser explicitly requests Max Ghost mode")
    response = requests.post(
        f"{API_BASE}/select-mode",
        json={
            "user_preference": "max_ghost",
            "risk_level": 0.3,
            "transaction_amount": 2.0
        }
    )
    print_response("Response:", response.json())


def demo_dynamic_adjustment():
    """Demonstrate dynamic privacy adjustment"""
    print("\n" + "="*60)
    print("DEMO: Dynamic Adjustment")
    print("="*60)
    
    # Start with normal mode
    print("\n1. Initial selection: Normal mode")
    response = requests.post(
        f"{API_BASE}/select-mode",
        json={
            "risk_level": 0.2,
            "transaction_amount": 3.0
        }
    )
    print_response("Response:", response.json())
    
    time.sleep(1)
    
    # Check current config
    print("\n2. Current configuration:")
    response = requests.get(f"{API_BASE}/current-config")
    print_response("Response:", response.json())
    
    time.sleep(1)
    
    # Adjust due to increased risk
    print("\n3. Adjusting due to increased risk (sniper activity detected)")
    response = requests.post(
        f"{API_BASE}/adjust",
        json={
            "risk_level": 0.8,
            "sniper_activity": 0.7
        }
    )
    print_response("Response:", response.json())


def demo_available_modes():
    """List available privacy modes"""
    print("\n" + "="*60)
    print("DEMO: Available Modes")
    print("="*60)
    
    response = requests.get(f"{API_BASE}/modes")
    print_response("Response:", response.json())


def main():
    """Run all demos"""
    print("\n" + "="*60)
    print("Privacy Gradient Engine - Quick Demo")
    print("="*60)
    print("\nMake sure the API server is running:")
    print("  python -m src.api.server")
    print("\nOr:")
    print("  uvicorn src.api.server:app --host 0.0.0.0 --port 8000")
    
    try:
        # Check if server is running
        response = requests.get("http://localhost:8000/health", timeout=2)
        if response.status_code != 200:
            print("\n❌ Server is not responding correctly")
            return
    except requests.exceptions.RequestException:
        print("\n❌ Cannot connect to API server at http://localhost:8000")
        print("   Please start the server first!")
        return
    
    print("\n✅ Server is running!")
    
    # Run demos
    demo_available_modes()
    demo_mode_selection()
    demo_user_preference()
    demo_dynamic_adjustment()
    
    print("\n" + "="*60)
    print("Demo complete!")
    print("="*60)


if __name__ == "__main__":
    main()

