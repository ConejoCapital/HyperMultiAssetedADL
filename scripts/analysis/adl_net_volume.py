#!/usr/bin/env python3
"""ADL net volume analysis for `ADL_NET_VOLUME_FULL_12MIN.md`.

Summarises ADL volume by ticker across the full 12-minute canonical dataset.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
CANONICAL_DIR = ROOT / "data/canonical/cash-only balances ADL event orderbook 2025-10-10"
ADL_PATH = CANONICAL_DIR / "adl_fills_full_12min_raw.csv"
OUTPUT_JSON = ROOT / "scripts" / "analysis" / "outputs" / "adl_net_volume_results.json"


def main() -> None:
    print("ADL Net Volume • Canonical Replay")
    adl = pd.read_csv(ADL_PATH)

    by_ticker = adl.groupby("coin").agg(
        events=("coin", "count"),
        net_volume=("size", "sum"),
        net_notional=("notional", "sum"),
        total_pnl=("closed_pnl", "sum"),
        avg_price=("price", "mean"),
    ).sort_values("net_notional", ascending=False)

    result = {
        "total_events": int(len(adl)),
        "total_notional": float(by_ticker["net_notional"].sum()),
        "top10": (
            by_ticker.head(10)
            .round({"net_volume": 4, "net_notional": 2, "avg_price": 4, "total_pnl": 2})
            .to_dict(orient="index")
        ),
    }

    print(f"Total ADL events: {result['total_events']:,}")
    print(f"Total ADL notional: ${result['total_notional']:,.0f}")

    OUTPUT_JSON.write_text(json.dumps(result, indent=2))
    print(f"Saved results to {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
