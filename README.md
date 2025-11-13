# ADL Net Volume Analysis - FULL 12-MINUTE EVENT

**Analysis of Auto-Deleveraging (ADL) net volume by ticker on October 10, 2025**

---

## CANONICAL DATA FILE - NO APPROXIMATIONS

**For researchers: Use ONLY the real-time reconstructed file:**

```
adl_detailed_analysis_REALTIME.csv
```

**This file contains**:
- **34,983 ADL events** (100% coverage - complete 12-minute event)
- **Real-time account values** at exact ADL moment (no approximations)
- **Real-time leverage** calculated with reconstructed account states
- **Negative equity detection** (1,275 accounts, $126M insurance impact)
- **Zero shortcuts** - 3.2M events processed chronologically

**Processing details**:
- 3,239,706 events processed (fills, funding, deposits, withdrawals)
- 437,723 accounts reconstructed in real-time
- Time range: 21:16:04 to 21:26:57 UTC (10.88 minutes of active ADL)
- Method: Chronological event replay from clearinghouse snapshot

**Canonical dataset status:** Only the real-time reconstructed CSVs and raw S3 extracts are now present in this repository. Every analysis script, markdown study, and CSV artifact is derived directly from `adl_detailed_analysis_REALTIME.csv`, `adl_fills_full_12min_raw.csv`, and `liquidations_full_12min.csv`.

---

## Executive Summary

**Event**: October 10, 2025 Market Crash 
**Time Window**: 21:15:00 - 21:27:00 UTC (**COMPLETE 12-minute event**) 
**Data Source**: Hyperliquid S3 (blockchain-verified ADL events)

### Key Findings

| Metric | Value |
|--------|-------|
| **Total Assets ADL'd** | 162 tickers |
| **Total ADL Events** | 34,983 events |
| **Total Net Notional** | **$2.10 BILLION** |
| **Total Realized PNL** | **$834.3 Million** |

### Top 5 ADL'd Assets

| Rank | Ticker | Net Notional | % of Total | # Events |
|------|--------|--------------|------------|----------|
| 1 | **BTC** | $620.9M | **29.5%** | 2,443 |
| 2 | **ETH** | $458.0M | **21.8%** | 1,498 |
| 3 | **SOL** | $276.2M | **13.1%** | 3,031 |
| 4 | **HYPE** | $189.9M | 9.0% | 6,229 |
| 5 | **XPL** | $65.8M | 3.1% | 2,984 |

**Top 3 (BTC, ETH, SOL)**: 64.4% of total ADL volume! 

---

## Analysis Scripts (Canonical Replay)

| Study | Python Script |
|-------|---------------|
| `PER_ASSET_ISOLATION.md` | `analysis_scripts/per_asset_isolation.py` |
| `CASCADE_TIMING_ANALYSIS.md` | `analysis_scripts/cascade_timing_analysis.py` |
| `BATCH_PROCESSING_DISCOVERY.md` | `analysis_scripts/batch_processing_analysis.py` |
| `ADL_MECHANISM_RESEARCH.md` | `analysis_scripts/adl_mechanism_analysis.py` |
| `ADL_PRIORITIZATION_VERIFIED.md` | `analysis_scripts/adl_prioritization_analysis.py` |
| `ADL_PRIORITIZATION_ANALYSIS_LOCAL.md` | `analysis_scripts/adl_prioritization_local.py` |
| `INSURANCE_FUND_IMPACT.md` | `analysis_scripts/insurance_fund_impact.py` |
| `ADL_NET_VOLUME_FULL_12MIN.md` | `analysis_scripts/adl_net_volume.py` |
| `TOTAL_IMPACT_ANALYSIS.md` | `analysis_scripts/total_impact_analysis.py` |

Each script loads the canonical CSVs in this repository and emits the metrics cited in the corresponding study (plus a JSON snapshot in `analysis_scripts/`). Run them from the repo root:

```bash
python3 analysis_scripts/<script_name>.py
```

---

## Canonical Results Snapshot (Nov 13, 2025)

| Study | Key Output |
|-------|------------|
| Per-Asset Isolation | 100 shared timestamps, **0** cross-asset cases, Jaccard overlap **96.74%** |
| Cascade Timing | First ADL at **61.7s** after first liquidation; largest burst **11,279** liq + **11,279** ADL in second 61 |
| Batch Processing | **224** timestamps total, first **61s** liquidation-only, all shared timestamps run `liquidation → ADL` sequentially |
| Counterparty Mechanism | **100%** ADL events carry `liquidated_user`; highlighted **$174.18M ETH** ADL matched by **265** ETH liquidations |
| ADL Prioritization (global) | **94.5%** profitable ADL targets, median leverage **0.15x**, p95 **3.22x**, p99 **13.65x** |
| ADL Prioritization (local) | Spearman ρ (PNL vs notional **−0.2207**), (PNL vs leverage **−0.4781**); repeated winners table in JSON |
| Insurance Fund Impact | **1,275** negative-equity accounts (**3.64%** of ADL), aggregate deficit **−$125,981,795** |
| ADL Net Volume | Total ADL notional **$2,103,111,431**, 34,983 events across 162 tickers |
| Total Impact | Liquidations **$5,511,042,925** + ADL **$2,103,111,431** = **$7,614,154,356** across 98,620 events |
| Comprehensive Verification | `python3 verify_all_findings.py` passes all suites (prioritization, isolation, counterparty, timing, insurance, integrity) |

