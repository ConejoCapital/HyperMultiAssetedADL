#!/usr/bin/env python3
"""
Comprehensive ADL Event Analysis using Clearinghouse Data
Analyzes the October 10, 2025 liquidation cascade with complete account state tracking
"""

import json
import pandas as pd
from collections import defaultdict
from datetime import datetime
import sys

print("="*80)
print("HYPERLIQUID CLEARINGHOUSE ANALYSIS")
print("October 10, 2025 - Liquidation Cascade Event")
print("="*80)

# ============================================================================
# STEP 1: Load Snapshot Data (Block 758750000, 2025-10-10 20:04:54.218 UTC)
# ============================================================================

print("\n[1/8] Loading snapshot data...")

# Load account values
print("  Loading account values...")
with open('account_value_snapshot_758750000_1760126694218.json', 'r') as f:
    account_values = json.load(f)

print(f"  ✓ Loaded {len(account_values):,} accounts")

# Load perp positions by market
print("  Loading perp positions...")
with open('perp_positions_by_market_758750000_1760126694218.json', 'r') as f:
    positions_by_market = json.load(f)

print(f"  ✓ Loaded {len(positions_by_market):,} markets")

# Count total positions
total_positions = sum(market['position_count'] for market in positions_by_market)
print(f"  ✓ Total positions: {total_positions:,}")

# ============================================================================
# STEP 2: Merge into Unified Account States
# ============================================================================

print("\n[2/8] Building unified account states...")

# Create account state dictionary
# Structure: {user_address: {account_value, positions: {coin: position_data}}}
account_states = {}

# First, add all account values
for acc in account_values:
    account_states[acc['user']] = {
        'account_value': acc['account_value'],
        'total_long_notional': acc.get('total_long_notional', 0.0),
        'total_short_notional': acc.get('total_short_notional', 0.0),
        'positions': {}
    }

# Then, add all positions organized by user
for market in positions_by_market:
    coin = market['market_name'].replace('hyperliquid:', '')
    
    for pos in market['positions']:
        user = pos['user']
        
        # Create account if doesn't exist (shouldn't happen, but just in case)
        if user not in account_states:
            account_states[user] = {
                'account_value': pos['account_value'],
                'total_long_notional': 0.0,
                'total_short_notional': 0.0,
                'positions': {}
            }
        
        # Add position
        account_states[user]['positions'][coin] = {
            'size': pos['size'],
            'notional_size': pos['notional_size'],
            'funding_pnl': pos['funding_pnl'],
            'entry_price': pos['entry_price'],
            'is_cross': pos['is_cross'],
            'leverage': pos['leverage'],
            'liquidation_price': pos['liquidation_price']
        }

print(f"  ✓ Built states for {len(account_states):,} accounts")
print(f"  ✓ Accounts with positions: {sum(1 for s in account_states.values() if s['positions']):,}")

# Calculate some summary stats
total_account_value = sum(s['account_value'] for s in account_states.values())
accounts_with_positions = [s for s in account_states.values() if s['positions']]
avg_positions_per_account = sum(len(s['positions']) for s in accounts_with_positions) / len(accounts_with_positions) if accounts_with_positions else 0

print(f"\n  Summary at snapshot (20:04:54 UTC):")
print(f"    Total account value: ${total_account_value:,.0f}")
print(f"    Avg positions per active account: {avg_positions_per_account:.1f}")

# ============================================================================
# STEP 3: Load and Parse All Events
# ============================================================================

print("\n[3/8] Loading event data...")

# We need to process events chronologically across both hours
# Events structure:
# - Fills: [user, {coin, px, sz, side, time, startPosition, dir, closedPnl, ...}]
# - Misc: {time, inner: {EventType: data}}

all_events = []

print("  Loading fills from hour 20...")
with open('20_fills.json', 'r') as f:
    for line_num, line in enumerate(f):
        if line_num % 10000 == 0 and line_num > 0:
            print(f"    ...{line_num:,} blocks processed", end='\r')
        
        block = json.loads(line)
        if block.get('events'):
            for event in block['events']:
                user, details = event
                all_events.append({
                    'type': 'fill',
                    'time': details['time'],
                    'block_number': block['block_number'],
                    'block_time': block['block_time'],
                    'user': user,
                    'data': details
                })

print(f"\n  ✓ Loaded hour 20 fills")

print("  Loading fills from hour 21...")
with open('21_fills.json', 'r') as f:
    for line_num, line in enumerate(f):
        if line_num % 10000 == 0 and line_num > 0:
            print(f"    ...{line_num:,} blocks processed", end='\r')
        
        block = json.loads(line)
        if block.get('events'):
            for event in block['events']:
                user, details = event
                all_events.append({
                    'type': 'fill',
                    'time': details['time'],
                    'block_number': block['block_number'],
                    'block_time': block['block_time'],
                    'user': user,
                    'data': details
                })

print(f"\n  ✓ Loaded hour 21 fills")

