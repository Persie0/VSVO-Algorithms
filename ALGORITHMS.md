# VSVO-Algorithms: Distributed Systems Algorithm Collection

A collection of interactive Python implementations for distributed systems algorithms,
designed for exam preparation based on **van Steen/Tanenbaum - Distributed Systems (4th Ed)**.

---

## 📁 Main Directory

| File | Algorithm | Topic | Book Section |
|:-----|:----------|:------|:-------------|
| `Berkeley.py` | Berkeley Clock Sync | Synchronization | §6.1 |
| `ChordSystem.py` | Chord DHT | Flat Naming | §5.2 |
| `CryptoSystem.py` | Cryptographic Ops | Security | §9.2 |
| `DiffieHellman.py` | Diffie-Hellman Key Exchange | Security | §9.2 |
| `GreedyServerPlacementFixed.py` | Greedy Replica Placement | Replication | §7.4 |
| `LamportsLogicalClocks.py` | Lamport's Logical Clocks | Logical Clocks | §6.2 |
| `VectorClock.py` | Vector Clocks | Logical Clocks | §6.2 |
| `ReadWriteQuorums.py` | Read/Write Quorums | Consistency | §7.3 |
| `PolymorphPolyring.py` | Polymorph/Polyring | Naming | - |

---

## 📁 Optional Directory (`optional/`)

| File | Algorithm | Topic | Book Section |
|:-----|:----------|:------|:-------------|
| `BullyAlgorithm.py` | Bully Election | Leader Election | §6.4 |
| `RingAlgorithm.py` | Ring Election | Leader Election | §6.4 |
| `CristiansAlgorithm.py` | Cristian's Algorithm | Clock Sync | §6.1 |
| `NTPAlgorithm.py` | NTP (Network Time Protocol) | Clock Sync | §6.1 |
| `TwoPhaseCommit.py` | Two-Phase Commit (2PC) | Fault Tolerance | §8.2 |
| `ThreePhaseCommit.py` | Three-Phase Commit (3PC) | Fault Tolerance | §8.2 |
| `PaxosAlgorithm.py` | Paxos Consensus | Consensus | §8.2 |
| `DNSResolution.py` | DNS Resolution (Iterative/Recursive) | Naming | §5.3 |

---

## 🚀 Quick Start

```bash
# Activate virtual environment
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Run any algorithm interactively
python Berkeley.py
python optional/BullyAlgorithm.py
python optional/NTPAlgorithm.py
```

---

## 📖 Topic Coverage Summary

| Topic | Algorithms Implemented |
|:------|:-----------------------|
| **Clock Synchronization (§6.1)** | Berkeley, Cristian's, NTP |
| **Logical Clocks (§6.2)** | Lamport's, Vector Clocks |
| **Leader Election (§6.4)** | Bully, Ring |
| **Naming (§5)** | Chord DHT, DNS Resolution |
| **Consistency & Replication (§7)** | Read/Write Quorums, Greedy Server Placement |
| **Fault Tolerance (§8)** | 2PC, 3PC, Paxos |
| **Security (§9)** | Diffie-Hellman, Crypto Ops |
