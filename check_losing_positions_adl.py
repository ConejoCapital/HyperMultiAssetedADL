#!/usr/bin/env python3
"""Check if losing positions (liquidated users) are also labeled as ADL."""
import json
import lz4.frame
from pathlib import Path
from collections import defaultdict

# Find the raw S3 data file
ROOT = Path(__file__).resolve().parent
DESKTOP = ROOT.parent  # /Users/thebunnymac/Desktop

possible_paths = [
    DESKTOP / "ADL Clean" / "s3_raw_data" / "node_fills_20251010_21.lz4",
    DESKTOP / "@hyperliquid ADL Tool" / "s3_raw_data" / "node_fills_20251010_21.lz4",
    DESKTOP / "ADL Clearinghouse Data" / "node_fills_20251010_21.lz4",
]

S3_DATA_FILE = None
for path in possible_paths:
    if path.exists():
        S3_DATA_FILE = path
        print(f"✅ Found raw data: {path}")
        break

if not S3_DATA_FILE:
    print("❌ Could not find raw data file")
    print("Tried:")
    for p in possible_paths:
        print(f"  - {p}")
    exit(1)

print("="*80)
print("CHECKING: Are losing positions also labeled as ADL?")
print("="*80)
print(f"\nLoading raw data from: {S3_DATA_FILE}")
print("This may take a few minutes...\n")

# Track ADL events
adl_events = []
all_fills_with_liquidation = []

# Time window
from datetime import datetime, timezone
ADL_START = datetime(2025, 10, 10, 21, 15, 0, tzinfo=timezone.utc)
ADL_END = datetime(2025, 10, 10, 21, 27, 0, tzinfo=timezone.utc)

print("Processing raw fills...")
line_count = 0
adl_count = 0

with lz4.frame.open(S3_DATA_FILE, 'rb') as f:
    for line_num, line in enumerate(f, 1):
        line_count += 1
        if line_count % 100000 == 0:
            print(f"  Processed {line_count:,} lines, found {adl_count:,} ADL events...", end='\r')
        
        try:
            data = json.loads(line)
            
            # Get block time
            block_time_str = data.get('block_time', '')
            if not block_time_str:
                continue
            
            # Parse timestamp
            if '.' in block_time_str:
                base, frac = block_time_str.rsplit('.', 1)
                frac_truncated = frac[:6].ljust(6, '0')
                block_time_str = f"{base}.{frac_truncated}"
            
            block_time = datetime.fromisoformat(block_time_str)
            if block_time.tzinfo is None:
                block_time = block_time.replace(tzinfo=timezone.utc)
            
            # Filter to time window
            if block_time < ADL_START or block_time >= ADL_END:
                continue
            
            # Process events
            events = data.get('events', [])
            
            for event in events:
                if not isinstance(event, list) or len(event) < 2:
                    continue
                
                user = event[0]
                fill = event[1]
                
                # Check if this is an ADL event
                direction = fill.get('dir', '')
                
                if 'Auto-Deleveraging' not in direction:
                    continue
                
                adl_count += 1
                
                # Check for liquidation data
                liquidation_data = fill.get('liquidation', None)
                liquidated_user = None
                
                if liquidation_data:
                    if isinstance(liquidation_data, dict):
                        liquidated_user = liquidation_data.get('liquidatedUser') or liquidation_data.get('liquidated_user')
                    elif isinstance(liquidation_data, str):
                        liquidated_user = liquidation_data
                
                # Also check if there's a direct field
                if not liquidated_user:
                    liquidated_user = fill.get('liquidatedUser') or fill.get('liquidated_user')
                
                coin = fill.get('coin', '')
                if coin.startswith('@'):
                    continue
                
                adl_events.append({
                    'user': user,
                    'coin': coin,
                    'direction': direction,
                    'liquidated_user': liquidated_user,
                    'liquidation_data': liquidation_data,
                    'is_losing': user == liquidated_user if liquidated_user else None,
                    'closed_pnl': float(fill.get('closedPnl', 0)),
                    'size': float(fill.get('sz', 0)),
                    'price': float(fill.get('px', 0)),
                })
                
                # Also check all fills for liquidation info
                if liquidation_data or liquidated_user:
                    all_fills_with_liquidation.append({
                        'user': user,
                        'direction': direction,
                        'has_liquidation_data': liquidation_data is not None,
                        'liquidated_user': liquidated_user,
                    })
        
        except Exception as e:
            if line_num < 10:
                print(f"  Warning: Error on line {line_num}: {e}")
            continue

print(f"\n\n✅ Processing complete!")
print(f"  Total lines processed: {line_count:,}")
print(f"  ADL events found: {len(adl_events):,}")

print("\n" + "="*80)
print("ANALYSIS: Are losing positions labeled as ADL?")
print("="*80)

import pandas as pd
df = pd.DataFrame(adl_events)

print(f"\nTotal ADL events: {len(df):,}")

# Check liquidation data availability
has_liquidation_data = df['liquidation_data'].notna()
print(f"\nADL events with liquidation data: {has_liquidation_data.sum():,} ({has_liquidation_data.sum()/len(df)*100:.2f}%)")

has_liquidated_user = df['liquidated_user'].notna()
print(f"ADL events with liquidated_user: {has_liquidated_user.sum():,} ({has_liquidated_user.sum()/len(df)*100:.2f}%)")

# Check if user == liquidated_user (losing position)
losing_positions = df[df['is_losing'] == True]
winning_positions = df[df['is_losing'] == False]
unknown = df[df['is_losing'].isna()]

print(f"\n📊 Position Type Analysis:")
print(f"  Losing positions (user == liquidated_user): {len(losing_positions):,} ({len(losing_positions)/len(df)*100:.2f}%)")
print(f"  Winning positions (user != liquidated_user): {len(winning_positions):,} ({len(winning_positions)/len(df)*100:.2f}%)")
print(f"  Unknown (no liquidated_user): {len(unknown):,} ({len(unknown)/len(df)*100:.2f}%)")

if len(losing_positions) > 0:
    print("\n⚠️  FOUND: Losing positions ARE labeled as ADL!")
    print(f"\nSample losing positions (user == liquidated_user):")
    print(losing_positions[['user', 'coin', 'direction', 'closed_pnl', 'size']].head(10))
    
    print(f"\nStatistics for losing positions:")
    print(f"  Average closed_pnl: ${losing_positions['closed_pnl'].mean():,.2f}")
    print(f"  Total closed_pnl: ${losing_positions['closed_pnl'].sum():,.2f}")
    print(f"  Average size: {losing_positions['size'].abs().mean():,.4f}")
else:
    print("\n✅ CONFIRMED: No losing positions labeled as ADL")
    print("  All ADL events are winning positions (user != liquidated_user)")

if len(winning_positions) > 0:
    print(f"\nStatistics for winning positions:")
    print(f"  Average closed_pnl: ${winning_positions['closed_pnl'].mean():,.2f}")
    print(f"  Total closed_pnl: ${winning_positions['closed_pnl'].sum():,.2f}")

print("\n" + "="*80)
print("CONCLUSION")
print("="*80)

if len(losing_positions) > 0:
    print("❌ RESEARCHER IS CORRECT: Losing positions ARE also labeled as ADL")
    print(f"   Found {len(losing_positions):,} ADL events where user == liquidated_user")
    print("   This means both sides of an ADL event get the 'Auto-Deleveraging' label")
else:
    print("✅ RESEARCHER IS INCORRECT: Losing positions are NOT labeled as ADL")
    print("   All ADL events are winning positions providing liquidity")
    print("   Losing positions are likely labeled as 'Liquidated' not 'Auto-Deleveraging'")

