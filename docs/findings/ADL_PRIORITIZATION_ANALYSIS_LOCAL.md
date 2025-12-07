
# Local ADL Prioritization Analysis - Canonical Dataset

> Associated script: `scripts/analysis/adl_prioritization_local.py`

---

# ADL Prioritization Analysis (Canonical Dataset)

**Analysis Date:** November 13, 2025  
**Event:** October 10, 2025 Liquidation Cascade  
**Data Sources:**
- `data/canonical/cash-only balances ADL event orderbook 2025-10-10/adl_detailed_analysis_REALTIME.csv` (34,983 ADL fills with real-time leverage & equity, fixed position size calculation)
- `liquidations_full_12min.csv` (63,637 liquidation fills for comparison)
- `adl_fills_full_12min_raw.csv` (canonical 12-minute ADL feed)

**Status:** ✅ Fully reproducible with the canonical realtime reconstruction — leverage, account value, and per-asset liquidation data are now complete. This note preserves the original “local” experiments but refreshes every test with the regenerated dataset.

---

## Key Takeaways

| Finding | Evidence (Canonical Dataset) |
|---------|------------------------------|
| ADL is *not* ordered by profit, size, or leverage | Top 100 by PNL fire at **02:59** on average vs **01:43** overall; top 100 by size at **02:12**; top 100 by leverage at **02:17** |
| Correlations with trigger time remain near zero | `corr(pnl%, time) = +0.098`, `corr(adl_notional, time) = +0.009`, `corr(leverage, time) = +0.006` (≤99th pct leverage: −0.012) |
| Per-asset ADL/liq ratio is remarkably stable | Mean **35.4%**, median **33.2%**, 10 largest tickers in the 34–45% band |
| Profitable traders are repeatedly targeted | Top-10 ADL’d addresses average **$269k** realized PNL per event vs **$12k** for everyone else (22×) |
| Dataset coverage | 34,983 ADLs, 19,337 users, $2.10B notional, median leverage **0.20x** |

---

## Data & Methodology

1. **Time alignment** – Converted `time` (ms) to seconds-relative (0 = first ADL at 21:16:04.831 UTC).  
2. **Ranking tests** – Recomputed top/bottom timing splits for PNL, notional, and leverage using the canonical CSV.  
3. **Correlations** – Pearson correlations between trigger time and PNL%, ADL notional, leverage (full sample and ≤99th percentile).  
4. **Per-asset ratios** – Joined canonical ADL notional with liquidation notional per ticker.  
5. **User repetition** – Aggregated ADL events per address, capturing total/average realized PNL and mean leverage.

All calculations can be reproduced with the notebook-free Python snippets included in this repository (`data/canonical/cash-only balances ADL event orderbook 2025-10-10/adl_detailed_analysis_REALTIME.csv`, `data/canonical/cash-only balances ADL event orderbook 2025-10-10/liquidations_full_12min.csv`).

---

## Test 1 – Do the Most Profitable Positions Fire First?

**Hypothesis:** The protocol should ADL the highest PNL traders first if it wants the most insurance coverage.

| Rank | ADL Notional | Closed PNL | PNL % | Coin | When ADL Fired |
|------|--------------|------------|-------|------|-----------------|
| 1 | $174,176,486 | $38,045,716 | 21.84% | ETH | 01:01.21 |
| 2 | $14,706,419 | $37,676,714 | 256.20% | XPL | 02:19.16 |
| 3 | $13,144,867 | $28,497,394 | 216.78% | XPL | 01:09.30 |
| 4 | $193,370,257 | $23,666,342 | 12.73% | BTC | 01:42.62 |
| 5 | $38,274,871 | $12,662,923 | 33.08% | ETH | 01:42.62 |

- Top 100 by realized PNL fire at **02:59** on average.  
- Bottom 100 fire at **03:53**.  
- Entire dataset averages **01:43**.

**Result:** Even with full leverage data, high-PNL traders are *not* first in line; they still arrive well after the average ADL timestamp.

---

## Test 2 – Are the Largest Positions Closed First?

| Rank | ADL Notional | Closed PNL | PNL % | Coin | When ADL Fired |
|------|--------------|------------|-------|------|-----------------|
| 1 | $193,370,257 | $23,666,342 | 12.73% | BTC | 01:42.62 |
| 2 | $174,176,486 | $38,045,716 | 21.84% | ETH | 01:01.21 |
| 3 | $76,396,294 | $9,252,598 | 12.60% | BTC | 03:17.42 |
| 4 | $70,601,462 | $9,755,094 | 13.82% | BTC | 03:20.49 |
| 5 | $46,653,899 | $7,497,677 | 16.07% | SOL | 01:01.21 |

- Top 100 by notional: **02:12** average.  
- Bottom 100 by notional: **01:15** average.

**Result:** Larger positions still clear *later* than the smallest ones, so notional size remains an unlikely prioritization driver.

---

## Test 3 – Does Leverage Matter Now That We Have It?

- Full-sample correlation `corr(leverage, time) = +0.006` (≈0).  
- Trimming at the 99th percentile (to remove micro-position outliers) gives `corr = −0.012`.
- Top 100 leverage events fire at **02:17**; the lowest 100 leverage events fire at **01:56**.

