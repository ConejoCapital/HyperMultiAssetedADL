# Partial Closure Verification
## Are We Correctly Accounting for ADL Amounts?

**Date**: December 7, 2025  
**Question**: Do partial closures impact total ADL'd amount? Could users have added margin that we're missing?

---

## ✅ Confirmed: We ARE Using the Correct ADL Amount

### What We Use for Total ADL'd Amount

**Source**: Raw fill data from Hyperliquid S3  
**Field Used**: `size` (the fill amount)  
**Calculation**: `notional = size * price`

**Verification**:
- ✅ Raw data total notional: **$2,103,111,430.86**
- ✅ Detailed analysis total notional: **$2,103,111,430.86**
- ✅ **Perfect match** - we're using the correct field

### Key Insight

The `size` field in the fill data is the **actual amount that was ADL'd** in that specific fill. This is the amount that was closed according to the blockchain data, regardless of whether it was a full or partial closure.

---

## Partial Closure Analysis

### Statistics

| Metric | Value |
|--------|-------|
| **Total ADL Events** | 34,983 |
| **Full Closures** | 32,413 (92.65%) |
| **Partial Closures** | 2,570 (7.35%) |
| **Total ADL Notional** | **$2,103,111,430.86** |

### What Happens in Partial Closures

**Example**:
- Position size before ADL: 100 BTC
- Amount ADL'd (fill size): 20 BTC
- Remaining position: 80 BTC

**Our Calculation**:
- ✅ We count: 20 BTC × price = notional for that ADL event
- ✅ We do NOT count: 100 BTC × price (which would be wrong)

**Result**: Partial closures are correctly handled - we only count what was actually closed.

---

## Could Users Have Added Margin/Positions?

### ✅ YES - And We Track It!

**Our Reconstruction Process**:
1. Start with snapshot at block 758750000 (20:04:54 UTC)
2. Process ALL events chronologically:
   - Fills (trades that change positions)
   - Funding events
   - Deposits/withdrawals
   - Transfers
3. Update position sizes after each fill
4. At ADL moment, `position_size` reflects the position AFTER all fills

**Example Timeline**:
```
Snapshot (20:04:54): User has 10 BTC position
Fill 1 (21:00:00): User adds 5 BTC → position = 15 BTC
Fill 2 (21:10:00): User adds 3 BTC → position = 18 BTC
ADL (21:16:04): 5 BTC ADL'd → position_size = 18 BTC, adl_size = 5 BTC
```

**Result**: ✅ We correctly capture position changes between snapshot and ADL.

---

## Verification: Are We Missing Anything?

### Scenario 1: User Adds Margin Before ADL

**Question**: If a user adds margin/position between snapshot and ADL, do we capture it?

**Answer**: ✅ YES
- We process ALL fills chronologically
- Each fill updates the position size
- `position_size` at ADL moment reflects all changes

### Scenario 2: Partial Closure Accounting

**Question**: If only part of a position is ADL'd, are we counting the full position or just the ADL'd part?

**Answer**: ✅ We count ONLY the ADL'd part
- We use `adl_size` (from fill `size` field) = actual amount closed
- We use `adl_notional = adl_size * price` = actual notional closed
- We do NOT use `position_size` for notional calculation

### Scenario 3: Multiple ADL Events for Same Position

**Question**: Could a position be partially ADL'd multiple times?

**Answer**: ✅ Possible, and we track each separately
- Each ADL fill is a separate event
- Each has its own `size` (amount closed in that fill)
- We sum all ADL fills to get total ADL'd amount

---

## Data Flow Verification

### Raw Data → Analysis

1. **Raw Fill Data** (`adl_fills_full_12min_raw.csv`):
   - `size` = amount ADL'd in this fill
   - `start_position` = position size BEFORE this fill
   - `notional = size * price` = actual notional ADL'd

2. **Reconstruction** (`full_analysis_realtime.py`):
   - Processes all fills chronologically
   - Updates `position_size` after each fill
   - At ADL moment: `position_size` = position after all previous fills

3. **Detailed Analysis** (`adl_detailed_analysis_REALTIME.csv`):
   - `adl_size` = `size` from fill (actual amount ADL'd)
   - `position_size` = position size before this ADL (from reconstruction)
   - `adl_notional = adl_size * adl_price` = actual notional ADL'd

### Verification Check

```python
# Total ADL notional calculation
total_notional = sum(adl_size * adl_price for each ADL event)
                = $2,103,111,430.86

# This matches raw data
raw_total = sum(size * price for each ADL fill)
          = $2,103,111,430.86

# ✅ Perfect match - we're using the correct amount
```

---

## Impact of Partial Closures

### What If We Used `position_size` Instead?

**Hypothetical (WRONG) Calculation**:
- Using `position_size` (position before ADL) instead of `adl_size` (amount ADL'd)
- Total would be: **$41,925,277,016.98**
- **Overcount**: $39,822,165,586.12 (1,895% error!)

**Why This Would Be Wrong**:
- For partial closures, `position_size` > `adl_size`
- We'd be counting the full position, not just what was ADL'd
- This would massively overcount the ADL'd amount

### Our Correct Calculation

**Actual (CORRECT) Calculation**:
- Using `adl_size` (actual amount ADL'd from fill)
- Total: **$2,103,111,430.86**
- This is the amount actually closed according to blockchain data

---

## Conclusion

### ✅ We ARE Correctly Accounting for ADL Amounts

1. **Source of Truth**: We use `size` from the raw fill data (from blockchain events)
2. **Partial Closures**: Correctly handled - we only count what was actually closed
3. **Position Changes**: Tracked chronologically from snapshot to ADL moment
4. **Total Notional**: Correctly calculated as sum of actual ADL'd amounts

### ✅ No Missing Data

- We process ALL fills between snapshot and ADL
- Position changes (additions, reductions) are tracked
- `position_size` reflects the position at ADL moment
- `adl_size` reflects what was actually closed

### 📊 Final Verification

| Metric | Value | Status |
|--------|-------|--------|
| **Total ADL Notional** | $2,103,111,430.86 | ✅ Correct |
| **Partial Closures** | 2,570 (7.35%) | ✅ Handled correctly |
| **Position Tracking** | Chronological from snapshot | ✅ Complete |
| **Data Source** | Raw fill `size` field | From blockchain events |

**Answer**: We have it covered. The total ADL'd amount is correctly calculated from the raw fill data's `size` field, which represents the actual amount closed in each ADL event, regardless of whether it was a full or partial closure.