print("  Loading misc events from hour 20...")
with open('20_misc.json', 'r') as f:
    for block in [json.loads(line) for line in f]:
        if block.get('events'):
            for event in block['events']:
                # Parse time from event (it's in ISO format with nanoseconds)
                # Truncate to microseconds for Python parsing
                time_str = event['time'].replace('Z', '+00:00')
                if '.' in time_str:
                    parts = time_str.split('.')
                    time_str = parts[0] + '.' + parts[1][:6] + parts[1][9:]  # Keep only 6 decimal places
                event_time = datetime.fromisoformat(time_str)
                all_events.append({
                    'type': 'misc',
                    'time': int(event_time.timestamp() * 1000),  # Convert to milliseconds
                    'block_number': block['block_number'],
                    'block_time': block['block_time'],
                    'data': event
                })

print("  ✓ Loaded hour 20 misc events")

print("  Loading misc events from hour 21...")
with open('21_misc.json', 'r') as f:
    for block in [json.loads(line) for line in f]:
        if block.get('events'):
            for event in block['events']:
                # Parse time from event (truncate nanoseconds to microseconds)
                time_str = event['time'].replace('Z', '+00:00')
                if '.' in time_str:
                    parts = time_str.split('.')
                    time_str = parts[0] + '.' + parts[1][:6] + parts[1][9:]
                event_time = datetime.fromisoformat(time_str)
                all_events.append({
                    'type': 'misc',
                    'time': int(event_time.timestamp() * 1000),
                    'block_number': block['block_number'],
                    'block_time': block['block_time'],
                    'data': event
                })

print("  ✓ Loaded hour 21 misc events")

# Sort all events by time
print("  Sorting events chronologically...")
all_events.sort(key=lambda x: x['time'])

print(f"  ✓ Total events: {len(all_events):,}")

# Filter to our analysis window: 20:04:54 to 21:27:00
SNAPSHOT_TIME = 1760126694218  # 20:04:54.218
ADL_END_TIME = 1760130960000   # 21:16:00 (end of ADL events)
ANALYSIS_END_TIME = 1760131620000  # 21:27:00

events_in_window = [e for e in all_events if SNAPSHOT_TIME <= e['time'] <= ANALYSIS_END_TIME]
print(f"  ✓ Events in analysis window: {len(events_in_window):,}")

# Count event types
fill_events = [e for e in events_in_window if e['type'] == 'fill']
misc_events = [e for e in events_in_window if e['type'] == 'misc']

print(f"    - Fill events: {len(fill_events):,}")
print(f"    - Misc events: {len(misc_events):,}")

# Count fill directions
fill_directions = defaultdict(int)
liquidations = []
adl_events = []

for e in fill_events:
    direction = e['data'].get('dir', 'Unknown')
    fill_directions[direction] += 1
    
    if direction == 'Liquidation':
        liquidations.append(e)
    elif direction == 'Auto-Deleveraging':
        adl_events.append(e)

print(f"\n  Fill types breakdown:")
for direction, count in sorted(fill_directions.items(), key=lambda x: -x[1])[:10]:
    print(f"    - {direction}: {count:,}")

print(f"\n  ✓ Found {len(liquidations):,} liquidations")
print(f"  ✓ Found {len(adl_events):,} ADL events")

print("\n[4/8] Processing events and tracking account states...")
print("  (This will take several minutes due to the large number of events)")

# Save snapshot for analysis
snapshot_data = {
    'account_states_snapshot': account_states,
    'all_events': events_in_window,
    'liquidations': liquidations,
    'adl_events': adl_events,
    'snapshot_time': SNAPSHOT_TIME,
    'analysis_window': {
        'start': SNAPSHOT_TIME,
        'end': ANALYSIS_END_TIME
    }
}

print("\n  Saving intermediate data...")
with open('clearinghouse_snapshot.json', 'w') as f:
    # We'll save a smaller version with just the counts
    json.dump({
        'snapshot_summary': {
            'total_accounts': len(account_states),
            'total_account_value': total_account_value,
            'total_positions': total_positions,
            'snapshot_time': SNAPSHOT_TIME
        },
        'event_summary': {
            'total_events': len(events_in_window),
            'fill_events': len(fill_events),
            'misc_events': len(misc_events),
            'liquidations': len(liquidations),
            'adl_events': len(adl_events)
        }
    }, f, indent=2)

print("  ✓ Intermediate data saved to clearinghouse_snapshot.json")

print("\n" + "="*80)
print("PHASE 1 COMPLETE: Data loaded and indexed")
print("="*80)
print(f"\nNext steps:")
print(f"  - Process {len(events_in_window):,} events to track account state changes")
print(f"  - Calculate entry prices from {len(fill_events):,} fills")
print(f"  - Analyze {len(liquidations):,} liquidations for negative equity")
print(f"  - Determine ADL prioritization from {len(adl_events):,} ADL events")
print(f"\nThis script will continue in the next phase...")
print("="*80)

