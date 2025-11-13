#!/usr/bin/env python3
"""Batch processing verification for `BATCH_PROCESSING_DISCOVERY.md`.

Checks performed:
- number of timestamps containing both liquidations and ADL events
- confirmation that the initial window contains liquidations only
- per-timestamp ordering summary indicating the fraction of events that are
  liquidations vs ADL for the first shared timestamps
- exports JSON with aggregated metrics for reproducibility
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
ADL_PATH = ROOT / "adl_fills_full_12min_raw.csv"
LIQ_PATH = ROOT / "liquidations_full_12min.csv"
OUTPUT_JSON = ROOT / "analysis_scripts" / "batch_processing_results.json"


def load(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["block_time"] = pd.to_datetime(df["block_time"], utc=True)
    return df


def main() -> None:
    print("Batch Processing • Canonical Replay")
    liq = load(LIQ_PATH)
    adl = load(ADL_PATH)

    combined = (
        pd.concat([
            liq.assign(event_type="liquidation"),
            adl.assign(event_type="adl"),
        ])
        .sort_values("block_time")
        .reset_index(drop=True)
    )

    grouped = combined.groupby("block_time")
    summary = grouped["event_type"].value_counts().unstack(fill_value=0)
    summary = summary.rename(columns={"liquidation": "liquidations", "adl": "adls"})

    # Identify the first segment containing only liquidations
    summary["has_adl"] = summary["adls"] > 0
    liquidation_only_seconds = int((summary["has_adl"].idxmax() - summary.index.min()).total_seconds())

    both_mask = (summary["liquidations"] > 0) & (summary["adls"] > 0)
    timestamps_with_both = summary[both_mask]

    result = {
        "total_timestamps": len(summary),
        "timestamps_with_both": len(timestamps_with_both),
        "initial_liquidation_only_seconds": liquidation_only_seconds,
        "first_shared_timestamp": timestamps_with_both.index.min().isoformat() if not timestamps_with_both.empty else None,
        "top_shared_bursts": [
            {
                "timestamp": ts.isoformat(),
                "liquidations": int(row["liquidations"]),
                "adls": int(row["adls"]),
            }
            for ts, row in timestamps_with_both.sort_values([
                "liquidations", "adls"
            ], ascending=False).head(10).iterrows()
        ],
    }

    print(f"Timestamps analysed: {result['total_timestamps']:,}")
    print(f"Timestamps with both liquidation + ADL: {result['timestamps_with_both']:,}")
    print(f"Initial liquidation-only run: {result['initial_liquidation_only_seconds']} seconds")

    OUTPUT_JSON.write_text(json.dumps(result, indent=2))
    print(f"Results written to {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
