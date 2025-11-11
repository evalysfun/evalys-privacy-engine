# Setup Guide - Shared Virtual Environment

## 🎯 Recommended Setup for Evalys Ecosystem

Since Evalys consists of multiple Python components, we use a **shared virtual environment** at the root level to:
- ✅ Avoid duplication
- ✅ Reduce total project size
- ✅ Share dependencies across components
- ✅ Simplify dependency management

## 📋 Step-by-Step Setup

### 1. Navigate to Evalys Root

```bash
# From evalys-privacy-engine directory
cd ..  # Go to evalys root directory
```

Your structure should look like:
```
evalys/
├── venv/                    # Shared virtual environment (we'll create this)
├── evalys-privacy-engine/
├── evalys-burner-swarm/
├── evalys-launchpad-adapters/
└── ... (other components)
```

### 2. Create Virtual Environment

```bash
# Create shared virtual environment
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows PowerShell:**
```powershell
venv\Scripts\Activate.ps1
$env:PYTHONPATH = "."
```

**Windows CMD:**
```cmd
venv\Scripts\activate.bat
set PYTHONPATH=.
```

**Linux/Mac:**
```bash
source venv/bin/activate
export PYTHONPATH=.
```

### 4. Install Component Dependencies

```bash
# Navigate to component directory
cd evalys-privacy-engine

# Install dependencies
pip install -r requirements.txt

# Install component in development mode (optional)
pip install -e .
```

### 5. Verify Setup

```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Test import
python -c "from src.pge.orchestrator import PrivacyGradientEngine; print('✅ Import successful')"
```

## 🔄 Working with Multiple Components

Once the shared venv is set up:

```bash
# Activate venv (from evalys root)
venv\Scripts\Activate.ps1  # Windows PowerShell
$env:PYTHONPATH = "."

# Work on privacy engine
cd evalys-privacy-engine
python example.py

# Switch to another component
cd ../evalys-burner-swarm
python example.py

# All components share the same venv!
```

## 🐛 Troubleshooting

### Import Errors

If you get `ModuleNotFoundError`:

1. **Check venv is activated:**
   ```bash
   which python  # Should point to venv
   ```

2. **Verify PYTHONPATH is set:**
   ```bash
   echo $env:PYTHONPATH  # Windows PowerShell
   echo $PYTHONPATH      # Linux/Mac
   ```

3. **Make sure you're in the right directory:**
   ```bash
   # Should be in evalys root when setting PYTHONPATH
   # Then navigate to component directory
   ```

### Virtual Environment Not Found

If `venv\Scripts\Activate.ps1` doesn't exist:

1. Make sure you created venv in the **evalys root** directory
2. Check you're using the correct path
3. Try creating it again: `python -m venv venv`

### PYTHONPATH Not Persisting

PYTHONPATH needs to be set in each new terminal session. You can:

1. **Create a setup script** (`setup.ps1` for Windows):
   ```powershell
   # setup.ps1
   venv\Scripts\Activate.ps1
   $env:PYTHONPATH = "."
   ```

2. **Or add to your shell profile** (`.bashrc`, `.zshrc`, etc.)

## ✅ Quick Setup Script

Create a `setup.ps1` in evalys root:

```powershell
# setup.ps1
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv venv
}

Write-Host "Activating virtual environment..."
venv\Scripts\Activate.ps1

Write-Host "Setting PYTHONPATH..."
$env:PYTHONPATH = "."

Write-Host "✅ Setup complete! Virtual environment activated."
Write-Host "You can now navigate to any component directory and run scripts."
```

Then just run:
```powershell
.\setup.ps1
```

---

**Remember**: Always activate the venv and set PYTHONPATH from the **evalys root** directory, then navigate to component directories as needed.

