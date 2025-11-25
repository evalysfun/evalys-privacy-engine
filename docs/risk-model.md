# Risk Model v0.1

## Overview

The Privacy Gradient Engine uses a rule-based risk scoring model to determine appropriate privacy modes. This document specifies the risk calculation formula, inputs, and thresholds.

## Risk Score Formula

The risk score is computed as a weighted combination of multiple factors:

```
risk = w1 * sniper_activity + w2 * tx_amount_norm + w3 * volatility + w4 * fresh_launch + w5 * user_preference_boost
```

Where:
- `sniper_activity`: Normalized sniper activity level (0.0 to 1.0)
- `tx_amount_norm`: Normalized transaction amount (0.0 to 1.0)
- `volatility`: Curve volatility indicator (0.0 to 1.0)
- `fresh_launch`: Fresh launch indicator (0.0 to 1.0, higher for newer launches)
- `user_preference_boost`: Boost based on user preference (0.0 to 0.2)

### Current Weights (v0.1)

```python
w1 = 0.35  # Sniper activity (primary factor)
w2 = 0.25  # Transaction amount
w3 = 0.20  # Volatility
w4 = 0.15  # Fresh launch
w5 = 0.05  # User preference boost
```

These weights sum to 1.0 and can be adjusted based on empirical data.

## Input Normalization

### Sniper Activity (0.0 to 1.0)

```python
sniper_activity = min(1.0, detected_snipers / max_expected_snipers)
```

Where:
- `detected_snipers`: Number of detected sniper wallets in recent activity
- `max_expected_snipers`: Maximum expected snipers (typically 10-20)

**Source**: Curve Intelligence Layer or on-chain analysis

### Transaction Amount Normalization (0.0 to 1.0)

```python
tx_amount_norm = min(1.0, transaction_amount_sol / 100.0)
```

Where:
- `transaction_amount_sol`: Transaction amount in SOL
- Normalized to 100 SOL max (adjustable threshold)

**Source**: User input or execution context

### Volatility (0.0 to 1.0)

```python
volatility = min(1.0, price_volatility / max_volatility)
```

Where:
- `price_volatility`: Standard deviation of recent price changes
- `max_volatility`: Maximum expected volatility (typically 0.5-1.0)

**Source**: Curve Intelligence Layer

### Fresh Launch (0.0 to 1.0)

```python
fresh_launch = max(0.0, 1.0 - (time_since_launch_hours / 24.0))
```

Where:
- `time_since_launch_hours`: Hours since token launch
- Decays to 0 after 24 hours

**Source**: Launchpad adapter or on-chain data

### User Preference Boost (0.0 to 0.2)

```python
if user_preference == "max_ghost":
    user_preference_boost = 0.2
elif user_preference == "stealth":
    user_preference_boost = 0.1
else:
    user_preference_boost = 0.0
```

**Source**: User input

## Mode Thresholds

Based on computed risk score:

| Risk Score | Privacy Mode | Rationale |
|------------|-------------|-----------|
| < 0.35 | Normal | Low risk, minimal protection needed |
| 0.35 - 0.7 | Stealth | Medium risk, moderate protection |
| > 0.7 | Max Ghost | High risk, maximum protection |

### Threshold Behavior

The mode selector enforces these thresholds:

```python
if risk_level > 0.8:
    return PrivacyMode.MAX_GHOST
elif risk_level > 0.5:
    return PrivacyMode.STEALTH
elif risk_level > 0.3:
    return PrivacyMode.NORMAL
else:
    return PrivacyMode.NORMAL  # Default
```

**Note**: User preference can override thresholds (with safety limits):
- User preference "max_ghost" with risk > 0.7 → Max Ghost
- User preference "normal" with risk > 0.7 → Escalated to Stealth (safety override)

## Risk Score Examples

### Example 1: Low Risk Trade

```
sniper_activity = 0.1
tx_amount_norm = 0.05  # 5 SOL
volatility = 0.2
fresh_launch = 0.3
user_preference_boost = 0.0

risk = 0.35*0.1 + 0.25*0.05 + 0.20*0.2 + 0.15*0.3 + 0.05*0.0
     = 0.035 + 0.0125 + 0.04 + 0.045 + 0.0
     = 0.1325

Result: Normal mode (risk < 0.35)
```

### Example 2: Medium Risk Trade

```
sniper_activity = 0.5
tx_amount_norm = 0.3  # 30 SOL
volatility = 0.4
fresh_launch = 0.6
user_preference_boost = 0.1

risk = 0.35*0.5 + 0.25*0.3 + 0.20*0.4 + 0.15*0.6 + 0.05*0.1
     = 0.175 + 0.075 + 0.08 + 0.09 + 0.005
     = 0.425

Result: Stealth mode (0.35 <= risk < 0.7)
```

### Example 3: High Risk Trade

```
sniper_activity = 0.9
tx_amount_norm = 0.8  # 80 SOL
volatility = 0.7
fresh_launch = 0.9
user_preference_boost = 0.2

risk = 0.35*0.9 + 0.25*0.8 + 0.20*0.7 + 0.15*0.9 + 0.05*0.2
     = 0.315 + 0.2 + 0.14 + 0.135 + 0.01
     = 0.8

Result: Max Ghost mode (risk > 0.7)
```

## Implementation Notes

### Current Implementation (v0.1)

The current implementation uses simplified heuristics:

1. **Direct risk_level input**: If provided, used directly (0.0 to 1.0)
2. **Sniper activity**: From `curve_conditions.get("sniper_activity", 0.0)`
3. **Transaction amount**: Direct threshold checks (> 10 SOL → Stealth, > 50 SOL → Max Ghost)
4. **User preference**: Direct mode selection with risk override

### Future Enhancements (v0.2+)

- Full risk formula implementation
- Integration with Curve Intelligence Layer for real-time metrics
- Machine learning model for risk prediction
- Historical risk pattern analysis
- Dynamic weight adjustment based on market conditions

## Validation

The risk model should satisfy:

1. **Monotonicity**: Increasing any risk factor should never decrease privacy mode
2. **Bounded**: Risk score always in [0.0, 1.0]
3. **Deterministic**: Same inputs → same risk score
4. **Threshold stability**: Small changes near thresholds don't cause mode oscillation

## Testing

See `tests/test_risk_model.py` for:
- Threshold boundary tests
- Monotonicity tests
- Input validation tests
- Edge case handling

