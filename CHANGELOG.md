# Changelog

All notable changes to the Privacy Gradient Engine will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Threat model documentation (`docs/threat-model.md`)
- Risk model specification (`docs/risk-model.md`)
- Enhanced test suite with threshold and monotonicity tests
- Quick demo script (`examples/quick_demo.py`)
- CHANGELOG.md and ROADMAP.md

### Changed
- Updated README with measurable claims and scoped features
- Fixed README credibility issues (spacing, paths)
- Enhanced test coverage for risk model behavior

## [0.1.0] - Initial Release

### Added
- Three privacy modes: Normal, Stealth, Max Ghost
- Rule-based mode selection based on risk assessment
- REST API with FastAPI
- Privacy level configuration system
- Dynamic privacy adjustment
- Arcium confidential mode integration (bridge service support)
- gMPC encrypted intent processing (bridge service support)
- Basic test suite
- Documentation structure

### Features
- Mode selector with risk-based logic
- Privacy level definitions with configurable parameters
- Orchestrator for coordinating privacy operations
- API endpoints for mode selection, adjustment, and configuration
- Integration hooks for Arcium bridge services

### Technical Details
- Python 3.8+
- FastAPI for REST API
- Pydantic for data validation
- Configurable via environment variables

