# Complete Methodology: Anatomy of the October 10, 2025 ADL Event

**Document Purpose**: Comprehensive guide for researchers to understand and reproduce our complete analysis  
**Last Updated**: November 13, 2025  
**Event**: October 10, 2025 Hyperliquid Liquidation Cascade (21:15-21:27 UTC)

---

## 📚 Table of Contents

1. [Overview & Timeline](#overview--timeline)
2. [Data Sources](#data-sources)
3. [Data Acquisition](#data-acquisition)
4. [Data Processing Pipeline](#data-processing-pipeline)
5. [Analysis Stages](#analysis-stages)
6. [Key Discoveries](#key-discoveries)
7. [Reproducibility Guide](#reproducibility-guide)
8. [Data Reconciliation](#data-reconciliation)

---

## Overview & Timeline

### The Event

**Date**: October 10, 2025  
**Time**: 21:15:00 - 21:27:00 UTC (12 minutes)  
**Type**: Liquidation cascade triggering Auto-Deleveraging (ADL)  
**Impact**: $7.61 billion in forced position closures

### Analysis Evolution

| Date | Milestone | Data Used | Coverage |
|------|-----------|-----------|----------|
| **Nov 7, 2025** | Initial event analysis | S3 node_fills | 100% event data |
| **Nov 8, 2025** | Full 12-min analysis | S3 node_fills | All 98,620 events |
| **Nov 11, 2025** | Timing & batch discovery | Event sequencing | Cascade mechanics |
| **Nov 12, 2025** | **Clearinghouse breakthrough** | Snapshot + fills | Account-level data |
| **Nov 13, 2025** | Real-time reconstruction (canonical) | Snapshot + full replay | 100% account + event coverage |

### What We Can Now Answer

**Phase 1** (Event Data Only):
- ✅ How many events? → 98,620 (63,637 liquidations + 34,983 ADL)
- ✅ Total notional? → $7.61 billion
- ✅ Which assets? → 171 tickers
- ✅ Event timing? → ~64-second delay before ADL, burst patterns
- ✅ Batch processing? → Liquidations then ADL, sequentially

**Phase 2** (+ Clearinghouse Data Snapshot - Historical Approximation):
- ✅ What leverage were ADL'd positions? → Snapshot-only estimate (avg 1.16x, 31,444 events ≈90% coverage)
- ✅ How profitable? → 98.3% profitable (avg +82% PNL) using snapshot values
- ✅ Entry prices? → Calculated for 31,444 events (positions visible in snapshot)
- ✅ ADL prioritization? → **Pointed to profit targeting** (led to Phase 3)
- ⚠️ Limitations: Snapshot 70 min stale, no negative equity, no real-time account values

**Phase 3** (+ Real-Time Reconstruction - Canonical Dataset):
- ✅ Real-time leverage? → Median 0.18x (95th pct 4.23x, 99th pct 74.18x)
- ✅ Real-time PNL? → 94.5% profitable (avg +80.58% PNL)
- ✅ Negative equity? → **1,147 accounts (−$109.29M insurance impact)**
- ✅ Account values? → **437,723 accounts reconstructed in real-time**
- ✅ Total equity? → Cash + unrealized PNL at exact ADL moment
- ✅ Insurance fund impact? → **$109.29M coverage required**

---

## Data Sources

### 1. Event Data (S3 Bucket)

**Source**: Hyperliquid AWS S3  
**Bucket**: `s3://hl-mainnet-node-data/node_fills_by_block/`  
**File**: `hourly/20251010/21.lz4`

**What It Contains**:
- All fills (trades, liquidations, ADL) with nanosecond timestamps
- Direction labels: "Buy", "Sell", "Liquidated Cross Long", "Auto-Deleveraging", etc.
- Price, size, closedPnl, fees for each fill
- User addresses (anonymized)
- No account values or position history

**Coverage**: 
- Hour 20: `20.lz4` (20:00:00 - 20:59:59 UTC)
- Hour 21: `21.lz4` (21:00:00 - 21:59:59 UTC) ← **Main cascade hour**

**Format**: LZ4-compressed JSON lines (JSONL)  
**Size**: ~2 GB uncompressed for hour 21

**Data Structure**:
```json
{
  "local_time": "2025-10-10T21:16:04.831874828",
  "block_time": "2025-10-10T21:16:04.831874687",
  "block_number": 758800641,
  "events": [
    [
      "0xe92d2041199b18f611b137457f3acee8bedb22d3",
      {
        "coin": "AVAX",
        "px": "22.075",
        "sz": "28.53",
        "side": "B",
        "time": 1760130964831,
        "startPosition": "-28.53",
        "dir": "Auto-Deleveraging",
        "closedPnl": "194.275035",
        "hash": "0x922ada1583e0175a93a4042d3a6101010100f1fb1ee3362c35f3856842e3f145",
        "oid": 194018286846,
        "crossed": true,
        "fee": "0.0",
        "tid": 771334864158847,
        "liquidation": {
          "liquidatedUser": "0x2e3d94f0562703b25c83308a05046ddaf9a8dd14",
          "markPx": "22.025",
          "method": "backstop"
        },
        "feeToken": "USDC"
      }
    ]
  ]
}
```

### 2. Clearinghouse Data (Snapshot)

**Source**: Hyperliquid clearinghouse state export  
**Block**: 758750000  
**Timestamp**: 2025-10-10 20:04:54.218 UTC (70 minutes before cascade)

**Components**:

#### a) Account Values Snapshot
**File**: `account_value_snapshot_758750000_1760126694218.json`  
**Size**: 68 MB  
**Records**: 437,356 accounts (snapshot baseline → 437,723 unique accounts after reconstruction)

**Structure**:
```json
[
  {
    "user": "0x5b5d51203a0f9079f8aeb098a6523a13f298c060",
    "account_value": 272726535.490442,
    "total_long_notional": 0.0,
    "total_short_notional": 0.0
  }
]
```

**What It Contains**:
- Account value (USDC) for every perp account
- Total long/short notional exposure
- Snapshot taken before the cascade started

#### b) Positions by Market Snapshot
**File**: `perp_positions_by_market_758750000_1760126694218.json`  
**Size**: 72 MB  
**Records**: 221,422 positions across 182 markets

**Structure**:
```json
[
  {
    "market_name": "hyperliquid:JUP",
    "snapshot_id": "custom_1760126694218",
    "position_count": 1774,
    "positions": [
      {
        "user": "0x002479c9acacf25b14593c2f09c503a88dc3c4ff",
        "size": -14.0,
        "notional_size": 5.63346,
        "funding_pnl": 0.035389,
        "entry_price": 0.4716,
        "is_cross": true,
        "leverage": 10,
        "liquidation_price": 71.49134890249434,
        "account_value": 1076.000069
      }
    ]
  }
]
```

**What It Contains**:
- All open positions at snapshot time
- Entry prices (from when position was opened)
- Leverage settings
- Liquidation prices
- Account value for each position holder
- Position sizes and notionals

#### c) Complete Fill History
**Files**: `20_fills.json`, `21_fills.json`  
**Size**: 407 MB + 2.0 GB  
**Records**: 5,939,266 fills total

**What It Contains**:
- Every fill from 20:00:00 to 22:00:00 UTC
- Allows tracking position changes from snapshot to cascade
- Used to calculate weighted average entry prices

#### d) Misc Events (Optional)
**Files**: `20_misc.json`, `21_misc.json`  
**Size**: 36 MB + 43 MB

**What It Contains**:
- Funding events
- Deposits/withdrawals (LedgerUpdate)
- Validator rewards
- Used for precise account value tracking (not heavily used in current analysis)

### 3. Spot Balances (Available but Not Used)
**File**: `spot_balances__758750000_1760126694218.json`  
**Size**: 150 MB

**Note**: We excluded spot positions (tickers starting with "@") from our analysis.

---

## Data Acquisition

### How to Obtain S3 Event Data

**Method 1: Direct S3 Access** (Preferred)
```bash
# Install AWS CLI
pip install awscli

# Configure (no credentials needed for public bucket)
aws configure

# Download hour 21 (main cascade)
aws s3 cp s3://hl-mainnet-node-data/node_fills_by_block/hourly/20251010/21.lz4 ./

# Download hour 20 (pre-cascade context)
aws s3 cp s3://hl-mainnet-node-data/node_fills_by_block/hourly/20251010/20.lz4 ./

# Decompress
lz4 -d 21.lz4 21.json
lz4 -d 20.lz4 20.json
```

**Method 2: Hyperliquid Node** (Advanced)
- Run a Hyperliquid node
- Export fills from local database
- More complex, not recommended for research

### How to Obtain Clearinghouse Snapshot

**Source**: Researcher-provided clearinghouse export

**Requirements**:
1. Access to Hyperliquid clearinghouse state
2. Ability to query at specific block height (758750000)
3. Export capabilities for:
   - Account values
   - Position states per market
   - Historical fills

**Why Block 758750000?**
- Timestamp: 2025-10-10 20:04:54.218 UTC
- **70 minutes before cascade** (21:15:00 UTC)
- Provides clean baseline state
- Allows tracking all position changes leading up to cascade

**Export Format**: JSON (one file per data type)

**Contact**: Clearinghouse data typically requires:
- Hyperliquid team access, OR
- Third-party analytics provider with clearinghouse access, OR
- Direct node operator with export capabilities

---

## Data Processing Pipeline

### Stage 1: Event Data Extraction

**Script**: `extract_full_12min_adl.py`

**Process**:
```python
# 1. Load and decompress S3 data
import lz4.frame
import json

with lz4.frame.open('21.lz4', 'rb') as f:
    data = json.loads(f.read())

# 2. Filter by time window
START_TIME = 1760130900000  # 21:15:00.000 UTC
END_TIME = 1760131620000    # 21:27:00.000 UTC

# 3. Extract ADL events
adl_events = []
for block in data:
    for event in block['events']:
        user, details = event
        if details['dir'] == 'Auto-Deleveraging':
            if START_TIME <= details['time'] <= END_TIME:
                adl_events.append({
                    'user': user,
                    'coin': details['coin'],
                    'price': float(details['px']),
                    'size': float(details['sz']),
                    'closed_pnl': float(details['closedPnl']),
                    'time': details['time']
                })

# 4. Extract liquidations
liquidations = []
for block in data:
    for event in block['events']:
        user, details = event
        if 'Liquidated' in details['dir']:
            if START_TIME <= details['time'] <= END_TIME:
                liquidations.append(...)
```

**Output**:
- `adl_fills_full_12min_raw.csv` - All ADL events
- `liquidations_full_12min.csv` - All liquidation events
- `adl_net_volume_full_12min.csv` - Aggregated by ticker

### Stage 2: Clearinghouse Data Loading

**Script**: `analyze_clearinghouse.py`

**Process**:
```python
import json

# 1. Load account values
with open('account_value_snapshot_758750000_1760126694218.json', 'r') as f:
    account_values = json.load(f)

account_states = {}
for acc in account_values:
    account_states[acc['user']] = {
        'account_value': acc['account_value'],
        'positions': {},
        'realized_pnl': 0.0,
        'funding_pnl': 0.0
    }

# 2. Load positions by market
with open('perp_positions_by_market_758750000_1760126694218.json', 'r') as f:
    positions_by_market = json.load(f)

# 3. Merge positions into account states
for market in positions_by_market:
    coin = market['market_name'].replace('hyperliquid:', '')
    for pos in market['positions']:
        user = pos['user']
        account_states[user]['positions'][coin] = {
            'size': pos['size'],
            'entry_price': pos['entry_price'],
            'notional': pos['notional_size'],
            'leverage': pos['leverage']
        }

# Result: Unified state at block 758750000
```

**Output**:
- Unified account states dictionary
- 437,356 accounts with complete data
- 221,422 positions mapped to accounts

### Stage 3: Real-Time Replay Preparation

**Script**: `full_analysis_realtime.py`

**Process**:
```python
# 1. Load all fills and misc events from hours 20 and 21
fills = load_all('20_fills.json', '21_fills.json')
misc = load_all('20_misc.json', '21_misc.json')

# 2. Combine and sort every event chronologically
all_events = sorted(fills + misc, key=lambda evt: evt['time'])

SNAPSHOT_TIME = 1760126694218  # 2025-10-10 20:04:54.218 UTC
CASCADE_END  = 1760131620000   # 2025-10-10 21:27:00.000 UTC

# 3. Replay only the window between snapshot and cascade end
window = [evt for evt in all_events if SNAPSHOT_TIME <= evt['time'] <= CASCADE_END]
assert len(window) == 3_239_706
```

**Output**: Chronologically ordered ledger of 3,239,706 events (fills, funding, deposits/withdrawals) ready for replay.

### Stage 4: Account State Reconstruction

**Goal**: Maintain real-time account equity, position size, and funding accrual for 437,723 accounts.

```python
accounts = bootstrap_from_snapshot('account_value_snapshot_758750000_1760126694218.json',
                                   'perp_positions_by_market_758750000_1760126694218.json')

for evt in window:
    if evt['type'] == 'fill':
        apply_fill(accounts, evt)
    elif evt['type'] == 'funding':
        apply_funding(accounts, evt)
    elif evt['type'] == 'ledger_update':
        apply_ledger_delta(accounts, evt)
    # ... other event types (deposits, withdrawals, insurance adjustments)
```

**Key details**:
- Long/short positions updated tick-by-tick using actual trade prices.
- Funding and ledger events adjust cash balance immediately.
- We track `account_value_realtime`, `total_equity`, `position_size`, and `unrealized_pnl` continuously.

### Stage 5: Canonical ADL Extraction

```python
adl_rows = []
for evt in window:
    if evt['type'] == 'adl_fill':
        state = snapshot_account_state(accounts, evt['user'])
        adl_rows.append({
            'user': evt['user'],
            'coin': evt['coin'],
            'adl_price': evt['price'],
            'adl_size': evt['size'],
            'adl_notional': abs(evt['size']) * evt['price'],
            'account_value_realtime': state.account_value,
            'total_equity': state.total_equity,
            'leverage_realtime': state.position_notional(evt['coin']) / state.total_equity,
            'is_negative_equity': state.total_equity < 0,
            'pnl_percent': state.unrealized_pnl(evt['coin']) / state.position_notional(evt['coin']) * 100,
            'seconds_from_start': (evt['time'] - SNAPSHOT_TIME) / 1000
        })
```

**Canonical Outputs**:
- `adl_detailed_analysis_REALTIME.csv` – 34,983 ADL events with real-time leverage and equity (100% coverage).
- `adl_by_user_REALTIME.csv`, `adl_by_coin_REALTIME.csv` – aggregates using real-time metrics.
- `realtime_analysis_summary.json` – replay metadata and QA checks.
- `FINDINGS_VERIFICATION_REPORT.md` – regression tests that rerun prioritization, isolation, timing, and insurance analyses on the canonical dataset.
---

## Analysis Stages

### Analysis 1: Event-Level (Nov 7-8, 2025)

**Data**: S3 fills only  
**Coverage**: 100% of events

**What We Found**:
- 98,620 total events (63,637 liquidations + 34,983 ADL)
- $7.61 billion total impact
- 171 tickers affected
- BTC, ETH, SOL = 64.4% of volume

**Documents**:
- `ADL_NET_VOLUME_FULL_12MIN.md`
- `TOTAL_IMPACT_ANALYSIS.md`

### Analysis 2: Timing & Batching (Nov 11, 2025)

**Data**: S3 fills + event sequencing  
**Coverage**: All timestamps analyzed

**What We Found**:
- ~64-second delay before first ADL
- ADL activates in bursts, not continuously
- 0.945 correlation between liquidations and ADL
- Liquidations and ADL execute in separate batches

**Documents**:
- `CASCADE_TIMING_ANALYSIS.md`
- `BATCH_PROCESSING_DISCOVERY.md`

### Analysis 3: Per-Asset Isolation (Nov 11, 2025)

**Data**: S3 fills + asset-level grouping  
**Coverage**: 100 timestamps analyzed

**What We Found**:
- Zero cross-asset ADL contagion
- BTC liquidations only trigger BTC ADL
- ETH liquidations only trigger ETH ADL
- Perfect 1:1 matching per asset

**Documents**:
- `PER_ASSET_ISOLATION.md`

### Analysis 4: Counterparty Mechanics (Nov 11, 2025)

**Data**: S3 fills + liquidation field inspection  
**Coverage**: $174M ETH ADL analyzed

**What We Found**:
- ADL events have `liquidation.liquidatedUser` field
- 265 ETH liquidations matched 1 ETH ADL
- Same timestamp, same asset
- ADL is direct counterparty mechanism

**Documents**:
- `ADL_MECHANISM_RESEARCH.md`

### Analysis 5: ADL Prioritization (Nov 12, 2025) ⭐ **BREAKTHROUGH**

**Data**: Clearinghouse snapshot + fills + event data  
**Coverage**: 31,444 ADL events with complete data (90%)
**Status**: Historical snapshot approximation (superseded by Phase 3 replay)

**What We Found**:
- **98.3% of ADL'd positions were profitable**
- Average PNL: +82.43%
- Average leverage: 1.16x (LOW - using snapshot)
- **ADL targets PROFIT, not leverage**

**Documents**:
- `ADL_PRIORITIZATION_VERIFIED.md`

**Limitation**: Used snapshot account values (70 minutes stale)

### Analysis 6: Real-Time Account Reconstruction (Nov 13, 2025) 🔥 **BREAKTHROUGH**

**Data**: Clearinghouse snapshot + full event stream (3,239,706 chronological events)  
**Coverage**: 34,983 ADL events with **real-time** account states (100%)  
**Processing**: 437,723 accounts reconstructed event-by-event

**What We Found**:
- **94.5% of ADL'd positions were profitable** (real-time)
- Average PNL: +80.58% (real-time)
- Median leverage: **0.18x** (95th pct 4.23x, 99th pct 74.18x)
- **1,147 accounts in negative equity (−$109.29M)**
- **Insurance fund impact quantified** for first time at full scale

**Technical Achievement**:
- Processed 3,239,706 events chronologically (fills, funding, deposits, withdrawals)
- Updated account values after every event (closedPnl, funding, ledger deltas)
- Calculated unrealized PNL using real-time prices per asset
- Detected negative equity and insurance fund requirements at exact ADL moments

**Documents**:
- `INSURANCE_FUND_IMPACT.md`
- `full_analysis_realtime.py` (methodology)
- `adl_detailed_analysis_REALTIME.csv` (results)

**Output Files**:
- `adl_detailed_analysis_REALTIME.csv` - 34,983 rows with real-time metrics (canonical dataset)
- `adl_by_user_REALTIME.csv` - 19,337 user-level aggregations
- `adl_by_coin_REALTIME.csv` - 162 asset-level aggregations
- `realtime_analysis_summary.json` - Key statistics
- `FINDINGS_VERIFICATION_REPORT.md` - Automated verification results

---

## Key Discoveries

### Discovery Timeline

| Discovery | Date | Method | Impact |
|-----------|------|--------|--------|
| **Full event scope** | Nov 7 | S3 data extraction | Quantified $7.6B impact |
| **Per-asset isolation** | Nov 11 | Cross-asset analysis | Debunked "ADL contagion" myth |
| **~64-second delay** | Nov 11 | Timestamp analysis | Revealed ADL threshold |
| **Batch processing** | Nov 11 | Event sequencing | Found separate execution |
| **Counterparty mechanism** | Nov 11 | Field inspection | Proved 1:1 matching |
| **PNL prioritization** | Nov 12 | Clearinghouse + fills | **Solved ADL selection** |
| **Insurance fund impact** | Nov 13 | Real-time reconstruction | **Quantified $125.98M coverage** |

### Critical Findings

**1. ADL Prioritization (Most Important)**
```
Question: How does Hyperliquid choose which profitable traders to ADL?
Answer: Targets highest PNL%, NOT highest leverage

Evidence (Real-Time Reconstruction):
- 94.5% of ADL'd positions profitable
- Average unrealized PNL: +80.58% (median +50.09%)
- Median leverage: 0.18x (95th pct 4.23x, 99th pct 74.18x)
- Top 10 ADL'd by size: ALL profitable (10-36% gains)
- Negative-equity detections explain insurance drawdowns

Implication: Low leverage does NOT protect from ADL if highly profitable
```

**2. Per-Asset Isolation**
```
Question: Can BTC liquidations trigger ETH ADL?
Answer: NO - Zero cases of cross-asset ADL found

Evidence:
- Analyzed 100 timestamps with both liquidations and ADL
- 0/100 cases of cross-asset ADL
- Perfect 1:1 matching per asset when ADL triggers

Implication: "ADL contagion" is a myth; market contagion exists but ADL is isolated
```

**3. Cascade Timing**
```
Question: When does ADL activate?
Answer: ~64-second delay, then activates in bursts

Evidence:
- First 710 events: liquidations only (0-63 seconds)
- Second 64: MASSIVE burst (22,558 events!)
- Pattern continues with alternating waves

Implication: ADL has activation threshold, not immediate
```

**4. Batch Processing**
```
Question: Do liquidations and ADL execute concurrently?
Answer: NO - Sequential batches at same timestamp

Evidence:
- Biggest burst: 11,279 liquidations → 11,279 ADL
- Zero interleaving between types
- 100% of analyzed events show this pattern

Implication: Protocol processes in phases, not mixed
```

**5. Counterparty Mechanism**
```
Question: Does ADL have corresponding liquidations?
Answer: YES - Direct 1:1 counterparty trades

Evidence:
- $174M ETH ADL ← 265 ETH liquidations (same timestamp)
- ADL fills contain liquidatedUser field
- Perfect asset matching

Implication: ADL is forced exit for winners to cover losers
```

**6. Insurance Fund Impact (NEW!) 🔥**
```
Question: How much insurance fund coverage was required?
Answer: $109.29M to cover 1,147 underwater accounts

Evidence (Real-Time Reconstruction):
- 1,147 accounts in negative equity (3.28% of ADL'd)
- Total negative equity: -$109,290,000
- Largest underwater: -$7.4M
- Average underwater: -$145k
- Peak underwater rate: 387 accounts/minute

Implication: First-ever quantification of insurance fund impact in DeFi cascade
Method: Processed 3.2M events to reconstruct account states in real-time
```

---

## Reproducibility Guide

### Prerequisites

**Software**:
```bash
# Python 3.8+
python3 --version

# Required packages
pip install pandas numpy lz4 boto3
```

**Storage**:
- ~10 GB for S3 data
- ~300 MB for clearinghouse snapshots
- ~1 GB for processed outputs

### Step-by-Step Reproduction

#### Step 1: Obtain S3 Event Data

```bash
# Create directory
mkdir -p ~/Desktop/ADL_Analysis/raw_data
cd ~/Desktop/ADL_Analysis/raw_data

# Download from S3
aws s3 cp s3://hl-mainnet-node-data/node_fills_by_block/hourly/20251010/20.lz4 ./
aws s3 cp s3://hl-mainnet-node-data/node_fills_by_block/hourly/20251010/21.lz4 ./

# Decompress
lz4 -d 20.lz4 20_fills.json
lz4 -d 21.lz4 21_fills.json
```

#### Step 2: Extract ADL Events

```bash
# Use provided script
cd ~/Desktop/"ADL Net Volume"
python3 extract_full_12min_adl.py

# Outputs:
# - adl_fills_full_12min_raw.csv
# - adl_net_volume_full_12min.csv
# - liquidations_full_12min.csv
```

#### Step 3: Obtain Clearinghouse Snapshot

**Option A**: Request from researcher
```bash
# Contact researcher who provided clearinghouse access
# Request files for block 758750000:
# - account_value_snapshot_758750000_1760126694218.json
# - perp_positions_by_market_758750000_1760126694218.json
```

**Option B**: Export from Hyperliquid node (advanced)
```bash
# Requires running Hyperliquid node
# Query at block 758750000
# Export account states and positions
```

#### Step 4: Run the Real-Time Replay

```bash
cd ~/Desktop/"ADL Clearinghouse Data"
python3 full_analysis_realtime.py \
  --fills ~/Desktop/"ADL Net Volume"/adl_fills_full_12min_raw.csv \
  --liquidations ~/Desktop/"ADL Net Volume"/liquidations_full_12min.csv \
  --snapshot account_value_snapshot_758750000_1760126694218.json \
  --positions perp_positions_by_market_758750000_1760126694218.json \
  --misc 20_misc.json 21_misc.json
```

**Outputs (canonical)**:
- `adl_detailed_analysis_REALTIME.csv`
- `adl_by_user_REALTIME.csv`
- `adl_by_coin_REALTIME.csv`
- `realtime_analysis_summary.json`
- `FINDINGS_VERIFICATION_REPORT.md`

> Legacy Phase-2 files (`adl_detailed_analysis.csv`, `adl_by_user.csv`, `adl_by_coin.csv`) are archived and should not be regenerated.

#### Step 5: Verify Canonical Metrics

```python
import pandas as pd
adl = pd.read_csv('adl_detailed_analysis_REALTIME.csv')

print(f"ADL events: {len(adl):,}")
print(f"Total ADL notional: ${adl['adl_notional'].sum():,.0f}")
print(f"Profitable positions: {(adl['pnl_percent'] > 0).sum():,}"
      f" ({(adl['pnl_percent'] > 0).mean()*100:.1f}%)")
print(f"Median leverage (real-time): {adl['leverage_realtime'].median():.2f}x")
print(f"Negative-equity accounts: {adl['is_negative_equity'].sum():,}")
```

**Expected output**
```
ADL events: 34,983
Total ADL notional: $2,103,111,431
Profitable positions: 33,064 (94.5%)
Median leverage (real-time): 0.18x
Negative-equity accounts: 1,147
```

Run `python3 ../"ADL Net Volume"/verify_all_findings.py` to regenerate the verification report covering prioritization, isolation, timing, and insurance analyses.

### Validation Checklist

- [ ] S3 data downloaded and decompressed (`20.lz4`, `21.lz4`)
- [ ] Event counts match (63,637 liquidations, 34,983 ADL)
- [ ] `full_analysis_realtime.py` replay completes (3,239,706 events processed)
- [ ] `adl_detailed_analysis_REALTIME.csv` contains 34,983 rows with real-time metrics
- [ ] Negative-equity tally equals 1,147 accounts (−$109.29M total equity)
- [ ] `verify_all_findings.py` passes all prioritization/isolation/timing/insurance checks

---

## Data Reconciliation

### Matching Accounts Across Data Sources

**Challenge**: Event data uses addresses, clearinghouse uses same addresses

**Solution**: Direct address matching
```python
# Event data
adl_event = {
    'user': '0xe92d2041199b18f611b137457f3acee8bedb22d3',
    'coin': 'AVAX',
    'price': 22.075
}

# Clearinghouse data
account_state = account_states['0xe92d2041199b18f611b137457f3acee8bedb22d3']
# Returns: {account_value: 1234.56, positions: {...}}

# Match: Same address = same account
```

### Handling Time Discrepancies

**Challenge**: Snapshot is 70 minutes before cascade

**Solution**: Track all fills between snapshot and event
```python
# Snapshot: 20:04:54.218
# ADL Event: 21:16:04.831

# Process fills in between to update positions
for fill in fills_between:
    # Update position based on fill
    # Track entry price changes
    # Account for closedPnl
```

### Dealing with Missing Data

**Phase 2 (snapshot-only)** covered 90% of ADL events because accounts opened after the 20:04 snapshot lacked balance data. The Phase 3 replay eliminates that gap by rebuilding account state between the snapshot and the cascade in real time.

| Data Point | Coverage | Canonical Source |
|------------|----------|------------------|
| Event data | 100% (34,983) | `adl_fills_full_12min_raw.csv`
| Account value / equity | 100% | `full_analysis_realtime.py` replay
| Entry price | 100% | Weighted-by-fills reconstruction during replay
| Leverage | 100% | Real-time position notional ÷ equity
| Negative equity flag | 100% | Derived from `total_equity < 0`

Historical Phase-2 CSVs (`adl_detailed_analysis.csv`, etc.) remain archived for provenance but are not used in production analyses.
### Cross-Validating Data Sources

**Method 1: User Address Overlap**
```python
# Event users
event_users = set(df_adl['user'])  # 19,337 unique users

# Snapshot users  
snapshot_users = set(account_states.keys())  # 437,356 accounts

# Overlap
overlap = len(event_users & snapshot_users)  # 19,337 (100%)

```

**Method 2: Notional Reconciliation**
```python
# From events only (S3)
total_adl_notional_s3 = $2,103,111,431

# From canonical replay
total_adl_notional_replay = $2,103,111,431

# Difference: $0
# Replay guarantees 100% coverage with consistent totals
```

**Method 3: Timestamp Validation**
```python
# All ADL events should be AFTER snapshot
assert all(adl['time'] > SNAPSHOT_TIME for adl in adl_events)

# All liquidations that triggered ADL should be AT SAME timestamp
for adl in adl_events:
    if adl.get('liquidation'):
        liquidated_user = adl['liquidation']['liquidatedUser']
        # Find corresponding liquidation
        # Should have same timestamp
```

---

## File Inventory

### Generated Outputs

**Event-Level Analysis**:
```
/Users/thebunnymac/Desktop/ADL Net Volume/
├── adl_fills_full_12min_raw.csv          # All 34,983 ADL events
├── liquidations_full_12min.csv            # All 63,637 liquidation events
├── adl_net_volume_full_12min.csv         # Aggregated by ticker (162 tickers)
├── combined_impact_by_ticker.csv         # Liquidations + ADL by ticker
└── ADL_NET_VOLUME_FULL_12MIN.md          # Full report
```

**Clearinghouse Analysis (Canonical)**:
```
/Users/thebunnymac/Desktop/ADL Clearinghouse Data/
├── adl_detailed_analysis_REALTIME.csv     # 34,983 ADL events with real-time metrics
├── adl_by_user_REALTIME.csv               # User-level aggregates (real-time)
├── adl_by_coin_REALTIME.csv               # Asset-level aggregates (real-time)
├── realtime_analysis_summary.json         # Replay scope and QA
├── CLEARINGHOUSE_ANALYSIS_SUMMARY.md      # Phase 3 methodology update
└── archive/                               # Phase-2 snapshot CSVs (historical reference only)
```

**Analysis Documents**:
```
/Users/thebunnymac/Desktop/ADL Net Volume/
├── README.md                              # Main overview
├── ADL_PRIORITIZATION_VERIFIED.md         # ⭐ ADL targets profit
├── ADL_MECHANISM_RESEARCH.md              # Counterparty mechanics
├── CASCADE_TIMING_ANALYSIS.md             # ~64-second delay
├── BATCH_PROCESSING_DISCOVERY.md          # Sequential execution
├── PER_ASSET_ISOLATION.md                 # Zero cross-asset ADL
└── TOTAL_IMPACT_ANALYSIS.md               # Combined stats
```

**Processing Scripts**:
```
/Users/thebunnymac/Desktop/ADL Net Volume/
├── extract_full_12min_adl.py              # S3 event extraction
├── prepare_data.py                        # Visualization dataset builder (canonical files)
└── calculate_total_impact.py              # Aggregate statistics

/Users/thebunnymac/Desktop/ADL Clearinghouse Data/
├── analyze_clearinghouse.py               # Snapshot bootstrap utilities
└── full_analysis_realtime.py              # Canonical real-time replay pipeline
```

---

## Common Pitfalls & Solutions

### Pitfall 1: Timestamp Format Confusion

**Problem**: S3 data uses milliseconds, clearinghouse uses nanoseconds

**Solution**:
```python
# S3 fills
fill_time = 1760130964831  # milliseconds since epoch

# Clearinghouse snapshot  
snapshot_time = 1760126694218  # milliseconds

# Convert to datetime
from datetime import datetime
dt = datetime.fromtimestamp(fill_time / 1000)  # Divide by 1000
```

### Pitfall 2: Entry Price NULL Values

**Problem**: 88% NULL in pure event data

**Solution**:
- Use clearinghouse snapshot for entry prices at snapshot time
- Calculate from fills between snapshot and event
- Accept 10% will remain NULL (opened after snapshot)

### Pitfall 3: Address Case Sensitivity

**Problem**: Addresses might have different cases

**Solution**:
```python
# Always normalize to lowercase
user_address = user_address.lower()
```

### Pitfall 4: LZ4 Decompression

**Problem**: Standard `gzip` won't work on .lz4 files

**Solution**:
```bash
# Install lz4
sudo apt-get install lz4  # Linux
brew install lz4          # Mac

# Or use Python
pip install lz4

# Then decompress
lz4 -d file.lz4 file.json
```

### Pitfall 5: Memory Issues

**Problem**: 2.7M fills won't fit in memory on some systems

**Solution**:
```python
# Process in chunks
chunk_size = 100000
for chunk in pd.read_csv('fills.csv', chunksize=chunk_size):
    # Process chunk
    process_fills(chunk)
```

---

## Future Research Directions

### With Current Data

**Completed with canonical replay**:
- [x] ADL prioritization analysis (real-time)
- [x] Leverage distribution analysis (real-time)
- [x] Entry price reconstruction across 100% of ADLs
- [x] PNL analysis at ADL time (real-time)
- [x] Negative equity quantification
- [x] Insurance fund impact measurement
- [x] Precise leverage at liquidation/ADL moment
- [x] Account value trajectory throughout the cascade

**Still open for deeper study**:
- [ ] User behavior analysis (repeat ADL targets)
- [ ] Asset-specific ADL pattern clustering
- [ ] Time-series leverage/PNL visualizations

### With Additional Data

**Requires mark price history**:
- [ ] Mark vs trade price analysis
- [ ] Unrealized PNL with official mark prices
- [ ] Liquidation price accuracy

**Requires orderbook data**:
- [ ] Market depth at critical moments
- [ ] Slippage analysis
- [ ] Price impact of liquidations

---

## Citation

If using this methodology or data:

```
Hyperliquid ADL Event Analysis (2025). "Complete Methodology: 
Anatomy of the October 10, 2025 ADL Event."

Data Sources:
- Event Data: Hyperliquid S3 (s3://hl-mainnet-node-data/)
- Clearinghouse: Snapshot at block 758750000 (2025-10-10 20:04:54 UTC)
- Analysis: 98,620 events, 437,356 accounts, 2.7M fills processed

Key Finding: ADL targets profit (94.5% profitable, avg +80.6% PNL), 
not leverage (median 0.18x leverage).

Repository: https://github.com/ConejoCapital/HyperMultiAssetedADL
```

---

## Contact & Collaboration

**For questions about**:
- Data access → Contact clearinghouse data provider
- Methodology → Review this document and analysis scripts
- Collaboration → Open to academic partnerships
- Code issues → Check GitHub repository

**Repository**: https://github.com/ConejoCapital/HyperMultiAssetedADL

---

**Document Version**: 1.1  
**Last Updated**: November 13, 2025  
**Status**: ✅ Complete and verified  
**Reproducibility**: Full (with clearinghouse access)

