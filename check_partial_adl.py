#!/usr/bin/env python3
"""Check if partial ADL closures exist in the data."""
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ADL_PATH = ROOT / "data/canonical/cash-only balances ADL event orderbook 2025-10-10/adl_fills_full_12min_raw.csv"

print("Loading ADL fills...")
df = pd.read_csv(ADL_PATH)

print(f"Total ADL fills: {len(df):,}")
print(f"Columns: {list(df.columns)}")

# Check if we have liquidated_user column
if 'liquidated_user' in df.columns:
    print("\n✓ liquidated_user column exists")
    print(f"  Non-null liquidated_user: {df['liquidated_user'].notna().sum():,}")
    print(f"  Null liquidated_user: {df['liquidated_user'].isna().sum():,}")
    
    # Check cases where user == liquidated_user (losing position)
    losing_positions = df[df['user'] == df['liquidated_user']]
    print(f"\nLosing positions (user == liquidated_user): {len(losing_positions):,}")
    
    # Check cases where user != liquidated_user (winning position providing liquidity)
    winning_positions = df[df['user'] != df['liquidated_user']]
    print(f"Winning positions (user != liquidated_user): {len(winning_positions):,}")
    
    # Check if size == abs(start_position) for losing positions
    if len(losing_positions) > 0:
        losing_full = losing_positions[losing_positions['size'] == losing_positions['start_position'].abs()]
        losing_partial = losing_positions[losing_positions['size'] != losing_positions['start_position'].abs()]
        print(f"\n  Losing positions - Full closure (size == abs(start_position)): {len(losing_full):,}")
        print(f"  Losing positions - Partial closure (size != abs(start_position)): {len(losing_partial):,}")
        if len(losing_partial) > 0:
            print("\n  ⚠️  WARNING: Found losing positions with partial closures!")
            print(losing_partial[['user', 'coin', 'size', 'start_position', 'closed_pnl']].head(10))
    
    # Check if size == abs(start_position) for winning positions
    if len(winning_positions) > 0:
        winning_full = winning_positions[winning_positions['size'] == winning_positions['start_position'].abs()]
        winning_partial = winning_positions[winning_positions['size'] != winning_positions['start_position'].abs()]
        print(f"\n  Winning positions - Full closure (size == abs(start_position)): {len(winning_full):,}")
        print(f"  Winning positions - Partial closure (size != abs(start_position)): {len(winning_partial):,}")
        if len(winning_partial) > 0:
            print("\n  ✓ Found winning positions with partial closures (expected!)")
            print(winning_partial[['user', 'coin', 'size', 'start_position', 'closed_pnl']].head(10))
else:
    print("\n✗ liquidated_user column NOT found")
    print("  Need to check raw data source for this field")

# General check: size vs abs(start_position)
print("\n" + "="*80)
print("General Analysis: size vs abs(start_position)")
print("="*80)

df['abs_start'] = df['start_position'].abs()
full_closure = df[df['size'] == df['abs_start']]
partial_closure = df[df['size'] != df['abs_start']]

print(f"\nFull closure (size == abs(start_position)): {len(full_closure):,} ({len(full_closure)/len(df)*100:.2f}%)")
print(f"Partial closure (size != abs(start_position)): {len(partial_closure):,} ({len(partial_closure)/len(df)*100:.2f}%)")

if len(partial_closure) > 0:
    print("\nSample partial closures:")
    print(partial_closure[['user', 'coin', 'size', 'start_position', 'closed_pnl']].head(10))
    
    print("\nStatistics for partial closures:")
    print(f"  Average size: {partial_closure['size'].mean():.4f}")
    print(f"  Average start_position: {partial_closure['start_position'].abs().mean():.4f}")
    print(f"  Average ratio (size/abs(start_position)): {(partial_closure['size'] / partial_closure['abs_start']).mean():.4f}")
    print(f"  Min ratio: {(partial_closure['size'] / partial_closure['abs_start']).min():.4f}")
    print(f"  Max ratio: {(partial_closure['size'] / partial_closure['abs_start']).max():.4f}")

