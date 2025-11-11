# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Setup Shared Virtual Environment (Recommended)

Since Evalys uses multiple components, it's recommended to use a **shared virtual environment** at the root level:

```bash
# From evalys root directory (parent of evalys-privacy-engine)
cd ..  # Go to evalys root

# Create shared virtual environment
python -m venv venv

# Activate virtual environment
# On Windows PowerShell:
venv\Scripts\Activate.ps1
# On Windows CMD:
venv\Scripts\activate.bat
# On Linux/Mac:
source venv/bin/activate

# Set PYTHONPATH to include current directory (for imports)
# On Windows PowerShell:
$env:PYTHONPATH = "."
# On Windows CMD:
set PYTHONPATH=.
# On Linux/Mac:
export PYTHONPATH=.

# Navigate to privacy engine directory
cd evalys-privacy-engine

# Install dependencies
pip install -r requirements.txt
```

**Note**: The shared venv approach avoids duplication and reduces total project size. All Evalys components can use the same virtual environment.

### 2. Run Example

```bash
# Make sure you're in evalys-privacy-engine directory
# and venv is activated with PYTHONPATH set
python example.py
```

This will demonstrate all the features of the Privacy Gradient Engine.

### 3. Use as Python Library

```python
from src.pge.orchestrator import PrivacyGradientEngine

# Initialize
engine = PrivacyGradientEngine()

# Select mode
level = engine.select_mode(
    user_preference="max_ghost",
    risk_level=0.8
)

# Get configuration
config = engine.get_privacy_config()
print(config)
```

### 4. Run as API Server

```bash
# Start the API server
python -m src.api.server

# Or use uvicorn directly
uvicorn src.api.server:app --host 0.0.0.0 --port 8000 --reload
```

Then visit:
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### 5. Test API

```bash
# Select privacy mode
curl -X POST "http://localhost:8000/api/v1/privacy/select-mode" \
  -H "Content-Type: application/json" \
  -d '{
    "user_preference": "max_ghost",
    "risk_level": 0.8
  }'

# Get current config
curl http://localhost:8000/api/v1/privacy/current-config
```

### 6. Run Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Run tests
pytest

# With coverage
pytest --cov=src --cov-report=html
```

## 📚 Next Steps

- Read the [README.md](README.md) for detailed documentation
- Check out the [example.py](example.py) for more usage examples
- Explore the API at http://localhost:8000/docs when server is running

## 🐛 Troubleshooting

### Import Errors
Make sure you're in the project root directory and have installed dependencies:
```bash
pip install -r requirements.txt
```

### Port Already in Use
Change the port in `.env` or environment variable:
```bash
export API_PORT=8001
```

### Module Not Found
Make sure:
1. Virtual environment is activated
2. PYTHONPATH is set (see step 1)
3. You're in the evalys-privacy-engine directory

```bash
# Verify PYTHONPATH is set
echo $env:PYTHONPATH  # Windows PowerShell
# or
echo $PYTHONPATH      # Linux/Mac

# Run from component directory
python -m src.api.server
```

