#!/usr/bin/env python3
"""Per-Asset Isolation verification for `PER_ASSET_ISOLATION.md`.

This script uses the canonical 12-minute dataset to recompute the per-asset
isolation metrics:
- number of timestamps with both liquidations and ADL events
- cross-asset contamination checks (ADL tickers not subset of liquidations)
- Jaccard overlap (liquidation vs ADL tickers) summary
- largest simultaneous burst ticker counts
Results are printed to stdout and saved as JSON for reproducibility.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Set

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_DIR = ROOT / "cash-only balances ADL event orderbook 2025-10-10"
CANONICAL_ADL = CANONICAL_DIR / "adl_fills_full_12min_raw.csv"
CANONICAL_LIQ = CANONICAL_DIR / "liquidations_full_12min.csv"
OUTPUT_JSON = ROOT / "analysis_scripts" / "per_asset_isolation_results.json"


def load_dataset(path: Path, time_col: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df[time_col] = pd.to_datetime(df[time_col], utc=True)
    return df


def group_coins(df: pd.DataFrame, time_col: str) -> Dict[pd.Timestamp, Set[str]]:
    return (
        df.groupby(time_col)["coin"]
        .apply(lambda s: set(str(x) for x in s))
        .to_dict()
    )


def main() -> None:
    print("Per-Asset Isolation • Canonical Replay (12 minutes)")
    print("Loading canonical datasets...")
    adl_df = load_dataset(CANONICAL_ADL, "block_time")
    liq_df = load_dataset(CANONICAL_LIQ, "block_time")

    adl_groups = group_coins(adl_df, "block_time")
    liq_groups = group_coins(liq_df, "block_time")

    common_times = sorted(set(adl_groups) & set(liq_groups))
    cross_asset_cases = []
    jaccard_scores = []

    for ts in common_times:
        adl_coins = adl_groups[ts]
        liq_coins = liq_groups[ts]
        if not adl_coins.issubset(liq_coins):
            cross_asset_cases.append({
                "timestamp": ts.isoformat(),
                "adl_only_coins": sorted(adl_coins - liq_coins),
            })
        union = liq_coins | adl_coins
        if union:
            jaccard_scores.append(len(liq_coins & adl_coins) / len(union))

    # capture largest simultaneous burst
    burst_counts = {
        ts.isoformat(): {
            "liquidation_tickers": len(liq_groups[ts]),
            "adl_tickers": len(adl_groups[ts]),
        }
        for ts in common_times
    }
    top_bursts = sorted(
        burst_counts.items(),
        key=lambda kv: (kv[1]["liquidation_tickers"], kv[1]["adl_tickers"]),
        reverse=True,
    )[:5]

    result = {
        "total_timestamps_with_both": len(common_times),
        "cross_asset_cases": cross_asset_cases,
        "cross_asset_case_count": len(cross_asset_cases),
        "jaccard_avg_first_100": float(pd.Series(jaccard_scores[:100]).mean()),
        "jaccard_min_first_100": float(pd.Series(jaccard_scores[:100]).min()),
        "largest_bursts": top_bursts,
    }

    print("\nSummary:")
    print(f"  Timestamps with both liquidation + ADL: {result['total_timestamps_with_both']}")
    print(f"  Cross-asset cases: {result['cross_asset_case_count']}")
    print(f"  Jaccard overlap (first 100): {result['jaccard_avg_first_100']*100:.2f}% avg")

    OUTPUT_JSON.write_text(json.dumps(result, indent=2))
    print(f"\nResults written to {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
