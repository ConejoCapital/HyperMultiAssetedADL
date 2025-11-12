#!/usr/bin/env python3
"""
COMPLETE CLEARINGHOUSE ANALYSIS - Phase 2
Processes all events, tracks account states, calculates leverage, entry prices, and ADL prioritization
"""

import json
import pandas as pd
from collections import defaultdict
from datetime import datetime
import sys
from copy import deepcopy

print("="*80)
print("PHASE 2: COMPLETE EVENT PROCESSING AND ANALYSIS")
print("="*80)

# ============================================================================
# STEP 1: Load Snapshot and Events
# ============================================================================

print("\n[1/5] Loading snapshot data...")

# Load account values
with open('account_value_snapshot_758750000_1760126694218.json', 'r') as f:
    account_values = json.load(f)

# Load perp positions by market
with open('perp_positions_by_market_758750000_1760126694218.json', 'r') as f:
    positions_by_market = json.load(f)

# Build initial account states
account_states = {}
for acc in account_values:
    account_states[acc['user']] = {
        'account_value': acc['account_value'],
        'positions': {},
        'realized_pnl': 0.0,  # Track cumulative realized PNL
        'funding_pnl': 0.0    # Track cumulative funding
    }

# Add positions
for market in positions_by_market:
    coin = market['market_name'].replace('hyperliquid:', '')
    for pos in market['positions']:
        user = pos['user']
        if user not in account_states:
            account_states[user] = {
                'account_value': pos['account_value'],
                'positions': {},
                'realized_pnl': 0.0,
                'funding_pnl': 0.0
            }
        account_states[user]['positions'][coin] = {
            'size': pos['size'],
            'entry_price': pos['entry_price'],
            'notional': pos['notional_size'],
            'funding_pnl': pos['funding_pnl'],
            'is_cross': pos['is_cross'],
            'leverage': pos['leverage']
        }

print(f"  ✓ Loaded {len(account_states):,} accounts")

# ============================================================================
# STEP 2: Load ALL Events
# ============================================================================

print("\n[2/5] Loading all events (this takes 2-3 minutes)...")

SNAPSHOT_TIME = 1760126694218  # 20:04:54.218
ADL_START_TIME = 1760130903000  # Approx 21:15:03 (when ADL starts)
ADL_END_TIME = 1760131200000   # 21:20:00 (when major ADL ends)

all_fills = []

# Load fills from both hours
for hour_file in ['20_fills.json', '21_fills.json']:
    print(f"  Loading {hour_file}...")
    with open(hour_file, 'r') as f:
        for line_num, line in enumerate(f):
            block = json.loads(line)
            if block.get('events'):
                for event in block['events']:
                    user, details = event
                    all_fills.append({
                        'time': details['time'],
                        'user': user,
                        'coin': details['coin'],
                        'price': float(details['px']),
                        'size': float(details['sz']),
                        'side': details['side'],
                        'direction': details.get('dir', 'Unknown'),
                        'closedPnl': float(details.get('closedPnl', 0)),
                        'fee': float(details.get('fee', 0)),
                        'startPosition': float(details.get('startPosition', 0)),
                        'liquidation_data': details.get('liquidation', None)
                    })

print(f"  ✓ Loaded {len(all_fills):,} total fills")

# Sort by time
all_fills.sort(key=lambda x: x['time'])

# Filter to analysis window
fills_in_window = [f for f in all_fills if SNAPSHOT_TIME <= f['time'] <= ADL_END_TIME]
print(f"  ✓ Fills in window: {len(fills_in_window):,}")

# ============================================================================
# STEP 3: Identify Liquidations and ADL Events
# ============================================================================

print("\n[3/5] Identifying liquidation and ADL events...")

liquidations = []
adl_events = []

# ADL events have liquidation_data
# Liquidations are events where dir contains "Liquidated"
for fill in fills_in_window:
    direction = fill['direction']
    
    # ADL events
    if direction == 'Auto-Deleveraging':
        adl_events.append(fill)
    
    # Liquidations
    elif 'Liquidated' in direction:
        liquidations.append(fill)

print(f"  ✓ Found {len(liquidations):,} liquidation fills")
print(f"  ✓ Found {len(adl_events):,} ADL fills")

# Group by user to get unique accounts
liquidated_users = set(f['user'] for f in liquidations)
adl_users = set(f['user'] for f in adl_events)

print(f"  ✓ Unique liquidated accounts: {len(liquidated_users):,}")
print(f"  ✓ Unique ADL'd accounts: {len(adl_users):,}")

# ============================================================================
# STEP 4: Calculate Entry Prices and Positions at Critical Moments
# ============================================================================

