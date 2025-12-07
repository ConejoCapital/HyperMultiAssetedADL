#!/usr/bin/env python3
"""Supplementary prioritization stats for `ADL_PRIORITIZATION_ANALYSIS_LOCAL.md`.

Produces correlation measures and per-coin ranking diagnostics.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[2]
CANONICAL_DIR = ROOT / "data/canonical/cash-only balances ADL event orderbook 2025-10-10"
ADL_DETAIL_PATH = CANONICAL_DIR / "adl_detailed_analysis_REALTIME.csv"
OUTPUT_JSON = ROOT / "analysis_scripts" / "adl_prioritization_local_results.json"


def per_coin_rank_gap(df: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
    """Compute average rank position for top-N profitable accounts per coin."""
    records = []
    for coin, grp in df.groupby("coin"):
        grp = grp.sort_values("time")
        grp["adl_order"] = np.arange(len(grp)) + 1
        grp = grp.sort_values("pnl_percent", ascending=False)
        top = grp.head(min(top_n, len(grp)))
        if not top.empty:
            records.append({
                "coin": coin,
                "avg_order_top_profit": top["adl_order"].mean(),
                "median_order_top_profit": top["adl_order"].median(),
                "avg_pnl_top": top["pnl_percent"].mean(),
            })
    return pd.DataFrame(records).sort_values("avg_order_top_profit")


def main() -> None:
    print("Local Prioritization Diagnostics • Canonical Replay")
    df = pd.read_csv(ADL_DETAIL_PATH)
    df["time"] = pd.to_datetime(df["time"], unit="ms", utc=True)

    correlations = {
        "pnl_vs_notional": spearmanr(df["pnl_percent"], df["adl_notional"]).correlation,
        "pnl_vs_leverage": spearmanr(df["pnl_percent"], df["leverage_realtime"]).correlation,
        "notional_vs_leverage": spearmanr(df["adl_notional"], df["leverage_realtime"]).correlation,
    }

    per_coin_stats = per_coin_rank_gap(df)
    top_assets = per_coin_stats.head(10).to_dict(orient="records")

    result = {
        "spearman_correlations": correlations,
        "top_assets_by_avg_order": top_assets,
    }

    print("Spearman correlations (pnl vs metrics):")
    for metric, value in correlations.items():
        print(f"  {metric}: {value:.4f}")

    OUTPUT_JSON.write_text(json.dumps(result, indent=2))
    print(f"Saved results to {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
