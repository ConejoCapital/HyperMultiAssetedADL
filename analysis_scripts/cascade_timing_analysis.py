#!/usr/bin/env python3
"""Cascade timing analysis for `CASCADE_TIMING_ANALYSIS.md`.

Produces:
- initial liquidation time
- first ADL activation time and delay
- per-second liquidation/ADL counts
- top burst seconds
Outputs JSON alongside stdout summary.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_DIR = ROOT / "cash-only balances ADL event orderbook 2025-10-10"
ADL_PATH = CANONICAL_DIR / "adl_fills_full_12min_raw.csv"
LIQ_PATH = CANONICAL_DIR / "liquidations_full_12min.csv"
OUTPUT_JSON = ROOT / "analysis_scripts" / "cascade_timing_results.json"


def load(path: Path, time_col: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df[time_col] = pd.to_datetime(df[time_col], utc=True)
    return df


def per_second_counts(df: pd.DataFrame, time_col: str, origin: pd.Timestamp) -> pd.Series:
    seconds = (df[time_col] - origin).dt.total_seconds().astype(int)
    return seconds.value_counts().sort_index()


def main() -> None:
    print("Cascade Timing • Canonical Replay")
    liq = load(LIQ_PATH, "block_time")
    adl = load(ADL_PATH, "block_time")

    event_start = min(liq["block_time"].min(), adl["block_time"].min())
    first_liq = liq["block_time"].min()
    first_adl = adl["block_time"].min()
    delay_seconds = (first_adl - first_liq).total_seconds()

    liq_counts = per_second_counts(liq, "block_time", event_start)
    adl_counts = per_second_counts(adl, "block_time", event_start)

    combined_index = sorted(set(liq_counts.index) | set(adl_counts.index))
    timeline = []
    for sec in combined_index:
        timeline.append({
            "second": int(sec),
            "liquidations": int(liq_counts.get(sec, 0)),
            "adls": int(adl_counts.get(sec, 0)),
        })

    top_bursts = sorted(
        timeline,
        key=lambda entry: (entry["liquidations"] + entry["adls"]),
        reverse=True,
    )[:10]

    result: Dict[str, object] = {
        "event_start": event_start.isoformat(),
        "first_liquidation": first_liq.isoformat(),
        "first_adl": first_adl.isoformat(),
        "delay_seconds": delay_seconds,
        "timeline": timeline,
        "top_bursts": top_bursts,
    }

    print(f"First liquidation: {first_liq.isoformat()}")
    print(f"First ADL: {first_adl.isoformat()} (delay {delay_seconds:.1f}s)")
    print("Top bursts (liquidations + ADL events per second):")
    for entry in top_bursts:
        sec = entry["second"]
        total = entry["liquidations"] + entry["adls"]
        print(f"  second {sec:>3}: {entry['liquidations']} liq / {entry['adls']} adl (total {total})")

    OUTPUT_JSON.write_text(json.dumps(result, indent=2))
    print(f"\nResults written to {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
