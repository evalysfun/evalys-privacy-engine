# Evalys Privacy Gradient Engine

Privacy Gradient Engine (PGE) - The core orchestrator for privacy modes in the Evalys ecosystem.

## 🎯 Overview

The Privacy Gradient Engine manages three privacy levels:
- **Normal**: Basic unlinkability (1 burner, 100ms jitter, no slicing)
- **Stealth**: Timing unpredictability (3 burners, 500ms jitter, 3 slices, MEV protection)
- **Max Ghost**: Highest mitigation profile (5+ burners, 2000ms jitter, 8 slices, MEV protection)

## ✨ Features

- 🎚️ **Three Privacy Modes**: Normal, Stealth, Max Ghost (v0.1 - rule-based selection)
- 🤖 **Rule-Based Mode Selection (v0.1)**: Selects mode based on risk thresholds and conditions (pluggable for ML in v0.4)
- 🔄 **Dynamic Adjustment**: Adjusts privacy level based on execution context (risk escalation)
- 🌐 **REST API**: FastAPI-based API for integration (5 endpoints, health check)
- 📦 **Standalone**: Can be used independently or as part of Evalys ecosystem
- 🔐 **Arcium Integration**: Support for confidential computation via Arcium bridge services (hooks ready)

## 🚀 Installation

### From Source (Recommended: Shared Virtual Environment)

For the Evalys ecosystem, it's recommended to use a **shared virtual environment** at the root level:

```bash
# From evalys root directory
python -m venv venv

# Activate virtual environment
# Windows PowerShell:
venv\Scripts\Activate.ps1
$env:PYTHONPATH = "."
# Windows CMD:
venv\Scripts\activate.bat
set PYTHONPATH=.
# Linux/Mac:
source venv/bin/activate
export PYTHONPATH=.

# Navigate to component directory
cd evalys-privacy-engine

# Install dependencies
pip install -r requirements.txt
pip install -e .
```

**Note**: Using a shared venv at the root avoids duplication and reduces project size. All Evalys components share the same environment.

### Standalone Installation

If using this component independently:

```bash
git clone https://github.com/evalysfun/evalys-privacy-engine
cd evalys-privacy-engine
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
pip install -e .
```

### As Python Package (Future)

```bash
pip install evalys-privacy-engine
```

## 📖 Usage

### As Python Library

```python
from evalys_privacy_engine import PrivacyGradientEngine, PrivacyMode

# Initialize engine
engine = PrivacyGradientEngine(default_mode=PrivacyMode.NORMAL)

# Select mode based on conditions
privacy_level = engine.select_mode(
    user_preference="max_ghost",
    risk_level=0.8,
    transaction_amount=5.0,
    curve_conditions={"sniper_activity": 0.6}
)

# Get configuration
config = engine.get_privacy_config()
print(f"Mode: {config['mode']}")
print(f"Burner count: {config['burner_count']}")
print(f"Timing jitter: {config['timing_jitter_ms']}ms")

# Adjust based on context
adjusted = engine.adjust_privacy_level({
    "risk_level": 0.9,
    "sniper_activity": 0.8
})
```

### As REST API

```bash
# Start the API server
python -m src.api.server

# Or use uvicorn directly
uvicorn src.api.server:app --host 0.0.0.0 --port 8000
```

#### API Endpoints

- `POST /api/v1/privacy/select-mode` - Select privacy mode
- `GET /api/v1/privacy/current-config` - Get current configuration
- `POST /api/v1/privacy/adjust` - Adjust privacy level
- `POST /api/v1/privacy/reset` - Reset to default
- `GET /api/v1/privacy/modes` - List available modes
- `GET /health` - Health check

#### Example API Request

```bash
curl -X POST "http://localhost:8000/api/v1/privacy/select-mode" \
  -H "Content-Type: application/json" \
  -d '{
    "user_preference": "max_ghost",
    "risk_level": 0.8,
    "transaction_amount": 5.0
  }'
```

#### Quick Demo (Standalone - Perfect for Screen Recording!)

Run the standalone promotional demo (no server required):

```bash
# Run the demo script
python demo.py

# Or with quiet mode (suppresses logging for cleaner output)
python demo.py --quiet
```

The demo shows:
- Mode selection with different risk levels
- User preference handling
- Dynamic privacy adjustment
- Risk threshold visualization

**Perfect for screen recordings and promotional videos!**

#### API Demo (Alternative)

For API-based demo, start the server first:

```bash
# Start the API server
python -m src.api.server

# In another terminal, run the API demo
python examples/quick_demo.py
```

## 🏗️ Architecture

