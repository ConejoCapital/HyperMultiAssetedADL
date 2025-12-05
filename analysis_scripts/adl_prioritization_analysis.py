#!/usr/bin/env python3
"""ADL prioritization analysis for `ADL_PRIORITIZATION_VERIFIED.md`.

Calculates profitability, leverage distribution, and top repeated winners
using the canonical real-time dataset.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_DIR = ROOT / "cash-only balances ADL event orderbook 2025-10-10"
ADL_DETAIL_PATH = CANONICAL_DIR / "adl_detailed_analysis_REALTIME.csv"
OUTPUT_JSON = ROOT / "analysis_scripts" / "adl_prioritization_results.json"


def main() -> None:
    print("ADL Prioritization • Canonical Replay")
    df = pd.read_csv(ADL_DETAIL_PATH)

    profitable_pct = (df["pnl_percent"] > 0).mean() * 100
    avg_pnl = df["pnl_percent"].mean()
    median_pnl = df["pnl_percent"].median()
    median_leverage = df["leverage_realtime"].median()
    p95_leverage = df["leverage_realtime"].quantile(0.95)
    p99_leverage = df["leverage_realtime"].quantile(0.99)

    # Identify repeated winners targeted multiple times
    winner_counts = (
        df[df["pnl_percent"] > 0]
        .groupby("user")["pnl_percent"]
        .count()
        .sort_values(ascending=False)
    )

    top_repeaters = [
        {"user": user, "adl_events": int(count)}
        for user, count in winner_counts.head(10).items()
    ]

    results = {
        "total_adl_events": int(len(df)),
        "profitable_pct": profitable_pct,
        "avg_pnl_percent": avg_pnl,
        "median_pnl_percent": median_pnl,
        "median_leverage": median_leverage,
        "p95_leverage": p95_leverage,
        "p99_leverage": p99_leverage,
        "top_repeated_winners": top_repeaters,
    }

    print(f"Profitable ADL share: {profitable_pct:.2f}%")
    print(f"Median leverage: {median_leverage:.2f}x (p95 {p95_leverage:.2f}x, p99 {p99_leverage:.2f}x)")

    OUTPUT_JSON.write_text(json.dumps(results, indent=2))
    print(f"Results written to {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
