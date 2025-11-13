# ADL Mechanism Research - Empirical Evidence from October 10, 2025 Cascade

## Summary

Analysis of the $174.18M ETH Auto-Deleveraging (ADL) event using blockchain data from Hyperliquid's October 10, 2025 liquidation cascade.

This report has been refreshed using the canonical real-time reconstruction dataset (`adl_detailed_analysis_REALTIME.csv`, generated November 13, 2025).

## Key Finding: YES, the $174M ADL has corresponding liquidations

**ADL Event:**
- Amount: $174,176,486.12 ETH
- User: `0x2ea18c23f72a4b6172c55b411823cdc5335923f4`
- Timestamp: `2025-10-10 21:17:06.037894+00:00`
- Direction: Auto-Deleveraging
- PNL: $38,045,716.34 (profitable short forced to close)
- Real-time account value at ADL: $113,407,181.02
- Real-time total equity at ADL: $147,432,877.35
- Real-time leverage at ADL: 1.31x
- Unrealized PNL% at ADL: +21.84%

**Corresponding Liquidations:**
- **265 ETH liquidations** at the EXACT SAME TIMESTAMP
- All from user: `0xb0a55f13d22f66e6d495ac98113841b2326e9540`
- All direction: "Liquidated Cross Long" (losing long positions)
- Total liquidation amount: **$204,671,086.94**

## The ADL Mechanism in Action

### What Happened:

1. **Price Drop:** ETH crashed during the cascade
2. **Liquidations Triggered:** One user (`0xb0a5...540`) had 265 separate long positions that hit liquidation price
3. **Total Loss:** $204.67M worth of ETH longs liquidated
4. **Counterparty Needed:** To close these positions, the exchange needed to find sellers
5. **ADL Activated:** Profitable short position holder (`0x2ea1...3f4`) was force-closed via ADL
6. **Amount:** $174.18M of the liquidations were covered by this ADL

### Why Not 100% Match?

- **ADL Amount:** $174,176,486.12
- **Total Liquidations:** $204,671,086.94
- **Difference:** $30,494,600.82 (14.9%)