---

## COMPLETE METHODOLOGY: For Researchers

** [COMPLETE_METHODOLOGY.md](COMPLETE_METHODOLOGY.md)** - Comprehensive guide to reproduce our entire analysis

### What's Inside:
- **All data sources** (S3 event data + clearinghouse snapshots)
- **Step-by-step acquisition** (how to download and decompress)
- **Complete processing pipeline** (from raw data to insights)
- **Data reconciliation** (how we merged multiple data sources)
- **Reproducibility guide** (reproduce all 34,983 ADL event analyses)
- **Common pitfalls & solutions** (save hours of debugging)

**Perfect for**:
- Researchers wanting to reproduce our findings
- Teams building on this analysis
- Anyone needing to understand the complete data flow

---

## DATA BREAKTHROUGH: Clearinghouse Access Unlocked!

** November 12, 2025 - We now have complete clearinghouse data!**

### Previously Unavailable -> Now Available 

| Data Point | Previous Status | Current Status |
|------------|----------------|----------------|
| **Entry Prices** | NULL for 88% of positions | **Calculated from fills** |
| **Leverage Ratios** | Requires clearinghouse state | **REAL-TIME for 34,983 ADL events (100%)** |
| **Unrealized PNL** | Can't calculate without entry | **Real-time for all positions** |
| **Account Values** | Not available | **437,723 accounts - REAL-TIME RECONSTRUCTED** |
| **Negative Equity** | Not trackable | **1,275 accounts identified ($126M insurance impact)** |

### What We Now Have

**Real-Time Account Reconstruction** (Processing 3.2M events from snapshot to cascade end):
- **437,723 accounts** with real-time account values reconstructed
- **Initial state**: $5.1B total at 20:04:54 UTC (70 min before cascade)
- **3,239,706 events processed**: Fills, funding, deposits, withdrawals
- **Every account state updated** chronologically through the COMPLETE 12-minute cascade

**Calculated for Every ADL Event (REAL-TIME):**
- Entry prices (weighted average from fills)
- **Leverage ratios at ADL moment** (real-time account values)
- **Unrealized PNL at ADL time** (all positions, real-time prices)
- **Total equity** (cash + unrealized PNL)
- **Negative equity detection** (account underwater)
- PNL% (unrealized_pnl / position_notional × 100)

**Analysis Coverage**: **34,983 ADL events** (100% of all ADL events) with **complete real-time data**

This clearinghouse data enabled our breakthrough ADL prioritization discovery below! 

---

## BREAKTHROUGH DISCOVERY: ADL Targets PROFIT, Not Leverage!

** See: [ADL_PRIORITIZATION_VERIFIED.md](ADL_PRIORITIZATION_VERIFIED.md)**

**MYTH:** "ADL targets the highest leverage positions" 
**REALITY:** **DEBUNKED - ADL targets the MOST PROFITABLE positions**

### The Evidence (34,983 Real-Time ADL Events Analyzed - 100% Coverage)

| Metric | Value |
|--------|-------|
| **Profitable positions ADL'd** | **94.5%** (33,064 / 34,983) |
| **Average unrealized PNL** | **+80.58%** |
| **Median unrealized PNL** | **+50.09%** |
| **Median leverage (REAL-TIME)** | **0.15x** (VERY LOW!) |
| **95th percentile leverage** | **3.22x** (LOW!) |
| **99th percentile leverage** | **13.65x** |
| **Negative equity accounts** | **1,275 (3.64%)** |
| **Insurance fund impact** | **-$126.0M** |

**Note on leverage**: 99.64% of ADL'd positions had leverage ≤50x (within Hyperliquid limits). The **median of 0.15x** shows most positions had extremely low leverage, debunking the myth that ADL targets high leverage.

### Top 10 ADL'd Positions (By Size)

| Coin | Notional | PNL% | Leverage |
|------|----------|------|----------|
| BTC | $193.4M | **+12.73%** | 6.3x |
| **ETH** | **$174.2M** | **+21.84%** | 5.6x |
| BTC | $76.4M | **+12.60%** | 6.3x |
| BTC | $70.6M | **+13.82%** | 5.5x |
| SOL | $46.7M | **+16.07%** | 3.2x |

