#!/usr/bin/env python3
"""Insurance fund impact analysis for `INSURANCE_FUND_IMPACT.md`.

Calculates the distribution of negative-equity accounts (accounts where
`total_equity < 0`), aggregate deficit, and top underwater positions.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
CANONICAL_DIR = ROOT / "data/canonical/cash-only balances ADL event orderbook 2025-10-10"
ADL_DETAIL_PATH = CANONICAL_DIR / "adl_detailed_analysis_REALTIME.csv"
OUTPUT_JSON = ROOT / "scripts" / "analysis" / "outputs" / "insurance_fund_results.json"


def main() -> None:
    print("Insurance Fund Impact • Canonical Replay")
    df = pd.read_csv(ADL_DETAIL_PATH)

    underwater = df[df["is_negative_equity"]]
    total_underwater = float(underwater["total_equity"].sum())
    count_underwater = int(len(underwater))
    share = count_underwater / len(df) * 100

    top_underwater = (
        underwater.sort_values("total_equity")
        .head(10)[["user", "coin", "total_equity", "adl_notional"]]
        .to_dict(orient="records")
    )

    result = {
        "total_adl_events": int(len(df)),
        "underwater_accounts": count_underwater,
        "underwater_share_percent": share,
        "total_negative_equity": total_underwater,
        "top_underwater_accounts": top_underwater,
    }

    print(f"Accounts underwater: {count_underwater:,} ({share:.2f}% of ADL events)")
    print(f"Aggregate deficit: ${total_underwater:,.2f}")

    OUTPUT_JSON.write_text(json.dumps(result, indent=2))
    print(f"Results written to {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
