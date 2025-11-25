# Threat Model

## Overview

The Privacy Gradient Engine (PGE) protects users from various adversaries on Solana memecoin launchpads. This document outlines the threats we defend against and the mitigation strategies.

## Adversaries

### 1. Snipers / Front-Runners

**Description**: Bots that monitor mempools and on-chain activity to detect and front-run profitable trades.

**Capabilities**:
- Real-time mempool monitoring
- Pattern recognition (wallet clustering, timing analysis)
- Fast transaction submission (often via private RPCs)

**Threat Level**: High

**Mitigation**:
- Burner wallet rotation (unlinkability)
- Timing jitter (unpredictability)
- Order slicing (obfuscation)
- MEV protection (Jito bundles, private relays)

### 2. Copy Trading Bots

**Description**: Bots that identify profitable wallets and copy their trades automatically.

**Capabilities**:
- Wallet profiling and tracking
- Trade replication
- Multi-wallet coordination

**Threat Level**: Medium-High

**Mitigation**:
- Burner wallet usage (breaks wallet identity)
- Timing randomization (prevents pattern matching)
- Fragmentation (makes copying less effective)

### 3. MEV Extractors

**Description**: Validators and searchers that extract value by reordering transactions.

**Capabilities**:
- Transaction reordering
- Sandwich attacks
- Arbitrage extraction

**Threat Level**: Medium

**Mitigation**:
- Jito bundle submission (atomic execution)
- Private relay usage (reduces visibility)
- Timing coordination (reduces MEV opportunities)

### 4. On-Chain Analysts

**Description**: Entities analyzing on-chain data to profile users and strategies.

**Capabilities**:
- Historical transaction analysis
- Graph analysis (wallet clustering)
- Pattern detection

**Threat Level**: Medium

**Mitigation**:
- Burner wallet rotation (limits historical tracking)
- Order fragmentation (obfuscates intent)
- Timing jitter (breaks patterns)

### 5. Launchpad Operators

**Description**: Launchpad platforms that may have privileged access to transaction data.

**Capabilities**:
- Direct access to pending transactions
- User profiling
- Potential front-running

**Threat Level**: Low-Medium (varies by launchpad)

**Mitigation**:
- Standard privacy modes (burners, jitter)
- Max Ghost mode for high-value trades

## Attack Vectors

### 1. Wallet Clustering

**Attack**: Link multiple burner wallets to a single user through timing, amounts, or patterns.

**Defense**: 
- Random timing jitter
- Varied transaction amounts
- Independent burner wallet generation

### 2. Pattern Recognition

**Attack**: Identify user behavior patterns (timing, size, target tokens).

**Defense**:
- Timing randomization
- Order slicing with variable sizes
- Mode escalation based on risk

### 3. Mempool Surveillance

**Attack**: Monitor mempool for pending transactions and front-run.

**Defense**:
- MEV protection (Jito bundles)
- Private relay usage
- Timing coordination

### 4. Graph Analysis

**Attack**: Analyze transaction graphs to identify relationships.

**Defense**:
- Burner wallet rotation
- Fragmented execution
- Unlinkable transaction patterns

## Privacy Modes

### Normal Mode

**Threat Coverage**: Basic protection against casual observers

**Mitigations**:
- Single burner wallet
- Minimal timing jitter (100ms)
- No order slicing

**Use Case**: Low-value trades, low-risk environments

### Stealth Mode

**Threat Coverage**: Protection against most snipers and copy bots

**Mitigations**:
- Multiple burner wallets (3)
- Moderate timing jitter (500ms)
- Order slicing (3 fragments)
- MEV protection enabled

**Use Case**: Medium-value trades, moderate risk

### Max Ghost Mode

**Threat Coverage**: Maximum protection against all adversaries

**Mitigations**:
- Many burner wallets (5+)
- High timing jitter (2000ms)
- Heavy order slicing (8 fragments)
- MEV protection enabled
- Frequent wallet rotation

**Use Case**: High-value trades, high-risk environments, sensitive operations

### Confidential Mode (Arcium)

**Threat Coverage**: Protection of strategy and intent computation

**Mitigations**:
- Encrypted computation (MPC)
- Private strategy generation
- No exposure of raw inputs

**Use Case**: When strategy itself must remain private

## Risk Assessment

The engine uses a risk scoring model (see `docs/risk-model.md`) to determine appropriate privacy mode:

- **Low Risk (< 0.35)**: Normal mode
- **Medium Risk (0.35 - 0.7)**: Stealth mode
- **High Risk (> 0.7)**: Max Ghost mode

Risk factors include:
- Transaction amount
- Sniper activity levels
- Curve volatility
- Launch freshness
- User preference

## Limitations

1. **On-Chain Visibility**: All transactions are ultimately visible on-chain. We can only obfuscate patterns, not hide transactions entirely.

2. **Timing Constraints**: Some launchpads have time-sensitive opportunities that limit our ability to add jitter.

3. **Cost**: Higher privacy modes have higher gas costs (more transactions, more burners).

4. **Coordination**: Some mitigations require coordination with other Evalys components (burner swarm, execution engine).

## Future Enhancements

- Relay mesh integration for additional obfuscation
- Cross-launchpad privacy (unlinkability across platforms)
- Zero-knowledge proofs for strategy verification
- Sharded signing for distributed execution

