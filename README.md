# Evalys Privacy Gradient Engine

Privacy Gradient Engine (PGE) - The core orchestrator for privacy modes in the Evalys ecosystem.

## 🎯 Overview

The Privacy Gradient Engine manages three privacy levels:
- **Normal**: Basic unlinkability with single burner wallet
- **Stealth**: Timing unpredictability with multiple burners
- **Max Ghost**: Full camouflage with maximum privacy features

## ✨ Features

- 🎚️ **Three Privacy Modes**: Normal, Stealth, Max Ghost
- 🤖 **Intelligent Mode Selection**: Auto-selects mode based on risk and conditions
- 🔄 **Dynamic Adjustment**: Adjusts privacy level based on execution context
- 🌐 **REST API**: Full API for integration
- 📦 **Standalone**: Can be used independently or as part of Evalys ecosystem

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

## 🏗️ Architecture

```
Privacy Gradient Engine
├── Mode Selector      # Selects appropriate mode
├── Privacy Levels     # Defines mode configurations
└── Orchestrator       # Main coordination logic
```

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
# Run tests
pytest

# With coverage
pytest --cov=src --cov-report=html

# Run specific test
pytest tests/test_orchestrator.py
```

## 📦 Project Structure

```
evalys-privacy-engine/
├── src/
│   ├── pge/              # Core PGE logic
│   │   ├── privacy_level.py
│   │   ├── mode_selector.py
│   │   └── orchestrator.py
│   ├── api/              # REST API
│   │   ├── routes.py
│   │   └── server.py
│   ├── config/          # Configuration
│   └── utils/           # Utilities
├── tests/               # Tests
├── requirements.txt
├── setup.py
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

## 🔗 Related Projects

- [evalys-burner-swarm](https://github.com/evalysfun/evalys-burner-swarm) - Burner wallet management
- [evalys-launchpad-adapters](https://github.com/evalysfun/evalys-launchpad-adapters) - Launchpad integrations
- [evalys-curve-intelligence](https://github.com/evalysfun/evalys-curve-intelligence) - Curve analysis
- [evalys-execution-engine](https://github.com/evalysfun/evalys-execution-engine) - Transaction execution

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/evalysfun/evalys-privacy-engine/issues)
- **Discord**: [Coming Soon]

---

**Evalys Privacy Gradient Engine** - Orchestrating privacy for memecoin launchpads 🛡️

