# Cash-Only Balances – Hyperliquid ADL Event (2025-10-10)

This folder contains the canonical replay outputs regenerated with the cash-only account baseline (snapshot unrealized PnL removed before event processing). Use these files if you need the reconciled leverage, equity, and negative-equity metrics for the October 10, 2025 12-minute cascade.

## Contents

- `adl_detailed_analysis_REALTIME.csv` – 34,983 ADL events with real-time cash balances, leverage, total equity, and counterparty links.
- `adl_by_user_REALTIME.csv` – 19,337 user-level aggregates derived from the cash-only replay.
- `adl_by_coin_REALTIME.csv` – 162 coin-level aggregates.
- `realtime_analysis_summary.json` – Summary statistics (median leverage ≈ 0.18x, 1,147 underwater accounts, −$109.29M total equity).
- `adl_fills_full_12min_raw.csv` – Raw ADL fills (blockchain data) used by the replay.
- `liquidations_full_12min.csv` – Liquidation fills aligned with the same window.
- `adl_net_volume_full_12min.csv` – Net ADL notional per ticker.
- `ADL_NET_VOLUME_FULL_12MIN.md` – Narrative summary of ADL volumes.

## Key Differences vs. Previous Replay

- Snapshot account values are adjusted to remove unrealized PnL before streaming events.
- Leverage metrics now reflect true cash backing at the ADL moment (median 0.18x; 99th percentile ~74x).
- Negative equity count is 1,147 accounts with an aggregate −$109.29M deficit.

## Reproduction

From the repository root:

```bash
python extract_full_12min_adl.py
python full_analysis_realtime.py
```

Ensure the clearinghouse snapshot JSONs (`account_value_snapshot_*.json`, `perp_positions_by_market_*.json`, etc.) are present in the working directory before running `full_analysis_realtime.py`.
