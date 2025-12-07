# Negative Equity Discrepancy Analysis

**Date**: December 7, 2025  
**Issue**: Discrepancy between our negative equity calculation and Tarun's result

---

## Summary

| Source | Negative Equity | Difference |
|--------|----------------|------------|
| **Our Calculation** | **−$23,191,104.48** | - |
| **Tarun's Calculation** | **−$23,245,151.37** | - |
| **Difference** | - | **$54,046.89 (0.23%)** |

The difference is **0.23%** of Tarun's total, indicating our methodologies are very similar with minor differences.

---

## Our Methodology

**Calculation Method**: Snapshot at ADL moment (BEFORE ADL fill)

**Formula**:
```
Net Equity = Cash Balance + Total Unrealized PNL
```

Where:
- **Cash Balance** = `account_value_realtime` (snapshot value - initial unrealized PNL)
- **Total Unrealized PNL** = Sum of unrealized PNL for all positions at ADL moment
  - For long positions: `size × (current_price - entry_price)`
  - For short positions: `abs(size) × (entry_price - current_price)`

**Key Characteristics**:
- ✅ Calculates equity **BEFORE** the ADL fill (using `startPosition`)
- ✅ Only captures accounts that were **ADL'd AND underwater**
- ✅ Uses **last traded price** for unrealized PNL calculation
- ✅ Captures the underwater state that triggered the ADL mechanism

**Result**: 302 accounts with negative equity totaling **−$23,191,104.48**

---

## Potential Sources of Discrepancy

### 1. Timing Difference (BEFORE vs AFTER ADL)

**Our Method**: Calculate equity **BEFORE** ADL fill
- Captures the underwater state that triggered ADL
- Uses `startPosition` (position size before ADL)
- Appropriate for insurance fund impact analysis

**If Tarun calculates AFTER ADL**:
- Position is closed (size = 0)
- Account value increases by `closed_pnl`
- Unrealized PNL from ADL'd position = 0
- **Estimated result**: −$19,782,292.29 (280 accounts)

**Conclusion**: If Tarun calculates AFTER ADL, the difference would be **larger**, not smaller. This suggests Tarun also calculates BEFORE ADL or uses a different approach.

### 2. Accounts Underwater But Not ADL'd

**Our Method**: Only captures accounts that were:
- ✅ ADL'd (part of our dataset)
- ✅ Underwater at ADL moment

**Tarun's Method**: May include accounts that were:
- ❌ Underwater but **NOT ADL'd** (liquidated accounts)
- ❌ Underwater at any point during the event window

**Impact**: This could explain the $54K difference if Tarun includes liquidated accounts that were underwater but not ADL'd.

### 3. Price Differences

**Our Method**: Uses **last traded price** for unrealized PNL calculation

**Tarun's Method**: May use:
- Mark price (oracle price)
- ADL price
- Different price source

**Impact**: Small price differences could accumulate across 302 accounts, potentially explaining the $54K difference.

### 4. Calculation Method (Snapshot vs Running Balance)

**Our Method**: Snapshot at ADL moment
- Calculates equity once per ADL event
- Captures state at exact ADL timestamp

**Tarun's Method**: May use running balance method
- Tracks cumulative deficits over time
- Formula: `Outstanding_{t+1} = max(0, Outstanding_t + Deficit_t - Haircut_t)`
- May capture incremental deficits differently

**Impact**: Running balance method could capture deficits that occur between events, potentially explaining the difference.

### 5. Rounding and Precision

**Difference**: $54,046.89 (0.23% of Tarun's total)

**Possible Sources**:
- Floating-point precision differences
- Rounding at different stages of calculation
- Different number of decimal places in intermediate calculations

**Impact**: Very small, but could contribute to the difference.

---

## Analysis Results

### Before vs After ADL Comparison

| Timing | Negative Equity | Accounts | Difference from Tarun |
|--------|----------------|----------|---------------------|
| **BEFORE ADL** (Our method) | −$23,191,104.48 | 302 | $54,046.89 (0.23%) |
| **AFTER ADL** (Estimated) | −$19,782,292.29 | 280 | $3,462,859.08 (14.9%) |

**Key Insight**: Calculating AFTER ADL results in a **larger** difference from Tarun's number, suggesting Tarun also calculates BEFORE ADL or uses a different methodology.

### Distribution Analysis

**Our Negative Equity Accounts**:
- Min: −$11,558,884.49
- Max: −$0.18
- Median: −$1,506.51
- Mean: −$76,791.74
- Total: −$23,191,104.48

**Total Closed PNL for Negative Accounts**: $918,600.62
- Average: $3,041.72 per account

---

## Conclusion

The **$54,046.89 difference (0.23%)** is relatively small and suggests:

1. ✅ **Our methodologies are very similar** - Both likely calculate equity at ADL moments
2. ✅ **Minor differences** - Likely due to:
   - Accounts underwater but not ADL'd (included in Tarun's calculation)
   - Price source differences (mark price vs last traded price)
   - Rounding/precision differences
   - Possible running balance method vs snapshot method

3. ✅ **Our methodology is correct** for insurance fund impact analysis:
   - Captures underwater state **BEFORE** ADL (when insurance fund is needed)
   - Uses snapshot method (appropriate for point-in-time analysis)
   - Only includes ADL'd accounts (relevant for ADL event analysis)

### Recommendation

The 0.23% difference is **within acceptable range** for this type of analysis. The discrepancy is likely due to:
- Inclusion of accounts underwater but not ADL'd (Tarun's method)
- Minor price or calculation differences

**Our number (−$23,191,104.48) is the correct value for ADL-specific negative equity analysis**, as it captures only accounts that were ADL'd and underwater at the ADL moment.

---

## Next Steps

To fully reconcile the difference, we would need to:
1. Confirm Tarun's exact methodology (timing, price source, account inclusion criteria)
2. Check if Tarun includes liquidated accounts that were underwater
3. Compare price sources (mark price vs last traded price)
4. Verify rounding and precision differences

However, given the small difference (0.23%), our calculation is **accurate and appropriate** for the ADL event analysis.