```
Privacy Gradient Engine
├── Mode Selector      # Rule-based mode selection (risk thresholds)
├── Privacy Levels     # Mode configurations (burner count, jitter, slicing)
└── Orchestrator       # Main coordination logic (mode selection, Arcium hooks)
```

### Core Components

- **`src/pge/mode_selector.py`**: Rule-based mode selection logic
  - Inputs: user_preference, risk_level, transaction_amount, curve_conditions
  - Outputs: PrivacyMode (NORMAL, STEALTH, MAX_GHOST)
  - Side effects: None (pure function)

- **`src/pge/privacy_level.py`**: Privacy level definitions
  - Defines: burner_count, timing_jitter_ms, order_slicing, fragmentation_level
  - Invariants: fragmentation_level in [1, 10], burner_count >= 1

- **`src/pge/orchestrator.py`**: Main orchestrator
  - Inputs: mode selection parameters, Arcium/gMPC inputs (optional)
  - Outputs: PrivacyLevel configuration
  - Side effects: Logging, state management

- **`src/api/routes.py`**: REST API endpoints
  - Endpoints: /select-mode, /current-config, /adjust, /reset, /modes
  - Inputs: JSON request bodies
  - Outputs: JSON responses with privacy config

See `docs/threat-model.md` and `docs/risk-model.md` for detailed specifications.

## 🔧 Configuration

Set environment variables:

```bash
export DEFAULT_PRIVACY_MODE=normal  # or stealth, max_ghost
export LOG_LEVEL=INFO
export API_HOST=0.0.0.0
export API_PORT=8000
```

## 🧪 Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=src --cov-report=html

# Run specific test suite
pytest tests/test_orchestrator.py
pytest tests/test_mode_selector.py
pytest tests/test_risk_model.py  # Threshold, monotonicity, config stability tests
```

### Test Coverage

Tests verify:
- ✅ Mode selection thresholds (risk < 0.35 → Normal, 0.35-0.7 → Stealth, > 0.7 → Max Ghost)
- ✅ Config stability (same inputs → same config)
- ✅ Monotonicity (increasing risk never decreases privacy mode)
- ✅ User preference handling with safety overrides
- ✅ Dynamic adjustment behavior

See `tests/test_risk_model.py` for risk model behavior tests.

## 📦 Project Structure

```
evalys-privacy-engine/
├── src/
│   ├── pge/              # Core PGE logic
│   │   ├── privacy_level.py    # Privacy level definitions
│   │   ├── mode_selector.py    # Rule-based mode selection
│   │   └── orchestrator.py     # Main orchestrator + Arcium hooks
│   ├── api/              # REST API
│   │   ├── routes.py     # API endpoints
│   │   └── server.py     # FastAPI server
│   ├── config/          # Configuration
│   │   └── settings.py  # Environment-based settings
│   └── utils/           # Utilities
│       └── logger.py    # Logging utilities
├── tests/               # Test suite
│   ├── test_orchestrator.py
│   ├── test_mode_selector.py
│   ├── test_privacy_level.py
│   └── test_risk_model.py  # Risk model behavior tests
├── docs/                # Documentation
│   ├── threat-model.md  # Threat model and adversaries
│   └── risk-model.md    # Risk scoring formula and thresholds
├── examples/            # Example scripts
│   └── quick_demo.py    # Interactive API demo
├── requirements.txt
├── setup.py
├── CHANGELOG.md
├── ROADMAP.md
└── README.md
```

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines first.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📚 Documentation

- **[Threat Model](docs/threat-model.md)**: Adversaries, attack vectors, and mitigations
- **[Risk Model](docs/risk-model.md)**: Risk scoring formula, thresholds, and examples
- **[Changelog](CHANGELOG.md)**: Version history and changes
- **[Roadmap](ROADMAP.md)**: Planned features and improvements

## 🔗 Related Projects

- [evalys-burner-swarm](https://github.com/evalysfun/evalys-burner-swarm) - Burner wallet management
- [evalys-launchpad-adapters](https://github.com/evalysfun/evalys-launchpad-adapters) - Launchpad integrations
- [evalys-curve-intelligence](https://github.com/evalysfun/evalys-curve-intelligence) - Curve analysis
- [evalys-execution-engine](https://github.com/evalysfun/evalys-execution-engine) - Transaction execution
- [evalys-arcium-bridge-service](https://github.com/evalysfun/evalys-arcium-bridge-service) - Arcium confidential compute bridge
- [evalys-arcium-gMPC](https://github.com/evalysfun/evalys-arcium-gMPC) - Arcium gMPC bridge service

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/evalysfun/evalys-privacy-engine/issues)
- **Discord**: [Coming Soon]

---

**Evalys Privacy Gradient Engine** - Orchestrating privacy for memecoin launchpads 🛡️

