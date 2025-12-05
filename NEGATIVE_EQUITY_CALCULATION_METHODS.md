# Negative Equity Calculation Methods

## Overview

This document explains the difference between two methods of calculating negative equity:

1. **Snapshot Method** (Our current implementation)
2. **Running Balance Method** (Tarun's "Outstanding Negative Equity")

---

## Method 1: Snapshot Method (Our Current)

### Formula

```python
total_equity = account_value_realtime + total_unrealized_pnl
is_negative_equity = (total_equity < 0)
```

### What It Measures

- **Sum of all negative equity** at the exact moment each ADL occurs
- Each underwater account is counted once, at its ADL moment
- Does NOT account for how ADL haircuts reduce the deficit

### Current Results

- **Accounts with negative equity**: 302
- **Total negative equity**: -$23,191,104.48

### Interpretation

This represents the **total deficit across all underwater accounts** at the moment they were ADL'd. However, it doesn't account for:
- How ADL haircuts reduce the deficit
- Accounts that go underwater but aren't ADL'd
- The cumulative nature of bad debt

---

## Method 2: Running Balance Method (Tarun's)

### Formula

```
Outstanding_{t+1} = max(0, Outstanding_t + Deficit_t - Haircut_t)
```

Where:
- **Deficit_t** = negative(cash + PNL) when (cash + PNL) < 0
- **Haircut_t** = ADL notional amount that reduces the deficit
- **Outstanding_t** = running bad debt balance

### What It Measures

- **Cumulative bad debt** that accumulates over time
- Accounts for ADL haircuts that pay down the debt
- Tracks the **net outstanding balance** after all ADL haircuts

### Implementation Results

- **Final outstanding balance**: $10,479,701.90
- **Peak outstanding balance**: $11,557,364.34
- **Total deficits added**: $23,191,104.48
- **Total haircuts applied**: $2,103,111,430.86

### Interpretation

This represents the **net bad debt remaining** after accounting for ADL haircuts. The formula ensures:
- Deficits accumulate when accounts go underwater
- ADL haircuts reduce the outstanding balance
- The balance cannot go negative (overshoots are capped at zero)

---

## Key Differences

| Aspect | Snapshot Method | Running Balance Method |
|--------|----------------|----------------------|
| **What it measures** | Sum of negative equity at ADL moments | Net outstanding bad debt after haircuts |
| **Accounts for ADL haircuts** | ❌ No | ✅ Yes |
| **Cumulative tracking** | ❌ No | ✅ Yes |
| **Our result** | -$23.19M | $10.48M |
| **Tarun's result** | N/A | ~$100M |

---

## Why Tarun Gets ~$100M

Tarun's result (~$100M) is significantly higher than our running balance calculation ($10.48M). Possible reasons:

1. **Broader scope**: Tarun might be tracking negative equity for ALL accounts (not just ADL'd ones)
   - Accounts that go underwater but aren't ADL'd
   - Accounts that go underwater at different times

2. **Different definition of "cash + PNL"**:
   - Tarun might be using a different account value calculation
   - Might include/exclude certain components differently

3. **Different time window**:
   - Tarun might be tracking over a longer period
   - Might include accounts that go underwater before/after the ADL window

4. **Different ADL haircut calculation**:
   - Tarun might be calculating haircuts differently
   - Might not be applying haircuts to all deficits

---

## Our Implementation of Running Balance

We've implemented Tarun's running balance formula using our canonical data:

```python
# Sort ADL events by time
df_sorted = df.sort_values('time').copy()

outstanding_balance = 0.0

for row in df_sorted.iterrows():
    # Deficit = negative equity if account is underwater
    deficit = -row['total_equity'] if row['total_equity'] < 0 else 0.0
    
    # Haircut = ADL notional (reduces the deficit)
    haircut = row['adl_notional']
    
    # Update running balance
    outstanding_balance = max(0.0, outstanding_balance + deficit - haircut)
```

**Result**: $10.48M final outstanding balance

---

## Recommendations

1. **Clarify with Tarun**:
   - What accounts are included in his calculation?
   - What is his exact definition of "cash + PNL"?
   - What time window is he using?
   - How is he calculating ADL haircuts?

2. **Expand our analysis**:
   - Track negative equity for ALL accounts (not just ADL'd ones)
   - Track negative equity continuously (not just at ADL moments)
   - Compare with Tarun's methodology step-by-step

3. **Document both methods**:
   - Snapshot method: Useful for understanding individual account states
   - Running balance method: Useful for understanding exchange-level bad debt

---

## Files

- **Canonical data**: `cash-only balances ADL event orderbook 2025-10-10/adl_detailed_analysis_REALTIME.csv`
- **Running balance calculation**: See `analysis_scripts/outstanding_negative_equity.py` (to be created)

---

**Last Updated**: December 2025  
**Status**: Awaiting clarification from Tarun on methodology differences