print("\n[4/5] Calculating entry prices and account states at liquidation/ADL...")

# For each ADL event, we need to know:
# 1. Account value at the time
# 2. Position size
# 3. Entry price (calculated from fills)
# 4. Leverage
# 5. Unrealized PNL

# Track fills for entry price calculation
user_coin_fills = defaultdict(list)  # {(user, coin): [fills]}

for fill in fills_in_window:
    if fill['time'] < ADL_START_TIME:  # Only fills BEFORE ADL
        user_coin_fills[(fill['user'], fill['coin'])].append(fill)

print(f"  ✓ Tracked fills for entry price calculation")

# Calculate entry prices for ADL'd positions
adl_with_details = []

for adl in adl_events:
    user = adl['user']
    coin = adl['coin']
    
    # Get account state at snapshot
    if user not in account_states:
        continue
    
    account_state = account_states[user]
    position = account_state['positions'].get(coin, None)
    
    if not position:
        continue
    
    # Calculate entry price from fills if available
    fills_for_position = user_coin_fills.get((user, coin), [])
    
    if fills_for_position:
        # Weighted average entry price
        total_notional = 0
        total_size = 0
        for fill in fills_for_position:
            if fill['time'] < adl['time']:
                # Only consider fills that built/modified the position
                if (fill['side'] == 'B' and position['size'] > 0) or (fill['side'] == 'S' and position['size'] < 0):
                    total_notional += fill['price'] * fill['size']
                    total_size += fill['size']
        
        calculated_entry = total_notional / total_size if total_size > 0 else position['entry_price']
    else:
        calculated_entry = position['entry_price']
    
    # Calculate leverage at the time
    position_notional = abs(position['size']) * adl['price']
    leverage = position_notional / account_state['account_value'] if account_state['account_value'] > 0 else 0
    
    # Calculate PNL at ADL price
    if position['size'] > 0:  # Long position
        unrealized_pnl = position['size'] * (adl['price'] - calculated_entry)
    else:  # Short position
        unrealized_pnl = abs(position['size']) * (calculated_entry - adl['price'])
    
    pnl_percent = (unrealized_pnl / position_notional * 100) if position_notional > 0 else 0
    
    adl_with_details.append({
        'user': user,
        'coin': coin,
        'time': adl['time'],
        'adl_price': adl['price'],
        'adl_size': adl['size'],
        'adl_notional': abs(adl['size']) * adl['price'],
        'closed_pnl': adl['closedPnl'],
        'position_size': position['size'],
        'entry_price': calculated_entry,
        'account_value': account_state['account_value'],
        'leverage': leverage,
        'unrealized_pnl': unrealized_pnl,
        'pnl_percent': pnl_percent,
        'liquidated_user': adl['liquidation_data']['liquidatedUser'] if adl['liquidation_data'] else None
    })

print(f"  ✓ Calculated details for {len(adl_with_details):,} ADL events")

# ============================================================================
# STEP 5: Analyze ADL Prioritization
# ============================================================================

print("\n[5/5] Analyzing ADL prioritization criteria...")

# Convert to DataFrame for analysis
df_adl = pd.DataFrame(adl_with_details)

if len(df_adl) > 0:
    print(f"\n  ADL Statistics:")
    print(f"    Total ADL'd notional: ${df_adl['adl_notional'].sum():,.0f}")
    print(f"    Average ADL size: ${df_adl['adl_notional'].mean():,.2f}")
    print(f"    Median ADL size: ${df_adl['adl_notional'].median():,.2f}")
    print(f"    Largest ADL: ${df_adl['adl_notional'].max():,.2f}")
    
    print(f"\n  Leverage Analysis:")
    print(f"    Average leverage: {df_adl['leverage'].mean():.2f}x")
    print(f"    Median leverage: {df_adl['leverage'].median():.2f}x")
    print(f"    Max leverage: {df_adl['leverage'].max():.2f}x")
    
    print(f"\n  PNL Analysis:")
    print(f"    Average PNL%: {df_adl['pnl_percent'].mean():.2f}%")
    print(f"    Median PNL%: {df_adl['pnl_percent'].median():.2f}%")
    print(f"    Profitable positions: {(df_adl['pnl_percent'] > 0).sum():,} ({(df_adl['pnl_percent'] > 0).sum() / len(df_adl) * 100:.1f}%)")
    
    # Top 10 by PNL%
    top_pnl = df_adl.nlargest(10, 'pnl_percent')[['user', 'coin', 'pnl_percent', 'adl_notional', 'leverage']]
    print(f"\n  Top 10 ADL'd by PNL%:")
    for i, row in top_pnl.iterrows():
        print(f"    {row['coin']:6s} | {row['pnl_percent']:7.2f}% | ${row['adl_notional']:12,.0f} | {row['leverage']:.1f}x")
    
    # Top 10 by leverage
    top_lev = df_adl.nlargest(10, 'leverage')[['user', 'coin', 'leverage', 'pnl_percent', 'adl_notional']]
    print(f"\n  Top 10 ADL'd by Leverage:")
    for i, row in top_lev.iterrows():
        print(f"    {row['coin']:6s} | {row['leverage']:6.1f}x | {row['pnl_percent']:7.2f}% | ${row['adl_notional']:12,.0f}")
    
    # Top 10 by notional
    top_notional = df_adl.nlargest(10, 'adl_notional')[['user', 'coin', 'adl_notional', 'pnl_percent', 'leverage']]
    print(f"\n  Top 10 ADL'd by Notional:")
    for i, row in top_notional.iterrows():
        print(f"    {row['coin']:6s} | ${row['adl_notional']:12,.0f} | {row['pnl_percent']:7.2f}% | {row['leverage']:.1f}x")

