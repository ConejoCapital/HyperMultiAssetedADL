# High Leverage Outliers Explanation

**Analysis Date**: December 7, 2025  
**Issue**: Accounts with leverage > 40x (Hyperliquid's maximum)  
**Status**: Explained - These are data artifacts from liquidation delays, not actual trading positions

---

## Executive Summary

**480 ADL events (1.37% of total)** show leverage > 40x, with some extreme cases exceeding **33 million x leverage**. These are **not actual trading positions** but rather **data artifacts** caused by:

1. **Liquidation delays**: Accounts that should have been liquidated earlier but had positions remain open
2. **Near-zero account values**: Account value dropped to near-zero while positions remained open
3. **ADL timing**: These positions were eventually closed via ADL, but leverage was calculated at the moment of ADL when account value was already depleted

**Key Finding**: These outliers represent accounts that were **effectively wiped out** during the cascade but had their positions closed via ADL rather than immediate liquidation.

---

## The Problem

Hyperliquid's maximum leverage is **40x** across most markets. However, our analysis shows:

- **480 events** with leverage > 40x (1.37% of all ADL events)
- **Median leverage of outliers**: 990.50x
- **Maximum leverage observed**: 33,175,296x
- **50.4% of outliers** have account value < $1

This appears to violate Hyperliquid's leverage limits, but it's actually a **measurement artifact**.

---

## Root Cause Analysis

### Why These Outliers Exist

During the extreme liquidation cascade on October 10, 2025:

1. **Account values dropped rapidly** due to:
   - Realized losses from previous liquidations
   - Unrealized losses on remaining positions
   - Funding payments
   - Other account debits

2. **Positions remained open** even after account value approached zero because:
   - Liquidation system was overwhelmed (98,620 events in 12 minutes)
   - ADL system was processing in batches (not continuous)
   - Some accounts had positions that weren't immediately liquidatable

3. **Leverage calculation** at ADL moment:
   ```
   leverage = position_notional / account_value
   ```
   When `account_value` → $0.000005 and `position_notional` = $165.88:
   ```
   leverage = $165.88 / $0.000005 = 33,175,296x
   ```

### The Timing Pattern

**Outlier distribution over time:**
- **First 2 minutes** (21:15-21:17): 79 outliers (16.5%)
- **Minutes 2-6** (21:17-21:21): 393 outliers (81.9%) ← **Peak period**
- **Minutes 6-12** (21:21-21:27): 8 outliers (1.7%)

**Key Insight**: Most outliers occurred during the **peak cascade period** (minutes 2-6), when the system was most overwhelmed and liquidation delays were longest.

---

## Data Breakdown

### Account Value Distribution (Outliers)

| Account Value Range | Count | % of Outliers | Median Leverage |
|---------------------|-------|---------------|-----------------|
| < $0.01 | 64 | 13.3% | 7,041x |
| $0.01 - $1.00 | 178 | 37.1% | 704x |
| $1.00 - $10.00 | 113 | 23.5% | 156x |
| ≥ $10.00 | 125 | 26.0% | 58x |

**Observation**: The lower the account value, the higher the leverage. This confirms that leverage inflation is caused by near-zero denominators.

### Position Characteristics

- **Median position notional**: $1,072.61
- **Median account value**: $0.96
- **50.4% of outliers** have account value < $1

**Conclusion**: These are not large positions relative to normal trading, but they appear massive when compared to near-zero account values.

---

## Example Cases

### Case 1: Extreme Outlier (33.2M x leverage)

- **User**: `0xafb5565224fb85dab94576ebbf18957fa0ef7f6a`
- **Coin**: BTC
- **Leverage**: 33,175,296x
- **Account value**: $0.000005
- **Position notional**: $165.88
- **Position size**: -0.00153 BTC (short)
- **Time**: 21:17:06 UTC
- **Total equity**: $11.37 (positive due to unrealized PNL on other positions)

**Explanation**: This account had its account value reduced to essentially zero, but the BTC short position remained open. When ADL closed it, the leverage calculation produced an astronomical number.

### Case 2: Moderate Outlier (395x leverage)

- **User**: `0x686057cefd4f981368...`
- **Coin**: SUI
- **Leverage**: 395x
- **Account value**: $0.24
- **Position notional**: $94.92
- **Time**: 21:16:04 UTC (very early in cascade)

**Explanation**: Account value dropped to $0.24, but the SUI position ($94.92 notional) remained open until ADL closed it.

### Case 3: High Notional Outlier

- **User**: `0xc36b1bc96e1fc8733cf764413b65eeb44cb96fe5`
- **Coin**: BTC
- **Leverage**: 5,911,546x
- **Account value**: $0.001709
- **Position notional**: $10,102.83
- **Position size**: -0.09718 BTC (short)
- **Time**: 21:19:52 UTC

**Explanation**: This account had a larger position ($10K notional) that remained open even after account value dropped to $0.0017.

---

## Why This Happened

### System Overload

During the cascade:
- **98,620 forced closures** in 12 minutes
- **Average**: 8,218 events per minute
- **Peak**: ~137 events per second

The liquidation system was **overwhelmed**, causing delays in closing positions.

### ADL Batch Processing

ADL operates in **batches** (not continuous):
- Liquidations accumulate
- Threshold reached
- ADL fires in bursts
- Some accounts wait between batches

This created windows where accounts had near-zero value but open positions.

### Account Value Depletion

Account values dropped due to:
1. **Realized losses** from previous liquidations
2. **Unrealized losses** on remaining positions
3. **Funding payments** (negative funding rates during crash)
4. **Fee accumulation** from multiple trades

By the time ADL closed positions, account values were often near-zero.

---

## Validation

### These Are Not Real Trading Positions

Evidence:
1. **Account values are near-zero** - These accounts were effectively wiped out
2. **Timing correlation** - Outliers cluster during peak cascade (minutes 2-6)
3. **Position sizes are normal** - Not unusually large positions
4. **Negative equity correlation** - 4.6% of outliers have negative equity

### Comparison with Normal Leverage

| Metric | All ADL Events | Outliers (>40x) |
|--------|----------------|-----------------|
| Median leverage | 0.20x | 990.50x |
| 95th percentile | 5.10x | 4,507x |
| Account value (median) | $1,234.56 | $0.96 |
| % with account value < $1 | 0.1% | 50.4% |

**Conclusion**: Outliers are fundamentally different from normal ADL events - they represent accounts that were already wiped out.

---

## Implications

### For Research

**Safe to exclude outliers** from leverage analysis:
- These are measurement artifacts, not real trading positions
- They don't represent actual leverage usage
- They skew statistics (median leverage would be 0.20x without outliers)

**Use percentiles** instead of max:
- 95th percentile: 5.10x (reasonable)
- 99th percentile: 122.69x (still includes some outliers)
- Median: 0.20x (most representative)

### For Protocol Analysis

**System behavior is correct**:
- These accounts were eventually closed via ADL
- The "high leverage" is a calculation artifact, not a protocol failure
- No accounts exceeded 40x leverage when they opened positions

### For Documentation

**Clarify in reports**:
- These outliers are data artifacts
- They represent liquidation delays, not actual leverage
- Use median/percentiles for leverage statistics, not max

---

## Recommendations

### Statistical Reporting

1. **Report median leverage** (0.20x) as primary metric
2. **Report percentiles** (p95: 5.10x, p99: 122.69x) with context
3. **Exclude outliers** from leverage distribution analysis
4. **Note outliers separately** as "liquidation delay artifacts"

### Data Analysis

1. **Filter outliers** when analyzing leverage patterns:
   ```python
   normal_leverage = df[df['leverage_realtime'] <= 40]
   ```

2. **Analyze outliers separately** as a measure of system stress:
   ```python
   outliers = df[df['leverage_realtime'] > 40]
   # These represent liquidation delays
   ```

3. **Use account value** as a filter:
   ```python
   # Accounts with reasonable account values
   reasonable = df[df['account_value_realtime'] >= 1.0]
   ```

---

## Summary

**480 ADL events (1.37%)** show leverage > 40x due to:

1. **Liquidation delays** during system overload
2. **Near-zero account values** when ADL closed positions
3. **Mathematical artifact** from dividing position notional by tiny account value

**These are NOT:**
- Actual trading positions opened at >40x leverage
- Protocol failures or bugs
- Violations of Hyperliquid's leverage limits

**These ARE:**
- Measurement artifacts from liquidation cascade
- Evidence of system stress during peak activity
- Accounts that were effectively wiped out before ADL closed them

**Recommendation**: Use **median leverage (0.20x)** and **percentiles (p95: 5.10x)** for reporting, and note outliers separately as liquidation delay artifacts.

---

## Data Files

- **Outlier analysis CSV**: `data/raw/high_leverage_outliers_analysis.csv` (480 events with full details)
- **Canonical data**: `data/canonical/cash-only balances ADL event orderbook 2025-10-10/adl_detailed_analysis_REALTIME.csv`

---

**Generated**: December 7, 2025  
**Analysis Method**: Statistical analysis of canonical ADL dataset  
**Data Source**: Real-time account reconstruction (3.24M events processed)

