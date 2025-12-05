#!/usr/bin/env python3
"""Total impact calculation for `TOTAL_IMPACT_ANALYSIS.md`.

Uses canonical CSV outputs to compute aggregate liquidation + ADL totals.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_DIR = ROOT / "cash-only balances ADL event orderbook 2025-10-10"
ADL_PATH = CANONICAL_DIR / "adl_fills_full_12min_raw.csv"
LIQ_PATH = CANONICAL_DIR / "liquidations_full_12min.csv"
OUTPUT_JSON = ROOT / "analysis_scripts" / "total_impact_results.json"


def aggregate(df: pd.DataFrame) -> pd.DataFrame:
    grouped = df.groupby("coin").agg(
        events=("coin", "count"),
        notional=("notional", "sum"),
        pnl=("closed_pnl", "sum"),
    )
    return grouped.sort_values("notional", ascending=False)


def main() -> None:
    print("Total Impact • Canonical Replay")
    adl = pd.read_csv(ADL_PATH)
    liq = pd.read_csv(LIQ_PATH)

    adl_totals = aggregate(adl)
    liq_totals = aggregate(liq)

    total_notional = adl_totals["notional"].sum() + liq_totals["notional"].sum()
    total_events = int(len(adl) + len(liq))

    result = {
        "liquidations": {
            "events": int(len(liq)),
            "notional": float(liq_totals["notional"].sum()),
            "pnl": float(liq_totals["pnl"].sum()),
        },
        "adl": {
            "events": int(len(adl)),
            "notional": float(adl_totals["notional"].sum()),
            "pnl": float(adl_totals["pnl"].sum()),
        },
        "total": {
            "events": total_events,
            "notional": float(total_notional),
        },
        "top_combined_tickers": (
            pd.concat([
                liq_totals[["notional"]].rename(columns={"notional": "liquidations"}),
                adl_totals[["notional"]].rename(columns={"notional": "adl"}),
            ], axis=1)
            .fillna(0)
            .assign(total=lambda df: df.sum(axis=1))
            .sort_values("total", ascending=False)
            .head(10)
            .round(2)
            .to_dict(orient="index")
        ),
    }

    print(f"Liquidations: {result['liquidations']['events']:,} events – ${result['liquidations']['notional']:,.0f}")
    print(f"ADL: {result['adl']['events']:,} events – ${result['adl']['notional']:,.0f}")
    print(f"TOTAL IMPACT: ${result['total']['notional']:,.0f} across {total_events:,} events")

    OUTPUT_JSON.write_text(json.dumps(result, indent=2))
    print(f"Saved results to {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
