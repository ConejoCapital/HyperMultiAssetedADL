# Repository Organization

**Last Updated**: December 7, 2025

This document describes the organization of the HyperMultiAssetedADL repository.

---

## Directory Structure

```
HyperMultiAssetedADL/
├── README.md                    # Main repository overview
├── .gitignore                   # Git ignore rules
│
├── docs/                        # All documentation
│   ├── methodology/            # Methodology and how-to guides
│   │   ├── COMPLETE_METHODOLOGY.md
│   │   ├── ACCOUNT_BALANCE_RECONSTRUCTION_METHODOLOGY.md
│   │   └── ADL_ORDER_IDENTIFICATION_METHODOLOGY.md
│   │
│   ├── findings/               # Research findings and discoveries
│   │   ├── ADL_PRIORITIZATION_VERIFIED.md
│   │   ├── ADL_PRIORITIZATION_ANALYSIS_LOCAL.md
│   │   ├── PER_ASSET_ISOLATION.md
│   │   ├── ADL_MECHANISM_RESEARCH.md
│   │   ├── INSURANCE_FUND_IMPACT.md
│   │   └── HIGH_LEVERAGE_OUTLIERS_EXPLANATION.md
│   │
│   ├── analysis/               # Analysis reports
│   │   ├── TOTAL_IMPACT_ANALYSIS.md
│   │   ├── CASCADE_TIMING_ANALYSIS.md
│   │   ├── BATCH_PROCESSING_DISCOVERY.md
│   │   └── ...
│   │
│   └── reports/                # Verification and audit reports
│       ├── BUG_FIX_SUMMARY.md
│       ├── POSITION_SIZE_BUG_FIX.md
│       ├── PARTIAL_CLOSURE_VERIFICATION.md
│       ├── LOSING_POSITIONS_ADL_VERIFICATION.md
│       ├── RESEARCHER_FEEDBACK_ANALYSIS.md
│       ├── BUG_FIX_COMPARISON.md
│       ├── FINDINGS_VERIFICATION_REPORT.md
│       ├── AUDIT_REPORT.md
│       └── LEVERAGE_CORRECTION.md
│
├── scripts/                     # All Python scripts
│   ├── analysis/               # Analysis scripts (9 scripts)
│   │   ├── adl_prioritization_analysis.py
│   │   ├── adl_prioritization_local.py
│   │   ├── adl_mechanism_analysis.py
│   │   ├── cascade_timing_analysis.py
│   │   ├── batch_processing_analysis.py
│   │   ├── per_asset_isolation.py
│   │   ├── insurance_fund_impact.py
│   │   ├── adl_net_volume.py
│   │   ├── total_impact_analysis.py
│   │   └── outputs/            # Analysis script JSON outputs
│   │
│   ├── data/                   # Data extraction scripts
│   │   ├── extract_full_12min_adl.py
│   │   └── analyze_clearinghouse.py
│   │
│   ├── reconstruction/         # Account reconstruction scripts
│   │   └── full_analysis_realtime.py
│   │
│   └── verification/           # Verification and testing scripts
│       ├── verify_all_findings.py
│       ├── check_losing_positions_adl.py
│       └── check_partial_adl.py
│
└── data/                        # All data files
    ├── canonical/               # Canonical processed data
    │   └── cash-only balances ADL event orderbook 2025-10-10/
    │       ├── adl_detailed_analysis_REALTIME.csv
    │       ├── adl_by_user_REALTIME.csv
    │       ├── adl_by_coin_REALTIME.csv
    │       ├── adl_fills_full_12min_raw.csv
    │       ├── liquidations_full_12min.csv
    │       ├── adl_net_volume_full_12min.csv
    │       ├── realtime_analysis_summary.json
    │       ├── ADL_NET_VOLUME_FULL_12MIN.md
    │       └── README.md
    │
    └── raw/                     # Raw analysis outputs
        ├── ADL_ORDERS_COMPLETE_LIST.csv
        └── high_leverage_outliers_analysis.csv
```

---

## File Organization Principles

### Documentation (`docs/`)
- **methodology/**: Step-by-step guides on how to reproduce the analysis
- **findings/**: Research discoveries and key insights
- **analysis/**: Detailed analysis reports for specific topics
- **reports/**: Verification reports, bug fixes, and audit documents

### Scripts (`scripts/`)
- **analysis/**: Scripts that analyze the canonical data and generate insights
  - **outputs/**: JSON outputs from analysis scripts (regenerated on demand)
- **data/**: Scripts that extract data from raw sources
- **reconstruction/**: Scripts that reconstruct account states from events
- **verification/**: Scripts that verify findings and test data integrity

### Data (`data/`)
- **canonical/**: The authoritative, corrected datasets used for all analysis
- **raw/**: Raw analysis outputs and intermediate data files

---

## What's NOT in the Repository

The following are intentionally excluded (via `.gitignore`):
- Large raw data files (`*_fills.json`, `*_misc.json`)
- Snapshot files (`account_value_snapshot_*.json`, `perp_positions_*.json`)
- Compressed data files (`*.lz4`)
- Python cache files (`__pycache__/`, `*.pyc`)
- Log files (`*.log`)

These files are too large for GitHub and should be stored locally or in cloud storage.

---

## Key Files for Researchers

### Getting Started
1. **README.md** - Start here for overview
2. **docs/methodology/COMPLETE_METHODOLOGY.md** - Complete methodology guide

### Core Data
- `data/canonical/cash-only balances ADL event orderbook 2025-10-10/adl_detailed_analysis_REALTIME.csv` - Main dataset (34,983 ADL events)

### Key Findings
- `docs/findings/ADL_PRIORITIZATION_VERIFIED.md` - ADL targets profit, not leverage
- `docs/findings/PER_ASSET_ISOLATION.md` - Zero cross-asset ADL contagion
- `docs/analysis/TOTAL_IMPACT_ANALYSIS.md` - Complete cascade impact

### Verification
- `scripts/verification/verify_all_findings.py` - Comprehensive verification suite

---

## Maintenance

When adding new files:
- **Documentation** → Place in appropriate `docs/` subdirectory
- **Scripts** → Place in appropriate `scripts/` subdirectory
- **Data** → Place in `data/canonical/` or `data/raw/` as appropriate
- **Analysis outputs** → Place in `scripts/analysis/outputs/`

Keep the root directory clean - only `README.md` and `.gitignore` should be at the root level.

