#!/usr/bin/env python3
"""Counterparty mechanics verification for `ADL_MECHANISM_RESEARCH.md`.

Outputs:
- share of ADL events with an explicit `liquidated_user`
- details of the highlighted $174M ETH ADL event and matching liquidations
- saves summary JSON for reproducibility
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
ADL_DETAIL_PATH = ROOT / "adl_detailed_analysis_REALTIME.csv"
ADL_RAW_PATH = ROOT / "adl_fills_full_12min_raw.csv"
LIQ_PATH = ROOT / "liquidations_full_12min.csv"
OUTPUT_JSON = ROOT / "analysis_scripts" / "adl_mechanism_results.json"

TARGET_COIN = "ETH"


def main() -> None:
    print("ADL Mechanism • Canonical Replay")

    detail = pd.read_csv(ADL_DETAIL_PATH)
    raw_adl = pd.read_csv(ADL_RAW_PATH)
    liq = pd.read_csv(LIQ_PATH)

    detail["event_time"] = pd.to_datetime(detail["time"], unit="ms", utc=True)
    raw_adl["event_time"] = pd.to_datetime(raw_adl["block_time"], utc=True)
    liq["event_time"] = pd.to_datetime(liq["block_time"], utc=True)
    liq["time_ms"] = liq["event_time"].view('int64') // 10**6

    counterparty_rate = detail["liquidated_user"].notna().mean()

    eth_adl = detail[detail["coin"] == TARGET_COIN].sort_values("adl_notional", ascending=False).iloc[0]
    eth_time = eth_adl["event_time"]
    eth_time_ms = int(eth_adl["time"])  # millisecond epoch
    raw_match = raw_adl[(raw_adl["event_time"] == eth_time) & (raw_adl["coin"] == TARGET_COIN)]
    matching_liqs = liq[(liq["time_ms"] == eth_time_ms) & (liq["coin"] == TARGET_COIN)]

    print(f"Highlighted ADL ({TARGET_COIN}): ${eth_adl['adl_notional']:,.2f} at {eth_time}")
    print(f"Counterparty liquidation count at same timestamp: {len(matching_liqs):,}")
    print(f"ADL events with explicit counterparty: {counterparty_rate*100:.2f}%")

    result = {
        "total_adl_events": int(len(detail)),
        "counterparty_rate": counterparty_rate,
        "highlighted_adl": {
            "coin": TARGET_COIN,
            "timestamp": eth_time.isoformat(),
            "notional_usd": float(eth_adl["adl_notional"]),
            "real_time_account_value": float(eth_adl["account_value_realtime"]),
            "real_time_equity": float(eth_adl["total_equity"]),
            "unrealized_pnl_percent": float(eth_adl["pnl_percent"]),
            "liquidations_same_timestamp": int(len(matching_liqs)),
            "adl_fill_count_same_timestamp": int(len(raw_match)),
        },
    }

    OUTPUT_JSON.write_text(json.dumps(result, indent=2))
    print(f"Results written to {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
