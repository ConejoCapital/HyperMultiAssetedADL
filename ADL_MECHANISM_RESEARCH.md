# ADL Mechanism Research - Empirical Evidence from October 10, 2025 Cascade

## Summary

Analysis of the $174.18M ETH Auto-Deleveraging (ADL) event using blockchain data from Hyperliquid's October 10, 2025 liquidation cascade.

## Key Finding: YES, the $174M ADL has corresponding liquidations

**ADL Event:**
- Amount: $174,176,486.12 ETH
- User: `0x2ea18c23f72a4b6172c55b411823cdc5335923f4`
- Timestamp: `2025-10-10 21:17:06.037894+00:00`
- Direction: Auto-Deleveraging
- PNL: $38,045,716.34 (profitable short forced to close)

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

## What This Tells Us About ADL

### 1. ADL is Triggered by Liquidations
- The $174M ADL happened at the EXACT same millisecond as 265 liquidations
- This is not coincidence - it's the ADL mechanism responding to liquidation demand

### 2. ADL Takes the Opposite Side
- Liquidations: LONG positions (losing money)
- ADL: SHORT position (making money)
- The profitable short was forced to close to provide liquidity for liquidating the longs

### 3. One Profitable Trader vs Many Losing Traders
- 1 ADL user (profitable short)
- 265 liquidation fills from 1 user (actually one account with many positions)
- Shows how concentrated risk can trigger ADL for winners

### 4. ADL Doesn't Cover 100%
- Only covered 85% of the liquidation notional
- Insurance/HLP fund covered the rest
- This is normal - ADL is one part of the solvency mechanism

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

### Questions Worth Investigating:

1. **ADL Prioritization**: How does Hyperliquid choose which profitable traders to ADL?
   - Likely based on PNL and position size
   - May prioritize most profitable positions first
   - Research Hyperliquid docs or ask team

2. **Partial ADL**: Why was only 85% covered by this ADL?
   - Was the short position only $174M (smaller than liquidation need)?
   - Did other ADLs cover the remaining $30M?
   - What's the HLP fund's role in the remaining gap?

3. **Cascade Effect**: How do liquidations trigger more liquidations?
   - This event shows $7.6B total impact (liquidations + ADL)
   - Multiple waves of liquidations over 12 minutes
   - Each liquidation can cause price impact → more liquidations

4. **Insurance Fund**: What's its current size and how much did it lose?
   - Hyperliquid has an insurance fund
   - May have covered some of the $30M gap
   - Check Hyperliquid documentation for fund size

## Data Availability

All raw data and analysis code available at:
- **GitHub Repository**: https://github.com/ConejoCapital/HyperMultiAssetedADL
- **Contains**:
  - Raw S3 data (98,620 events)
  - Processing scripts
  - Complete liquidation + ADL analysis
  - $7.61 billion total impact calculation

## Conclusion

**YES**, the $174.18M ETH ADL has corresponding liquidations. In fact, it has **265 corresponding liquidations** totaling $204.67M, all occurring at the exact same timestamp. This is the ADL mechanism working as designed: when massive liquidations occur, profitable traders on the opposite side are force-closed to provide liquidity.

This is not a bug or data error - it's how Hyperliquid's ADL mechanism prevents exchange insolvency during extreme market events.

---

**Data extracted:** November 11, 2025  
**Event date:** October 10, 2025, 21:17:06 UTC  
**Blockchain:** Hyperliquid L1  
**Verification:** 100% blockchain-verified data