The remaining ~$30M was likely covered by:
- Insurance fund
- HLP fund (Hyperliquid's liquidity provider)
- Other ADL events (smaller ones not shown)
- Market makers

## Empirical Evidence

### Source Data
- **Blockchain:** Hyperliquid L1
- **Data Source:** AWS S3 bucket `s3://hl-mainnet-node-data/node_fills_by_block/`
- **File:** `hourly/20251010/21.lz4`
- **Total Events Analyzed:** 98,620 (63,637 liquidations + 34,983 ADLs)

### Transaction Details

**Liquidated User Address:**
```
0xb0a55f13d22f66e6d495ac98113841b2326e9540
```
[View on Hyperliquid Explorer](https://app.hyperliquid.xyz/explorer)

**ADL'd User Address:**
```
0x2ea18c23f72a4b6172c55b411823cdc5335923f4
```
[View on Hyperliquid Explorer](https://app.hyperliquid.xyz/explorer)

### Sample Liquidations (from the 265 total)

| Amount | Direction | PNL | Type |
|--------|-----------|-----|------|
| $26,221,120.59 | Liquidated Cross Long | -$579,836.36 | Largest single liquidation |
| $986,416.79 | Liquidated Cross Long | -$21,812.96 | |
| $874,898.88 | Liquidated Cross Long | -$19,346.93 | |
| $358,030.23 | Liquidated Cross Long | -$7,917.24 | |
| ... 261 more | ... | ... | |

All 265 occurred at timestamp: `2025-10-10 21:17:06.037894+00:00`


### Canonical Verification (November 13, 2025)
- **Data sources**: `adl_detailed_analysis_REALTIME.csv`, `adl_fills_full_12min_raw.csv`, `liquidations_full_12min.csv`
- **ADL fills at this timestamp**: 2,468 across all tickers (34,983-event canonical dataset).
- **ETH ADL fills**: 265 addresses forced to close, totaling **$204,671,086.94**, perfectly matching the ETH liquidation stack.
   - Largest ADL: `0x2ea1…3f4` with $174,176,486.12 (the case study position).
   - Remaining 264 ETH ADLs contributed the additional $30,494,600.82 needed to offset the 265 liquidations.
- **Cross-asset spillover**: 2,203 simultaneous ADLs on other tickers injected another $181,940,613.12 of liquidity at the same millisecond.
- **Insurance fund absorption**: Real-time reconstruction identified **1,275 negative-equity accounts** and **$125,981,795** of residual loss absorbed by the insurance/HLP buffers (`INSURANCE_FUND_IMPACT.md`).

## What This Tells Us About ADL

### 1. ADL is Triggered by Liquidations
- The $174M ADL happened at the EXACT same millisecond as 265 liquidations
- This is not coincidence - it's the ADL mechanism responding to liquidation demand

### 2. ADL Takes the Opposite Side
- Liquidations: LONG positions (losing money)
- ADL: SHORT position (making money)
- The profitable short was forced to close to provide liquidity for liquidating the longs

### 3. One Profitable Trader vs Many Losing Traders
- 265 ADL users (profitable shorts), including the $174M position holder
- 265 liquidation fills from a single long-only account
- Extreme concentration: one losing counterparty forced hundreds of profitable traders to close

### 4. ADL Doesn't Cover 100%
- The largest ADL supplied $174.18M (85% of the ETH liquidation stack); the remaining $30.5M came from the other 264 ETH ADLs in the same millisecond
- Any outstanding gap after ADLs was absorbed by the insurance/HLP buffers (see canonical insurance-impact analysis)
- This confirms ADL is part of a multi-layer solvency stack (ADL → insurance → socialization)

## Research Sources

### Primary Sources:
1. **Hyperliquid S3 Data**
   - `s3://hl-mainnet-node-data/node_fills_by_block/hourly/20251010/21.lz4`
   - Official blockchain data, compressed LZ4 format
   - Contains all fills, liquidations, and ADL events with nanosecond precision

2. **Hyperliquid Explorer**
   - https://app.hyperliquid.xyz/explorer
   - Can verify individual transactions and user addresses
   - Search by transaction hash or address

3. **HyperDash (Third-party Analytics)**
   - https://hyperdash.info/
   - User-friendly interface for trader history
   - Shows PNL, positions, and liquidation history

### Secondary Sources:
1. **SonarX Hyperliquid Data**
   - Provided external verification of fill data
   - 100% match with our S3 extraction (verified in `/Users/thebunnymac/Desktop/SonarX Data Verification/`)

2. **Hyperliquid Documentation**
   - https://hyperliquid.gitbook.io/
   - Official documentation (though ADL trigger mechanism not fully documented)

## Key Insights for Further Research

### Questions Worth Investigating (Updated with canonical realtime data)

1. **ADL Prioritization**: How does Hyperliquid choose which profitable traders to ADL?
   - ✅ **ANSWERED** with the realtime dataset (`adl_detailed_analysis_REALTIME.csv`)
   - **ADL targets PROFIT, not leverage**
   - 94.5% of ADL'd positions were profitable (avg +80.6% PNL)
   - Median leverage was only 0.15x (LOW!)
   - See `ADL_PRIORITIZATION_VERIFIED.md` and `FINDINGS_VERIFICATION_REPORT.md`

2. **Partial ADL Coverage**: Why was only 85% of the $204.7M liquidation stack covered by this single ETH ADL?
   - ✅ **EXPLAINED**: Canonical realtime data shows 34,983 ADLs across the burst. The remaining ~$30.5M was satisfied by follow-on ADLs in the same millisecond cluster **plus** $125,981,795 in insurance-fund absorption (quantified in `INSURANCE_FUND_IMPACT.md`).
   - Real-time equity for the forced short was $147.4M; the protocol drew only what was needed from that account while routing residual loss to other ADL counterparties and the insurance fund.

3. **Cascade Effect**: How do liquidations trigger more liquidations?
   - ✅ **VERIFIED** with the canonical 12-minute feed (`liquidations_full_12min.csv` + `adl_fills_full_12min_raw.csv`)
   - $7.61B combined impact, 61-second delay before the first ADL, alternating liquidation → ADL waves, 0.946 correlation.
   - See `CASCADE_TIMING_ANALYSIS.md`, `BATCH_PROCESSING_DISCOVERY.md`, and `TOTAL_IMPACT_ANALYSIS.md`.

4. **Insurance Fund Impact**: What's the size of the gap the fund had to absorb?
   - ✅ **MEASURED** using real-time reconstruction: 1,275 accounts in negative equity, totalling **$125,981,795** that the insurance fund (and HLP buffer) covered to prevent socialized losses.
   - Details in `INSURANCE_FUND_IMPACT.md`, `REAL_TIME_RECONSTRUCTION_SUMMARY.md`, and `LEVERAGE_CORRECTION.md`.

## Data Availability

All raw data and analysis code available at:
- **GitHub Repository**: https://github.com/ConejoCapital/HyperMultiAssetedADL
- **Contains**:
  - Raw S3 data (98,620 events)
  - Processing scripts
  - Complete liquidation + ADL analysis
  - $7.61 billion total impact calculation

**Canonical Clearinghouse Integration** (November 13, 2025 update):
- **Account snapshot**: 437,723 accounts reconstructed in real time ($5.1B total)
- **Complete event stream**: 3,239,706 fills, funding, and ledger updates processed
- **ADL analysis**: 34,983 ADL events with real-time leverage, entry prices, and equity
- **Repository files**:
  - `adl_detailed_analysis_REALTIME.csv` – Canonical per-position dataset
  - `adl_by_user_REALTIME.csv` – User-level aggregations
  - `adl_by_coin_REALTIME.csv` – Asset-level aggregations
  - `REAL_TIME_RECONSTRUCTION_SUMMARY.md` – Full methodology

## Conclusion

**YES**, the $174.18M ETH ADL has corresponding liquidations. In fact, it has **265 corresponding liquidations** totaling $204.67M, all occurring at the exact same timestamp. This is the ADL mechanism working as designed: when massive liquidations occur, profitable traders on the opposite side are force-closed to provide liquidity.

This is not a bug or data error - it's how Hyperliquid's ADL mechanism prevents exchange insolvency during extreme market events.

---

**Data extracted:** November 13, 2025  
**Event date:** October 10, 2025, 21:17:06 UTC  
**Blockchain:** Hyperliquid L1  
**Verification:** 100% blockchain-verified data

