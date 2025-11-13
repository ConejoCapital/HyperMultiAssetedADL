# Audit Report: Canonical 12-Minute Chain Replay (No Approximations)

**Date**: November 13, 2025  
**Status**: ✅ **COMPLETE — Canonical realtime replay verified**

---

## 🧾 Executive Summary

- Replayed **3,239,706 on-chain events** (fills, funding, ledger) from the clearinghouse snapshot at 20:04:54 UTC through 21:27:00 UTC using `full_analysis_realtime.py`.
- Produced the **canonical 34,983-event dataset** (`adl_detailed_analysis_REALTIME.csv`) with real-time account value, leverage, equity, and negative-equity detection.
- Confirmed **per-asset ADL coverage** (mean 35.4%, median 33.2%) against the matched liquidation feed (`liquidations_full_12min.csv`).
- Removed every approximation artifact (snapshot-based CSVs, stale leverage columns) and updated documentation to reference only realtime outputs.
- Cross-validated downstream analyses (`ADL_PRIORITIZATION_VERIFIED.md`, `ADL_PRIORITIZATION_ANALYSIS_LOCAL.md`, `INSURANCE_FUND_IMPACT.md`) on the regenerated dataset.

Use this report as the audit trail that the public repository contains one—and only one—canonical source of truth for the October 10, 2025 ADL cascade.

---

## 🔁 Chain Replay Verification (Current State)

| Item | Result |
|------|--------|
| Time window | 20:04:54 to 21:27:00 UTC (snapshot replay + 12-minute cascade) |
| Total events processed | **3,239,706** (fills, funding, deposits/withdrawals) |
| Accounts reconstructed | **437,723** |
| ADL fills extracted | **34,983** (100% coverage) |
| Liquidations matched | **34,983** counterparty events (1:1) |
| Negative-equity accounts | **1,275** (−$125,981,795 combined) |
| Median realtime leverage | **0.15x** |
| Dataset location | `adl_detailed_analysis_REALTIME.csv` |

The replay is reproducible by running `python full_analysis_realtime.py` from the repository root. A step-by-step walkthrough lives in `REAL_TIME_RECONSTRUCTION_SUMMARY.md`.

---

## 🛠️ Legacy Issues Resolved (Historical Record)

### 1. Incomplete Time Window (✅ Fixed)
- **Original problem**: `ADL_END_TIME` stopped at 21:20:00, omitting 2,310 ADL events and ~628k intermediary events.
- **Fix**: Expanded `ADL_END_TIME` to 21:27:00 (Unix ms `1760131620000`). Replay now covers the entire cascade (10.88 minutes of ADLs).

### 2. Approximation CSVs (✅ Purged)
- **Original problem**: Snapshot-based CSVs (`adl_detailed_analysis.csv`, `adl_by_user.csv`, `adl_by_coin.csv`) coexisted with realtime data and surfaced stale leverage/account values.
- **Fix**: Deleted the approximation files and replaced every reference with the realtime equivalents (only `_REALTIME` suffixed files remain).

These issues are documented here so future auditors can see what changed and why. The repository no longer contains any approximated outputs.

---

## 📦 Canonical Files & Supporting Artifacts

| File | Purpose |
|------|---------|
| `adl_detailed_analysis_REALTIME.csv` | Canonical per-position dataset (34,983 rows) with realtime account values, leverage, equity, negative-equity flag, and ADL counterparties. |
| `adl_by_user_REALTIME.csv` / `adl_by_coin_REALTIME.csv` | Aggregations derived directly from the canonical dataset. |
| `liquidations_full_12min.csv` | Matched liquidation fills used to compute per-asset ADL coverage. |
| `full_analysis_realtime.py` | Replay script (clearinghouse snapshot ➝ realtime metrics). |
| `REAL_TIME_RECONSTRUCTION_SUMMARY.md` | Detailed methodology and reproducibility notes. |
| `ADL_PRIORITIZATION_VERIFIED.md` | Public-facing verification that ADL targets profit, refreshed against the canonical replay. |

Only these realtime files should be used in research or downstream analysis. Any file without the `_REALTIME` suffix has been removed by design.

---

## ✅ Verification Checklist

### Data Integrity Checks
- ✅ 34,983 ADL events parsed from the raw chain feed (`adl_fills_full_12min_raw.csv`).
- ✅ Chronological replay of 3.24M events; no processing gaps.
- ✅ `account_value_realtime`, `total_unrealized_pnl`, and `total_equity` reconcile with cumulative `closed_pnl` movements.
- ✅ `is_negative_equity` flag aligns with `total_equity < 0` and feeds the insurance-fund impact analysis (`INSURANCE_FUND_IMPACT.md`).

### Column & Schema Checks
- ✅ `leverage_realtime` (not the deprecated `leverage`).
- ✅ `account_value_realtime` (not the deprecated snapshot `account_value`).
- ✅ Negative-equity detection, realtime entry prices, counterparty linkage columns present.

### Coverage & Cross-Checks
- ✅ Per-asset ADL-to-liquidation ratios computed (mean 35.4%, median 33.2%).
- ✅ ADL prioritization timing tests rerun on the canonical dataset (see `ADL_PRIORITIZATION_ANALYSIS_LOCAL.md`).
- ✅ Insurance-fund impact quantified: −$125,981,795 (see `INSURANCE_FUND_IMPACT.md`).

---

## 📘 Guidance for Researchers

```python
import pandas as pd

df = pd.read_csv('adl_detailed_analysis_REALTIME.csv')
assert len(df) == 34_983, "Expect 34,983 ADL events"
assert {'leverage_realtime', 'account_value_realtime', 'is_negative_equity'} <= set(df.columns)
print('✅ Canonical realtime dataset loaded.')
```

- Use ONLY the `_REALTIME` CSVs.
- Expect 34,983 rows; any other row count indicates an outdated file.
- Leverage statistics reported in the repository (median 0.15x, 95th percentile 3.22x, 99th percentile 13.65x) come directly from this dataset.

---

## 📚 References & Repository State

- Primary repo: https://github.com/ConejoCapital/HyperMultiAssetedADL
- Reproducibility: `full_analysis_realtime.py`, `REAL_TIME_RECONSTRUCTION_SUMMARY.md`
- Downstream analyses refreshed against the canonical data:
  - `ADL_PRIORITIZATION_VERIFIED.md`
  - `ADL_PRIORITIZATION_ANALYSIS_LOCAL.md`
  - `INSURANCE_FUND_IMPACT.md`
  - `PER_ASSET_ISOLATION.md`

The repository is free of approximation artifacts and every public claim now references the realtime replay.

---

**Audited**: November 13, 2025  
**Auditor**: Real-Time Reconstruction Pipeline  
**Files Processed**: 3,239,706 events  
**Events Analyzed**: 34,983 ADL events  
**Accounts Tracked**: 437,723  
**Coverage**: 100%  
**Approximations**: 0  
**Shortcuts**: 0