# ============================================================================
# Save Results
# ============================================================================

print("\n" + "="*80)
print("SAVING RESULTS")
print("="*80)

# Save detailed ADL analysis
df_adl.to_csv('adl_detailed_analysis.csv', index=False)
print(f"\n  ✓ Saved adl_detailed_analysis.csv ({len(df_adl):,} records)")

# Group by user for account-level analysis
user_summary = df_adl.groupby('user').agg({
    'adl_notional': 'sum',
    'closed_pnl': 'sum',
    'leverage': 'mean',
    'pnl_percent': 'mean',
    'account_value': 'first',
    'coin': 'count'
}).rename(columns={'coin': 'num_adl_events'}).reset_index()

user_summary = user_summary.sort_values('adl_notional', ascending=False)
user_summary.to_csv('adl_by_user.csv', index=False)
print(f"  ✓ Saved adl_by_user.csv ({len(user_summary):,} users)")

# Group by coin
coin_summary = df_adl.groupby('coin').agg({
    'adl_notional': 'sum',
    'closed_pnl': 'sum',
    'leverage': 'mean',
    'pnl_percent': 'mean',
    'user': 'nunique',
    'coin': 'count'
}).rename(columns={'coin': 'num_events', 'user': 'num_users'}).reset_index()

coin_summary = coin_summary.sort_values('adl_notional', ascending=False)
coin_summary.to_csv('adl_by_coin.csv', index=False)
print(f"  ✓ Saved adl_by_coin.csv ({len(coin_summary):,} coins)")

# Save summary stats
summary = {
    'analysis_window': {
        'start': datetime.fromtimestamp(SNAPSHOT_TIME / 1000).isoformat(),
        'end': datetime.fromtimestamp(ADL_END_TIME / 1000).isoformat()
    },
    'accounts': {
        'total_in_snapshot': len(account_states),
        'liquidated': len(liquidated_users),
        'adl_affected': len(adl_users)
    },
    'events': {
        'total_fills': len(fills_in_window),
        'liquidation_fills': len(liquidations),
        'adl_fills': len(adl_events)
    },
    'adl_totals': {
        'total_notional': float(df_adl['adl_notional'].sum()),
        'total_closed_pnl': float(df_adl['closed_pnl'].sum()),
        'avg_leverage': float(df_adl['leverage'].mean()),
        'avg_pnl_percent': float(df_adl['pnl_percent'].mean()),
        'profitable_count': int((df_adl['pnl_percent'] > 0).sum())
    }
}

with open('clearinghouse_analysis_summary.json', 'w') as f:
    json.dump(summary, f, indent=2)

print(f"  ✓ Saved clearinghouse_analysis_summary.json")

print("\n" + "="*80)
print("ANALYSIS COMPLETE!")
print("="*80)
print(f"\nKey Findings:")
print(f"  • ${df_adl['adl_notional'].sum():,.0f} in ADL notional")
print(f"  • {len(adl_users):,} accounts affected by ADL")
print(f"  • {len(liquidated_users):,} accounts liquidated")
print(f"  • {(df_adl['pnl_percent'] > 0).sum():,} profitable positions ADL'd ({(df_adl['pnl_percent'] > 0).sum() / len(df_adl) * 100:.1f}%)")
print(f"  • Average leverage of ADL'd positions: {df_adl['leverage'].mean():.2f}x")
print(f"  • Average PNL% of ADL'd positions: {df_adl['pnl_percent'].mean():.2f}%")
print("\n" + "="*80)