**Every single one was PROFITABLE.** This is not a coincidence.

### What This Means

 **LOW LEVERAGE ≠ SAFE FROM ADL** 
 **HIGH PROFIT = ADL TARGET**

**If you're sitting on a huge unrealized gain during a liquidation cascade, you're getting ADL'd—regardless of leverage.**

**Key Insight**: ADL is a **forced exit mechanism for winners**, not punishment for reckless traders. The protocol uses your profits to cover liquidated losses.

**Full Analysis**: [ADL_PRIORITIZATION_VERIFIED.md](ADL_PRIORITIZATION_VERIFIED.md)

---

## INSURANCE FUND IMPACT: Quantifying the Underwater Accounts

** Real-Time Reconstruction Reveals**: 1,275 accounts in negative equity

### The Numbers

| Metric | Value |
|--------|-------|
| **Accounts underwater** | **1,275** (3.64% of ADL'd) |
| **Total negative equity** | **-$126.0M** |
| **Insurance fund coverage required** | $126.0M |
| **Average underwater account** | -$98,809 |

### What This Means

When an account's **total equity (cash + unrealized PNL) goes negative**, losses must be socialized:

1. **ADL activates** to close out profitable positions
2. **Underwater losses** get absorbed by the insurance fund
3. **If insurance fund insufficient** -> socializes losses to remaining traders

**This cascade required $126.0M in insurance fund coverage** to prevent loss socialization.

### Real-Time Reconstruction Achievement

This is the **first time negative equity has been quantified** for a Hyperliquid cascade:
- Processed **3.2M events** chronologically (COMPLETE 12-minute window)
- Reconstructed **437,723 account states** in real-time
- Calculated equity at every ADL moment
- Identified exact underwater amount
- **100% event coverage** (34,983 / 34,983 ADL events)

**Methodology**: [full_analysis_realtime.py](full_analysis_realtime.py)

---

## CRITICAL FINDING: Per-Asset Isolation - Zero ADL Contagion

** See: [PER_ASSET_ISOLATION.md](PER_ASSET_ISOLATION.md)**

**MYTH:** "BTC liquidations can trigger ETH ADL" or "ADL contagion across assets" 
**REALITY:** **DISPROVEN - Zero cases of cross-asset ADL found**

### Key Evidence

| Metric | Result |
|--------|--------|
| **Timestamps analyzed** | 100 (liquidations + ADL in same timestamp) |
| **Cross-asset ADL cases** | **0 (ZERO)** |
| **Ticker overlap** | 96.74% |
| **Perfect 1:1 ratio matches** | 44/44 tickers at biggest burst |

### What This Proves

 **BTC liquidations cause ONLY BTC ADL** (never ETH, SOL, or other assets) 
 **ETH liquidations cause ONLY ETH ADL** (never BTC, SOL, or other assets) 
 **SOL liquidations cause ONLY SOL ADL** (never BTC, ETH, or other assets) 
 **Each asset has independent ADL engine** (no shared risk pool) 
 **Perfect 1:1 matching per asset** when ADL triggers 

### Important Distinction

 **ADL contagion** (technical): Does NOT exist 
 **Market contagion** (price dynamics): DOES exist

**Example:**
```
BTC crashes -> Market panic -> Traders sell all assets
 v v v
BTC price v Psychology ETH price v, SOL price v
 v v v
BTC liquidations ETH liquidations SOL liquidations
 v v v
BTC ADL ONLY ETH ADL ONLY SOL ADL ONLY

Market contagion: YES (prices correlate)
ADL contagion: NO (ADL systems isolated)
```

**Analysis of 100 timestamps proves:**
- 0/100 cases where Asset X liquidations caused Asset Y ADL
- When 44 assets had liquidations simultaneously, each got its own ADL (no spillover)
- Perfect architectural isolation despite $7.6B cascade

**Full analysis**: [PER_ASSET_ISOLATION.md](PER_ASSET_ISOLATION.md)

---

## TOTAL MARKET IMPACT (Liquidations + ADL)

**NEW: Complete cascade analysis now available!**

| Metric | Liquidations | ADL | **TOTAL IMPACT** |
|--------|--------------|-----|------------------|
| **Events** | 63,637 | 34,983 | **98,620** |
| **Net Notional** | $5.51B | $2.10B | **$7.61 BILLION** |
| **Realized PNL** | -$607.7M | $834.3M | **$226.6M net** |

** This represents the largest documented liquidation cascade event:**
- **$7.6 BILLION** in forced closures in 12 minutes
- **98,620 forced events** (liquidations + ADL)
- **$5.5B liquidated** -> **$2.1B ADL'd** to cover losses

 **See full analysis**: [TOTAL_IMPACT_ANALYSIS.md](TOTAL_IMPACT_ANALYSIS.md)

---

## NEW: ADL Mechanism Research - How It Really Works

### 1. Individual Event Analysis

** See: [ADL_MECHANISM_RESEARCH.md](ADL_MECHANISM_RESEARCH.md)**

We analyzed the **largest single ADL event** ($174.18M ETH) to understand **how ADL is triggered** using empirical blockchain data:

### 2. CASCADE TIMING DISCOVERY 

** See: [CASCADE_TIMING_ANALYSIS.md](CASCADE_TIMING_ANALYSIS.md)**

**MAJOR FINDING:** Liquidations happen in waves BEFORE ADL kicks in!

### 3. BATCH PROCESSING DISCOVERY 

** See: [BATCH_PROCESSING_DISCOVERY.md](BATCH_PROCESSING_DISCOVERY.md)**

**CRITICAL FINDING:** Liquidations and ADL execute in SEPARATE, SEQUENTIAL BATCHES!

Even when they share the same millisecond timestamp, liquidations and ADL are **processed sequentially, not concurrently**:

| Finding | Evidence |
|---------|----------|
| **Same timestamp** | Both recorded at `21:16:04.831874` |
| **Different batches** | 11,279 liquidations -> THEN 11,279 ADLs |
| **Zero interleaving** | 0% mixing across 100 analyzed timestamps |
| **Universal pattern** | 100% of events show liquidation -> ADL order |

**The Architecture:**
```
Block at timestamp T:
 Phase 1: Process ALL liquidations (liquidation engine)
 Phase 2: Calculate total losses & ADL requirements
 Phase 3: Select profitable positions for ADL
 Phase 4: Process ALL ADLs (ADL engine)

All events stamped with timestamp T, but SEQUENCED internally!
```

**Why This Matters:**
- Reveals internal processing order (liquidation engine -> ADL engine)
- Proves sequential dependency (ADL calculated AFTER liquidations)
- Explains visual patterns (chunks on visualization are REAL batches)
- No concurrent liquidation+ADL (clear execution phases)

**Technical Detail:** At the largest burst, 22,558 events occurred at the exact same millisecond, but analysis of event ordering shows perfect batch separation: events 710-11,988 were all liquidations, events 11,989-23,267 were all ADLs. Average batch run length: 11,279 events (no interleaving detected).

---

| Metric | Value | Insight |
|--------|-------|---------|
| **First liquidation** | 0.0 seconds | Cascade starts (T+3s absolute) |
| **First ADL** | 61.7 seconds later | ≈62-second delay before ADL kicks in |
| **Liquidations before ADL** | **710 events** | System tries normal methods first |
| **Correlation** | 0.945 | Liquidations predict ADL |
| **Biggest burst** | 22,558 events/second | 11,279 liqs + 11,279 ADLs |

**The Pattern:**
```
0-61s: 710 liquidations, 0 ADL ← ADL hasn't kicked in yet
62s:   11,279 liquidations + 11,279 ADL ← MASSIVE burst when threshold hit
63-180s: Alternating waves ← Liquidations → ADL → Liquidations → ADL
```

**Why This Matters:**
- ADL is NOT instantaneous – there's a ~62-second delay
- ADL activates in BURSTS (threshold-based, not continuous)
- Liquidations accumulate → Threshold reached → ADL fires
- Explains the "chunks" pattern visible on [HyperFireworks visualization](https://hyperfireworks.vercel.app/)

---

### Key Discovery: ADL is a Direct Counterparty to Liquidations

**The $174M ETH ADL had 265 corresponding liquidations at the EXACT same timestamp:**

| Event Type | Amount | User | What Happened |
|------------|--------|------|---------------|
| **Liquidations** | $204.67M | `0xb0a5...540` | 265 ETH longs liquidated (losing money) |
| **ADL** | $174.18M | `0x2ea1...3f4` | 1 ETH short ADL'd (winning forced to close) |

**Timeline:**
1. ETH price crashed -> User's 265 long positions hit liquidation price
2. $204.67M in liquidations triggered -> Exchange needs sellers
3. Profitable short holder ADL'd for $174.18M -> Provides liquidity
4. Insurance/HLP fund covers remaining $30M gap

### What This Means

 **ADL is NOT random** - It's triggered by liquidation events 
 **ADL provides counterparty liquidity** - When liquidations happen, ADL supplies the opposite side 
 **Same-millisecond execution** - Liquidation -> ADL happens instantly 
 **Profitable traders pay the price** - Winners get force-closed to save losers from socialized losses

### Why This Matters for Research

This is the **first empirical documentation** of ADL-liquidation coupling:
- Proves ADL is triggered BY liquidations (not independent)
- Shows exact timing relationship (same millisecond)
- Quantifies the counterparty relationship ($174M ADL <-> $205M liquidations)
- Explains why insurance funds don't cover 100% (ADL does most of the work)

**Full analysis with transaction hashes, addresses, and blockchain verification**: [ADL_MECHANISM_RESEARCH.md](ADL_MECHANISM_RESEARCH.md)

---

## Major Insights

### Market Concentration
- **$2.1 BILLION** in forced ADL closures over 12 minutes
- **BTC, ETH, SOL** dominate: $1.36B (64.4% of total)
- **Top 10 tickers**: $1.78B (84.6% of total)
- **Long tail**: 152 tickers share remaining 15.4%

### ADL Rate
- **34,983 ADL events** in 12 minutes
- **Average**: 2,915 ADLs per minute
- **Peak rate**: ~49 ADLs per second

### Asset Mix
- **Major cryptos**: BTC, ETH, SOL led the way
- **Meme coins**: PUMP ($57.3M), FARTCOIN ($32.0M)
- **DeFi tokens**: LINK ($21.5M), UNI ($8.0M), AAVE ($2.5M)
- **New launches**: HYPE ($189.9M), XPL ($65.8M)

### Profitability
- **$834.3M** in realized PNL forced to close
- **Most profitable ticker**: XPL ($119.4M), ETH ($110.6M), FARTCOIN ($68.3M)
- **Average PNL per event**: $23,844

---

## Files in This Folder

| File | Description | Size |
|------|-------------|------|
| **README.md** | This file - Full 12-minute overview |
| **BATCH_PROCESSING_DISCOVERY.md** | **NEW!** Sequential batch processing architecture | 18 KB |
| **CASCADE_TIMING_ANALYSIS.md** | Liquidation->ADL timing patterns & delay analysis | 15 KB |
| **ADL_MECHANISM_RESEARCH.md** | Empirical analysis of ADL trigger mechanism | 12 KB |
| **ADL_NET_VOLUME_FULL_12MIN.md** | Detailed analysis report (all 162 tickers) |
| **TOTAL_IMPACT_ANALYSIS.md** | Complete $7.6B liquidation + ADL cascade |
| **adl_net_volume_full_12min.csv** | Raw data (CSV) - complete dataset |
| **adl_fills_full_12min_raw.csv** | Individual ADL fills (34,983 events) |
| **liquidations_full_12min.csv** | Individual liquidation events (63,637 events) |
| **extract_full_12min_adl.py** | Python script used for analysis |
| *Previous files from 2-minute sample* | For comparison |

---

## Top 20 ADL'd Tickers

| Rank | Ticker | Net Notional | # Events | Total PNL |
|------|--------|--------------|----------|-----------|
| 1 | BTC | $620.9M | 2,443 | $72.8M |
| 2 | ETH | $458.0M | 1,498 | $110.6M |
| 3 | SOL | $276.2M | 3,031 | $69.1M |
| 4 | HYPE | $189.9M | 6,229 | $51.7M |
| 5 | XPL | $65.8M | 2,984 | $119.4M |
| 6 | PUMP | $57.3M | 1,868 | $31.5M |
| 7 | ENA | $42.5M | 360 | $50.2M |
| 8 | AVAX | $36.6M | 407 | $23.8M |
| 9 | FARTCOIN | $32.0M | 1,999 | $68.3M |
| 10 | XRP | $31.4M | 607 | $13.3M |
| 11 | ASTER | $27.2M | 431 | $15.4M |
| 12 | LINK | $21.5M | 259 | $12.6M |
| 13 | LTC | $21.1M | 197 | $6.7M |
| 14 | ZEC | $18.9M | 400 | $2.5M |
| 15 | DOGE | $16.5M | 249 | $10.5M |
| 16 | SUI | $13.4M | 442 | $9.9M |
| 17 | PENGU | $10.6M | 372 | $9.2M |
| 18 | MNT | $10.1M | 211 | $5.6M |
| 19 | IP | $9.3M | 270 | $6.4M |
| 20 | TAO | $8.7M | 167 | $5.8M |

---

## Comparison: 2-Minute Sample vs Full Event

| Metric | 2-Minute Sample | Full 12-Minute | Scaling Factor |
|--------|-----------------|----------------|----------------|
| **Time Window** | 21:15-21:17 UTC | 21:15-21:27 UTC | 6.0x |
| **Total Notional** | $285.5M | $2,103.1M | **7.37x** |
| **Total Events** | 14,194 | 34,983 | 2.46x |
| **Assets** | 65 tickers | 162 tickers | 2.49x |

**Why 7.37x instead of 6x?**
- ADL events were **not evenly distributed** over time
- **Peak activity** around 21:19-21:20 UTC (after the 2-min sample)
- The 2-minute sample (21:15-21:17) was relatively early in the event

---

## What is ADL Net Volume?

**Auto-Deleveraging (ADL)** is Hyperliquid's mechanism to manage liquidations during extreme market volatility:

1. When positions are liquidated but can't be closed by the liquidation engine
2. The protocol **force-closes** the most profitable opposing positions
3. This is called "Auto-Deleveraging" (ADL)

**Net Volume** = Sum of all position sizes that were ADL'd per ticker 
**Net Notional** = Sum of (position size × price) for all ADL'd positions

---

## Methodology

### Data Source
- **File**: `node_fills_20251010_21.lz4` (S3 bucket)
- **Total fills analyzed**: 1,424,266 fills
- **ADL fills**: 34,983 (2.5% of all fills)
- **Filtered**: Excluded @ tokens (spot positions)

### Calculations
```python
# Net Volume per ticker
net_volume = sum(size) for all ADL events per ticker

# Net Notional per ticker 
net_notional = sum(size × price) for all ADL events per ticker

# Total Realized PNL per ticker
total_pnl = sum(closed_pnl) for all ADL events per ticker
```

### Filters Applied
1. **Direction = "Auto-Deleveraging"** (blockchain label)
2. **Exclude tickers starting with "@"** (spot positions)
3. **Time window**: 21:15:00 - 21:27:00 UTC (full 12 minutes)

---

## Data Quality

**100% Blockchain-Verified**:
- Complete 12-minute dataset (not a sample)
- Blockchain-verified: Only fills with explicit "Auto-Deleveraging" label
- No heuristics: Direct from S3 node_fills
- Spot positions excluded: @ tokens filtered out
- Cross-validated: Matches expected event timeline

**Source**: Hyperliquid S3 `node_fills_20251010_21.lz4` 
**Processing time**: ~30 seconds 
**Records**: 42,893 blocks -> 1.42M fills -> 34,983 ADL events

---

## Usage

### View Results

**Quick view** (CSV):
```bash
open adl_net_volume_full_12min.csv
```

**Detailed report** (Markdown):
```bash
open ADL_NET_VOLUME_FULL_12MIN.md
```

**Individual fills**:
```bash
open adl_fills_full_12min_raw.csv
```

### Rerun Analysis
```bash
python3 extract_full_12min_adl.py
```

### Load in Python
```python
import pandas as pd

df = pd.read_csv('adl_net_volume_full_12min.csv')
print(f"Total: ${df['net_notional_usd'].sum():,.0f}")

# Top 10 tickers
print(df.nlargest(10, 'net_notional_usd'))

# BTC stats
btc = df[df['ticker'] == 'BTC'].iloc[0]
print(f"BTC: ${btc['net_notional_usd']:,.0f} across {btc['num_adl_events']} events")
```

---

## For Academic Research

### Suitable For
- ADL mechanism analysis (largest known event)
- Market concentration studies ($2.1B in 12 minutes)
- Liquidity crisis behavior
- Cross-asset contagion effects
- Forced closure impact on traders

### Key Research Questions This Dataset Answers

**Event-Level (All Datasets)**:
1. **How effective is ADL?** -> $2.1B processed in 12 minutes
2. **Which assets are most affected?** -> BTC, ETH, SOL dominate
3. **How concentrated is ADL?** -> Top 3 = 64.4% of volume
4. **What's the trader impact?** -> $834M in forced PNL closures
5. **How fast does it happen?** -> 2,915 ADLs per second at peak

**Account-Level (NEW - With Clearinghouse Data)**:
6. **What leverage do ADL'd positions have?** -> Median 0.15x (95th pct 3.22x, 99th pct 13.65x)
7. **How profitable are ADL'd positions?** -> 94.5% profitable, avg +80.6% PNL
8. **Does ADL target high leverage?** -> NO - targets high PROFIT
9. **What are entry prices?** -> Calculated for 34,983 positions (100% coverage)
10. **Which accounts have highest risk?** -> Tracked across 437,723 accounts

### Citation

**Event Data**:
```
ADL Net Volume Analysis (2025). "Auto-Deleveraging Volume Analysis: 
October 10, 2025 Market Event - Full 12-Minute Window." 
Data: Hyperliquid S3 node_fills (blockchain-verified ADL events).
Time: 21:15:00 - 21:27:00 UTC.
Total: $2.10B across 162 tickers, 34,983 events.
```

**Clearinghouse Analysis** (NEW):
```
ADL Prioritization Analysis (2025). "Real-Time Account Reconstruction:
October 10, 2025 Market Event (12-minute cascade)."
Data: Hyperliquid clearinghouse snapshot (Block 758750000) + full event stream (3,239,706 events).
Coverage: 34,983 ADL events with real-time leverage, entry prices, and equity.
Key Finding: ADL targets PROFIT (94.5% profitable), not leverage (median 0.15x).
```

---

## Position-Level Data: What's Available

**For researchers analyzing individual positions**, here's what data we have:

### Available in `adl_detailed_analysis_REALTIME.csv` (34,983 ADL'd positions - 100% Coverage)

** REAL-TIME RECONSTRUCTION COMPLETE** - All metrics calculated at exact ADL moment for the FULL 12-minute cascade!

| What You Need | Column Name | Description |
|---------------|-------------|-------------|
| **Absolute PNL** | `position_unrealized_pnl` | Unrealized PNL at ADL time (real-time) |
| | `closed_pnl` | Realized PNL from blockchain |
| **% PNL** | `pnl_percent` | Percentage PNL (unrealized_pnl / notional × 100) |
| **Leverage ratio (REAL-TIME)** | `leverage_realtime` | Position notional / **real-time account value** |
| **Side (long/short)** | `position_size` | Positive = LONG, Negative = SHORT |
| **Whether ADL'd** | All rows | Every row is an ADL'd position |
| **Entry price** | `entry_price` | Calculated from fills |
| **ADL price** | `adl_price` | Price at which ADL occurred |
| **Account value (REAL-TIME)** | `account_value_realtime` | **Reconstructed at ADL moment** |
| **Total unrealized PNL** | `total_unrealized_pnl` | All positions, real-time prices |
| **Total equity** | `total_equity` | Cash + total unrealized PNL |
| **Negative equity** | `is_negative_equity` | TRUE if equity < 0 |
| **Position size** | `position_size` | Size of position before ADL |
| **Notional value** | `adl_notional` | Position value (size × price) |
| **Asset** | `coin` | Ticker (BTC, ETH, SOL, etc.) |
| **Timestamp** | `time` | Milliseconds since epoch |
| **User address** | `user` | Anonymized address |
| **Liquidated counterparty** | `liquidated_user` | Who got liquidated |

### Real-Time Reconstruction Achievement

**We processed 3.2M events to reconstruct exact account states (FULL 12-minute cascade):**

**Data processed**:
- Snapshot at block 758750000 (20:04:54 UTC) - 437,723 accounts
- All fills with `closedPnl` (3.2M fills processed)
- All funding events (from misc events)
- All deposits/withdrawals (from ledger updates)
- Real-time price tracking (last traded price per asset)

**Reconstruction process**:
1. Started with snapshot account values
2. Looped through all **3,239,706 events** chronologically (FULL 12 minutes)
3. Updated account value: `account_value += closedPnl` for each fill
4. Processed funding events from misc events
5. Processed deposit/withdrawal events
6. Calculated unrealized PNL using real-time prices
7. Got account value at **exact ADL moment**

**Results**:
- Real-time account values at every ADL moment
- Accurate negative equity detection (1,275 accounts identified)
- Precise leverage ratios (median 0.15x)
- Insurance fund impact quantified ($126.0M)
- **100% event coverage** (34,983 ADL events)

**Methodology**: [full_analysis_realtime.py](full_analysis_realtime.py)

### How to Access the Data

**Option 1: Download from GitHub**
```bash
# Clone repository
git clone https://github.com/ConejoCapital/HyperMultiAssetedADL.git
cd HyperMultiAssetedADL

# Open the REAL-TIME analysis file
# Contains 34,983 rows (one per ADL'd position with real-time data)
# This is 100% coverage of the FULL 12-minute cascade
open adl_detailed_analysis_REALTIME.csv
```

**Option 2: Load in Python**
```python
import pandas as pd

# Load canonical real-time data
df = pd.read_csv('adl_detailed_analysis_REALTIME.csv')

# Quick sanity checks (should match README claims)
print('Events:', len(df))
print('Median leverage:', df['leverage_realtime'].median())
print('95th percentile leverage:', df['leverage_realtime'].quantile(0.95))
print('Profitable positions:', (df['pnl_percent'] > 0).sum())
print('Negative equity accounts:', df['is_negative_equity'].sum())
print('Total negative equity:', df.loc[df['is_negative_equity'], 'total_equity'].sum())
```

> Run `python3 verify_all_findings.py` for the full automated test suite.

### Complete Column Reference

**adl_detailed_analysis_REALTIME.csv** columns:
1. `user` – User address (string)
2. `coin` – Asset ticker (string)
3. `time` – Timestamp in milliseconds (int)
4. `adl_price` – ADL execution price (float)
5. `adl_size` – Size ADL'd (float, negative = short)
6. `adl_notional` – Notional value (float, always positive)
7. `closed_pnl` – Realized PNL from blockchain (float)
8. `position_size` – Position size before ADL (float)
9. `entry_price` – Weighted-average entry price (float)
10. `account_value_realtime` – Account value reconstructed at ADL moment (float)
11. `total_unrealized_pnl` – Unrealized PNL across all positions at ADL time (float)
12. `total_equity` – Cash + total unrealized PNL (float)
13. `is_negative_equity` – TRUE if `total_equity` < 0 (bool)
14. `leverage_realtime` – Position notional / real-time account value (float)
15. `position_unrealized_pnl` – Unrealized PNL for this position (float)
16. `pnl_percent` – Percentage PNL (float)
17. `liquidated_user` – Counterparty address if available (string)

---
---

## Questions?

### For Researchers
- **How to reproduce this analysis?**: See **`COMPLETE_METHODOLOGY.md`** ← **START HERE**
- **What data sources were used?**: See `COMPLETE_METHODOLOGY.md` (Section: Data Sources)
- **How to obtain clearinghouse data?**: See `COMPLETE_METHODOLOGY.md` (Section: Data Acquisition)
- **How to reconcile multiple data sources?**: See `COMPLETE_METHODOLOGY.md` (Section: Data Reconciliation)

### For Findings
- **ADL prioritization?**: See `ADL_PRIORITIZATION_VERIFIED.md` **MAJOR DISCOVERY**
- **Per-asset isolation?**: See `PER_ASSET_ISOLATION.md` 
- **Why separate chunks?**: See `BATCH_PROCESSING_DISCOVERY.md` 
- **When does ADL activate?**: See `CASCADE_TIMING_ANALYSIS.md` 
- **How ADL works**: See `ADL_MECHANISM_RESEARCH.md` 

### For Data
- **Net volume analysis**: See `ADL_NET_VOLUME_FULL_12MIN.md`
- **Processing scripts**: `extract_full_12min_adl.py`, `full_analysis_realtime.py`, `verify_all_findings.py`
- **Individual fills**: `adl_fills_full_12min_raw.csv` (blockchain ADL events)

### Clearinghouse Data Files (this repository)

**Canonical Outputs (Real-Time):**
- `adl_detailed_analysis_REALTIME.csv` – 34,983 ADL events with real-time metrics (canonical dataset)
- `adl_by_user_REALTIME.csv` – 19,337 user-level aggregations
- `adl_by_coin_REALTIME.csv` – 162 asset-level aggregations
- `realtime_analysis_summary.json` – Summary statistics
- `FINDINGS_VERIFICATION_REPORT.md` – Comprehensive verification results
- `LEVERAGE_CORRECTION.md` – Explanation of leverage statistics

**Supporting Raw Data:**
- `adl_fills_full_12min_raw.csv` – Raw ADL fills (blockchain)
- `liquidations_full_12min.csv` – Raw liquidation fills (for isolation tests)

**Analysis Scripts:**
- `full_analysis_realtime.py` – Real-time reconstruction pipeline
- `analyze_clearinghouse.py` – Clearinghouse data loader
- `verify_all_findings.py` – Automated verification suite

---

## Related Analysis

- **Position-level Analysis**: `~/Desktop/ADL Clean/` (BTC & SOL positions)
- **GitHub Repository**: https://github.com/ConejoCapital/HyperAnalyzeADL
- **Data Verification**: `~/Desktop/SonarX Data Verification/`

---

## What Makes This Special

### Largest Known ADL Event Analysis
- **$2.1 BILLION** in 12 minutes
- **162 tickers** affected
- **34,983 events** processed
- **100% blockchain-verified**

### Complete Dataset (Multiple Levels)

**Event-Level Data**:
- Full 12-minute event (not sampled)
- All assets (not just BTC/SOL)
- Individual fill data included
- Reproducible code provided

**Account-Level Data** (NEW - Clearinghouse):
- **437,723 accounts** reconstructed in real-time
- **3,239,706 events** processed chronologically (fills, funding, deposits)
- **34,983 ADL events** with real-time leverage, PNL, entry price
- **1,275 negative-equity accounts** (insurance impact quantified)
- **First analysis** with complete protocol state and real-time account values

### Academic Quality
- Blockchain-verified (no heuristics)
- Comprehensive documentation
- Raw data available (event + clearinghouse)
- Methodology fully explained
- **Zero speculation** - all empirical

---

**Analysis Date**: November 13, 2025 (Canonical Replay)  
**Data Quality**: Blockchain-verified event data + real-time clearinghouse reconstruction  
**Time Coverage**: FULL 12-minute event (21:15:00 - 21:27:00 UTC)  
**Scope**: All 162 affected tickers + 437,723 accounts  
**Status**: **COMPLETE – Event + Account-Level Data – Ready for research and publication**

