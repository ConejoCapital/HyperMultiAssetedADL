# Position Size Tracking Bug Fix

**Date**: December 7, 2025  
**Issue**: Position size was incorrectly set to `startPosition` instead of being updated based on fill direction

---

## Bug Description

### Original Code (WRONG)
```python
# Update position size based on fill
new_size = event['startPosition']  # startPosition is BEFORE fill, size is fill amount
working_states[user]['positions'][coin]['size'] = new_size
```

**Problem**: This sets position size to the position BEFORE the fill, not AFTER. This means:
- Position size never updates correctly
- Leverage calculations are wrong
- PNL calculations are wrong
- Entry price tracking may be wrong

### Fixed Code (CORRECT)
```python
# Update position size based on fill
# startPosition is position BEFORE fill, size is fill amount
# After fill: new_size = startPosition + size (if buy) or startPosition - size (if sell)
start_position = event['startPosition']
fill_size = event['size']
side = event.get('side', '')

if side == 'B':  # Buy - increases position
    new_size = start_position + fill_size
elif side == 'A':  # Sell - decreases position
    new_size = start_position - fill_size
else:
    # Fallback: use direction if side not available
    direction = event.get('direction', '')
    if 'Open Long' in direction or 'Close Short' in direction:
        new_size = start_position + fill_size
    elif 'Close Long' in direction or 'Open Short' in direction:
        new_size = start_position - fill_size
    else:
        # Default: assume startPosition is already the new size (for backwards compatibility)
        new_size = start_position

working_states[user]['positions'][coin]['size'] = new_size
```

---

## Impact Analysis

### What This Bug Affects

1. **Position Size Tracking**
   - ❌ Before: Position size = `startPosition` (position before fill)
   - ✅ After: Position size = `startPosition ± size` (position after fill)

2. **Leverage Calculations**
   - Formula: `leverage = abs(position_size) * price / account_value`
   - ❌ Before: Using wrong position size → wrong leverage
   - ✅ After: Using correct position size → correct leverage

3. **PNL Calculations**
   - Formula: `unrealized_pnl = position_size * (current_price - entry_price)`
   - ❌ Before: Using wrong position size → wrong PNL
   - ✅ After: Using correct position size → correct PNL

4. **Entry Price Tracking**
   - Entry price is updated when position size changes
   - ❌ Before: Position size never updates → entry price may be wrong
   - ✅ After: Position size updates correctly → entry price tracks correctly

### Files That Need Regeneration

**Canonical Data** (requires full reconstruction):
- `data/canonical/cash-only balances ADL event orderbook 2025-10-10/adl_detailed_analysis_REALTIME.csv`
  - Contains: `position_size`, `leverage_realtime`, `position_unrealized_pnl`, `pnl_percent`
- `data/canonical/cash-only balances ADL event orderbook 2025-10-10/adl_by_user_REALTIME.csv`
- `data/canonical/cash-only balances ADL event orderbook 2025-10-10/adl_by_coin_REALTIME.csv`
- `data/canonical/cash-only balances ADL event orderbook 2025-10-10/realtime_analysis_summary.json`

**Analysis Scripts** (regenerate after canonical data):
- All scripts in `scripts/analysis/` that use canonical data
- `scripts/verification/verify_all_findings.py`

**Reports** (regenerate after analysis):
- All markdown reports that reference leverage, PNL, or position metrics

---

## Regeneration Steps

### 1. Regenerate Canonical Data

**Script**: `scripts/reconstruction/full_analysis_realtime.py`

**Requirements**:
- Snapshot files: `account_value_snapshot_758750000_1760126694218.json`
- Snapshot files: `perp_positions_by_market_758750000_1760126694218.json`
- Raw fills data: `20_fills.json`, `21_fills.json` (or equivalent)

**Command**:
```bash
cd /Users/thebunnymac/Desktop/HyperMultiAssetedADL
python3 scripts/reconstruction/full_analysis_realtime.py
```

**Output**: Regenerates all canonical CSV and JSON files

### 2. Regenerate Analysis Scripts

**Scripts to run**:
```bash
python3 scripts/analysis/adl_prioritization_analysis.py
python3 scripts/analysis/adl_prioritization_local.py
python3 scripts/analysis/insurance_fund_impact.py
python3 scripts/analysis/adl_mechanism_analysis.py
python3 scripts/analysis/cascade_timing_analysis.py
python3 scripts/analysis/per_asset_isolation.py
python3 scripts/analysis/batch_processing_analysis.py
python3 scripts/analysis/adl_net_volume.py
python3 scripts/analysis/total_impact_analysis.py
```

### 3. Regenerate Verification

```bash
python3 scripts/verification/verify_all_findings.py
```

### 4. Update Reports

Check and update any markdown reports that reference:
- Leverage metrics
- PNL metrics
- Position size metrics

---

## Expected Changes

### Metrics That Will Change

1. **Leverage Ratios**
   - May increase or decrease depending on position tracking
   - Median leverage may change
   - Percentile leverage may change

2. **PNL Calculations**
   - Unrealized PNL will be more accurate
   - PNL percentages may change

3. **Position Sizes**
   - Position sizes will be correct (reflecting actual positions at ADL moment)

### Metrics That Won't Change

1. **ADL Amounts** ✅
   - Total ADL notional: Still $2,103,111,430.86
   - Uses `adl_size` (from fill data), not `position_size`

2. **Event Counts** ✅
   - Total ADL events: Still 34,983
   - Event-level metrics unchanged

3. **Account Values** ✅
   - Account value reconstruction unchanged
   - Fee subtraction unchanged

---

## Status

- ✅ **Bug Fixed**: Position size tracking corrected in `full_analysis_realtime.py`
- ⏳ **Pending**: Regeneration of canonical data (requires raw data files)
- ⏳ **Pending**: Regeneration of analysis scripts
- ⏳ **Pending**: Update of reports

---

## Notes

The bug fix is critical for accurate leverage and PNL calculations. However, the total ADL'd amount ($2.10B) is unaffected because it uses `adl_size` from the raw fill data, not the reconstructed `position_size`.