**Result:** Even with precise real-time account values, leverage is *not* a scheduling heuristic. High leverage trades do **not** exit meaningfully earlier than low leverage trades.

---

## Test 4 – Correlation Summary

| Metric vs Time | Pearson r | Interpretation |
|----------------|-----------|----------------|
| PNL % | +0.098 | Slightly later for higher PNL, but still weak |
| Realized PNL | +0.013 | Essentially zero |
| ADL Notional | +0.009 | Essentially zero |
| Leverage (raw) | +0.006 | Essentially zero |
| Leverage (≤99th pct) | −0.012 | Essentially zero |

No practical evidence of time-series ordering by these parameters.

---

## Test 5 – Per-Asset Matching Ratios (Top 10 by ADL Notional)

| Coin | ADL Notional | ADL Events | Liquidation Notional | Liquidation Events | ADL/Liq Ratio |
|------|--------------|------------|----------------------|--------------------|---------------|
| BTC | $620,890,948 | 2,443 | $1,789,607,764 | 5,419 | 34.7% |
| ETH | $458,008,925 | 1,498 | $1,058,159,259 | 3,462 | 43.3% |
| SOL | $276,200,961 | 3,031 | $618,098,440 | 5,563 | 44.7% |
| HYPE | $189,932,888 | 6,229 | $492,093,329 | 8,975 | 38.6% |
| XPL | $65,849,039 | 2,984 | $178,676,124 | 4,248 | 36.9% |
| PUMP | $57,293,422 | 1,868 | $147,483,588 | 3,300 | 38.8% |
| ENA | $42,494,476 | 360 | $122,705,743 | 1,246 | 34.6% |
| AVAX | $36,642,783 | 407 | $105,138,453 | 989 | 34.9% |
| FARTCOIN | $31,991,224 | 1,999 | $72,871,032 | 2,819 | 43.9% |
| XRP | $31,422,285 | 607 | $83,070,003 | 1,035 | 37.8% |

Across all 162 tickers: **mean 35.4%**, **median 33.2%**, **IQR 30.0–35.4%**. ADL continuously supplies roughly one third of the liquidation load per asset, confirming the “need-based” model first observed in the snapshot analysis.

---

## Test 6 – Repeated Targeting of Profitable Traders

| Address | ADL Events | Total Notional | Total Realized PNL | Avg PNL / ADL | Avg Leverage |
|---------|------------|----------------|--------------------|---------------|--------------|
| 0xa312114b… | 78 | $19,762,414 | $29,806,154 | $382,130 | 0.07x |
| 0xb317d2bc… | 75 | $330,448,624 | $41,449,316 | $552,658 | 0.56x |
| 0x79a2fc24… | 70 | $457,749 | $11,836 | $169 | 0.03x |
| 0x7717a7a2… | 59 | $5,105,127 | $4,351,385 | $73,752 | 0.01x |
| 0x4f7634c0… | 54 | $32,077,715 | $37,126,143 | $687,521 | 0.09x |

- Top-10 addresses average **$269,272** realized PNL per ADL.  
- The remaining 19,327 addresses average **$12,046**.  
- **Ratio:** 22× more realized gains per event among the frequently targeted cohort.

**Interpretation:** ADL continues to recycle the same profitable contra-parties, drawing on their large winning positions whenever additional liquidity is needed.

---

## Statistical Snapshot (Canonical Dataset)

| Metric | Value |
|--------|-------|
| ADL events | 34,983 |
| Unique addresses | 19,337 |
| Total ADL notional | $2,103,111,431 |
| Total realized PNL | $834,295,749 |
| Median unrealized PNL % | +50.09% |
| Median leverage (real-time) | 0.20x |
| 95th percentile leverage | 4.23x |
| 99th percentile leverage | 74.18x |
| Average ADL timestamp | 01:43 after start |

See `docs/reports/LEVERAGE_CORRECTION.md` for discussion of extreme leverage outliers (>1,000,000×) stemming from near-zero account equity.

---

## Remaining Limitations & Next Steps

- This analysis still focuses on a **single 12-minute cascade**; replaying additional market shocks would strengthen the conclusions.  
- Selection criteria inside the ADL engine remain opaque (we observe outcomes, not candidate rankings).  
- Funding/insurance thresholds were inferred from balances (`docs/findings/INSURANCE_FUND_IMPACT.md`) but not confirmed with protocol engineers.

Future work: repeat the pipeline for other cascades once clearinghouse snapshots are available, and attempt to infer the exact prioritization queue if Hyperliquid exposes more interior state.

---

## Related Canonical Notes

- `docs/findings/ADL_PRIORITIZATION_VERIFIED.md` – narrative write-up of the profitable-targeting discovery.  
- `docs/findings/INSURANCE_FUND_IMPACT.md` – quantifies the $23,191,104 insurance absorption that complements ADL.  
- `docs/findings/PER_ASSET_ISOLATION.md` – documents the per-asset batching behaviour summarized above.

---

**Answer to the original question:** even with perfect leverage and account reconstructions, ADL does **not** prioritize the “most profitable” or “largest” traders. It continues to operate as a need-based, per-asset backstop that repeatedly taps the same pool of profitable counterparties.
