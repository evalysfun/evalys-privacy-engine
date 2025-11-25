# Roadmap

This document outlines the planned features and improvements for the Privacy Gradient Engine.

## Version 0.1 (Current) ✅

**Status**: Released

- Rule-based privacy mode selection
- Three core privacy modes (Normal, Stealth, Max Ghost)
- REST API for integration
- Basic risk assessment
- Arcium bridge service integration hooks

## Version 0.2 (Planned)

**Target**: Q2 2024

### Real-Time Curve/Sniper Telemetry Integration

- **Curve Intelligence Integration**: Real-time bonding curve analysis
  - Sniper activity detection from Curve Intelligence Layer
  - Volatility metrics from live curve data
  - Launch freshness tracking

- **Enhanced Risk Model**: Full risk formula implementation
  - Weighted risk calculation (see `docs/risk-model.md`)
  - Dynamic weight adjustment
  - Historical pattern analysis

- **Telemetry Pipeline**: 
  - Real-time data feeds from Curve Intelligence
  - Caching and rate limiting
  - Fallback mechanisms

### Testing & Validation

- Integration tests with Curve Intelligence Layer
- End-to-end tests with Execution Engine
- Performance benchmarks
- Load testing for API

## Version 0.3 (Planned)

**Target**: Q3 2024

### Relay Mesh Integration

- **Private Relay Support**: Integration with relay networks
  - Multiple relay providers
  - Automatic failover
  - Relay performance metrics

- **Enhanced MEV Protection**:
  - Jito bundle optimization
  - Private mempool routing
  - Transaction timing coordination

### Advanced Privacy Features

- **Cross-Launchpad Privacy**: Unlinkability across platforms
  - Wallet rotation across launchpads
  - Pattern obfuscation
  - Cross-platform analytics

- **Adaptive Jitter**: Dynamic timing based on market conditions
  - Market-aware jitter calculation
  - Sniper activity response
  - Launch phase detection

## Version 0.4 (Future)

**Target**: Q4 2024

### MPC/Sharded Signing

- **Distributed Execution**: Sharded signing for maximum privacy
  - Multi-party transaction construction
  - Distributed key management
  - Coordinated execution

- **Zero-Knowledge Proofs**: Strategy verification without exposure
  - ZK proofs for privacy mode selection
  - Verifiable risk assessment
  - Privacy-preserving analytics

### Machine Learning Integration

- **ML-Based Risk Prediction**: 
  - Historical pattern learning
  - Sniper behavior prediction
  - Market condition classification

- **Adaptive Mode Selection**:
  - Learned thresholds
  - User behavior modeling
  - Dynamic weight optimization

## Version 0.5+ (Future Research)

### Advanced Features

- **Privacy-Preserving Analytics**: 
  - Multi-user aggregation
  - Differential privacy
  - Federated learning

- **Cross-Chain Privacy**:
  - Privacy across Solana and other chains
  - Bridge transaction obfuscation
  - Multi-chain wallet rotation

- **Decentralized Privacy Network**:
  - P2P privacy coordination
  - Distributed relay network
  - Community-driven privacy modes

## Contributing

We welcome contributions! See our contributing guidelines for:
- Feature proposals
- Bug reports
- Code contributions
- Documentation improvements

## Notes

- Roadmap is subject to change based on:
  - User feedback
  - Market conditions
  - Technical feasibility
  - Ecosystem developments

- Priority is given to:
  - Security and privacy improvements
  - Integration with other Evalys components
  - Performance optimizations
  - Developer experience

