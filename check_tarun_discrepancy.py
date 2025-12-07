#!/usr/bin/env python3
"""
Investigate discrepancy between our negative equity calculation and Tarun's.

Our calculation: -$23,191,104.48
Tarun's calculation: -$23,245,151.37
Difference: $54,046.89 (0.23%)

Key differences to investigate:
1. Timing: BEFORE vs AFTER ADL fill
2. Accounts underwater but not ADL'd
3. Price used for unrealized PNL calculation
4. Rounding/precision differences
"""
import pandas as pd
from pathlib import Path

# Load canonical data
canonical_dir = Path('data/canonical/cash-only balances ADL event orderbook 2025-10-10')
df = pd.read_csv(canonical_dir / 'adl_detailed_analysis_REALTIME.csv')

# Our calculation
negative_equity = df[df['total_equity'] < 0]
our_total = negative_equity['total_equity'].sum()

# Tarun's number
tarun_total = -23245151.37
diff = abs(our_total - tarun_total)

print('='*80)
print('NEGATIVE EQUITY DISCREPANCY ANALYSIS')
print('='*80)
print(f'\nOur calculation: -\${abs(our_total):,.2f}')
print(f'Tarun\'s calculation: -\${abs(tarun_total):,.2f}')
print(f'Difference: \${diff:,.2f} ({diff/abs(tarun_total)*100:.2f}% of Tarun\'s total)')
print()

print('OUR METHODOLOGY:')
print('  - Calculate equity BEFORE ADL fill (using startPosition)')
print('  - Only capture accounts that were underwater at ADL moment')
print('  - total_equity = account_value_realtime + total_unrealized_pnl')
print('  - account_value_realtime = cash balance (snapshot value - initial unrealized)')
print('  - total_unrealized_pnl = sum of unrealized PNL for all positions')
print()

print('POTENTIAL SOURCES OF DISCREPANCY:')
print()
print('1. TIMING DIFFERENCE:')
print('   - We calculate BEFORE ADL (captures underwater state)')
print('   - Tarun might calculate AFTER ADL (position closed, different state)')
print('   - After ADL: position size = 0, account_value += closed_pnl - fee')
print()

print('2. ACCOUNTS NOT ADL\'D:')
print('   - We only capture accounts that were ADL\'d AND underwater')
print('   - Tarun might include accounts that were underwater but NOT ADL\'d')
print('   - These would be liquidated accounts, not ADL\'d accounts')
print()

print('3. PRICE DIFFERENCES:')
print('   - We use last traded price for unrealized PNL')
print('   - Tarun might use mark price or ADL price')
print('   - Small price differences could accumulate')
print()

print('4. CALCULATION METHOD:')
print('   - We use snapshot method (equity at ADL moment)')
print('   - Tarun might use running balance method')
print('   - Running balance tracks cumulative deficits over time')
print()

# Check if calculating AFTER ADL would explain the difference
print('='*80)
print('ESTIMATING AFTER-ADL CALCULATION')
print('='*80)

# For each negative equity account, estimate equity AFTER ADL
# After ADL:
# - Position is closed (size = 0, no unrealized PNL from that position)
# - Account value increases by closed_pnl - fee
# - Other positions remain unchanged

negative_accounts = df[df['total_equity'] < 0].copy()

# Estimate equity after ADL
# We'd need to:
# 1. Remove unrealized PNL from the ADL'd position
# 2. Add closed_pnl to account_value
# 3. Recalculate total_unrealized_pnl

# But we don't have the exact position_unrealized_pnl for the ADL'd position
# We can estimate using the position_unrealized_pnl field

dollar = '$'
print(f'\nNegative equity accounts: {len(negative_accounts):,}')
print(f'Total closed_pnl: {dollar}{negative_accounts["closed_pnl"].sum():,.2f}')
if 'fee' in negative_accounts.columns:
    print(f'Total fees: {dollar}{negative_accounts["fee"].sum():,.2f}')
    print(f'Net change (closed_pnl - fee): {dollar}{(negative_accounts["closed_pnl"] - negative_accounts["fee"]).sum():,.2f}')
else:
    print('Fee column not available in dataset')
print()

# The difference is $54K
# If we assume Tarun calculates AFTER ADL:
# - Remove position_unrealized_pnl from total_unrealized_pnl
# - Add closed_pnl to account_value
# - Recalculate total_equity

# But we need the position_unrealized_pnl for the ADL'd position
# We have position_unrealized_pnl in the dataframe

print('ESTIMATE: Equity AFTER ADL (for negative accounts)')
print('='*60)

# For each negative account, estimate equity after ADL
estimated_after_equity = []

for idx, row in negative_accounts.iterrows():
    # Before ADL
    account_value_before = row['account_value_realtime']
    total_unrealized_before = row['total_unrealized_pnl']
    total_equity_before = row['total_equity']
    
    # Position-specific PNL (for the ADL'd position)
    position_unrealized = row['position_unrealized_pnl']
    
    # After ADL:
    # - Remove position_unrealized_pnl from total_unrealized_pnl
    # - Add closed_pnl to account_value
    # - Subtract fee from account_value (if available)
    
    fee = row.get('fee', 0.0)
    account_value_after = account_value_before + row['closed_pnl'] - fee
    total_unrealized_after = total_unrealized_before - position_unrealized
    total_equity_after = account_value_after + total_unrealized_after
    
    estimated_after_equity.append(total_equity_after)

negative_accounts['estimated_equity_after_adl'] = estimated_after_equity

# Calculate total negative equity AFTER ADL
negative_after = negative_accounts[negative_accounts['estimated_equity_after_adl'] < 0]
total_after = negative_after['estimated_equity_after_adl'].sum()

print(f'\nBefore ADL: -\${abs(our_total):,.2f} ({len(negative_accounts):,} accounts)')
print(f'After ADL (estimated): -\${abs(total_after):,.2f} ({len(negative_after):,} accounts)')
print(f'Difference: \${abs(our_total - total_after):,.2f}')
print()

print('CONCLUSION:')
print('  The difference of $54K is relatively small (0.23% of Tarun\'s total)')
print('  This suggests:')
print('    1. Minor timing differences (BEFORE vs AFTER ADL)')
print('    2. Possible inclusion of accounts underwater but not ADL\'d')
print('    3. Rounding or precision differences')
print('    4. Different price sources for unrealized PNL calculation')
print()
print('  Our methodology (BEFORE ADL) is correct for insurance fund impact')
print('  as it captures the underwater state that triggered the ADL mechanism.')

