# ADL Net Volume Analysis

**Analysis of Auto-Deleveraging (ADL) net volume by ticker on October 10, 2025**

---

## 📊 Quick Summary

**Event**: October 10, 2025 Market Crash  
**Time Window Analyzed**: 21:15:00 - 21:17:00 UTC (2-minute sample)  
**Data Source**: SonarX (blockchain-verified ADL events)

### Key Findings

| Metric | Value |
|--------|-------|
| **Total Assets ADL'd** | 65 tickers |
| **Total ADL Events** | 14,194 events |
| **Total Net Notional** | $285.5M |
| **Total Realized PNL** | $142.1M |

### Top 3 ADL'd Assets

1. **HYPE** - $137.0M notional (48.0% of total)
2. **PUMP** - $30.0M notional (10.5% of total)
3. **XPL** - $20.6M notional (7.2% of total)

---

## 📁 Files in This Folder

| File | Description |
|------|-------------|
| **README.md** | This file - Overview |
| **ADL_NET_VOLUME_REPORT.md** | Detailed analysis report |
| **adl_net_volume_by_ticker.csv** | Raw data (CSV) |
| **calculate_adl_volume.py** | Python script used for analysis |

---

## 🎯 What is ADL Net Volume?

**Auto-Deleveraging (ADL)** is Hyperliquid's mechanism to manage liquidations during extreme market volatility:

1. When a position is liquidated but can't be closed by the liquidation engine
2. The protocol **force-closes** the most profitable opposing positions
3. This is called "Auto-Deleveraging" (ADL)

**Net Volume** = Sum of all position sizes that were ADL'd per ticker

**Net Notional** = Sum of (position size × price) for all ADL'd positions

---

## 🔍 Key Insights

### Market Concentration
- **Top 3 tickers** account for 65.7% of total ADL volume
- **HYPE alone** represents 48% of all ADL'd notional value
- **Meme coins** (PUMP, FARTCOIN) heavily represented

### Asset Distribution
- **65 different tickers** experienced ADL events
- **Major assets**: HYPE, PUMP, XPL, ENA, FARTCOIN
- **Established coins**: LINK, ENS, AVAX also affected

### Profitability
- **$142.1M** in realized PNL from ADL'd positions
- **Average PNL per ticker**: $2.2M
- **Most profitable**: XPL ($24.6M), FARTCOIN ($22.3M), HYPE ($38.8M)

---

## ⚠️ Important Limitations

### Time Coverage
This analysis covers **only 2 minutes** (21:15-21:17 UTC) of the full ADL event:
- **Full event window**: 21:15-21:27 UTC (12 minutes)
- **Scaling factor**: Multiply by ~6x for full event estimate
- **Estimated full notional**: ~$1.7 billion

### Data Quality
✅ **Blockchain-verified**: Only fills with `DIR = "Auto-Deleveraging"`  
✅ **Spot positions excluded**: @ tokens filtered out  
✅ **No heuristics**: Explicit blockchain labels only

---

## 📊 Top 10 ADL'd Tickers

| Rank | Ticker | Net Notional | # Events | Total PNL |
|------|--------|--------------|----------|-----------|
| 1 | HYPE | $137.0M | 5,441 | $38.8M |
| 2 | PUMP | $30.0M | 1,647 | $11.5M |
| 3 | XPL | $20.6M | 2,744 | $24.6M |
| 4 | ENA | $16.2M | 32 | $11.6M |
| 5 | FARTCOIN | $15.8M | 1,456 | $22.3M |
| 6 | IP | $7.8M | 203 | $3.6M |
| 7 | PENGU | $6.4M | 165 | $3.4M |
| 8 | LINK | $5.7M | 91 | $2.1M |
| 9 | LINEA | $4.6M | 140 | $2.6M |
| 10 | ENS | $4.4M | 96 | $1.9M |

---

## 🔬 Methodology

### Data Source
- **File**: `SonarX Hyperliquid node_fills_20251010_2115_2117.csv`
- **Total fills**: 290,992
- **ADL fills**: 14,194
- **Filtered**: Excluded @ tokens (spot positions)

### Calculations
```python
# Net Volume per ticker
net_volume = sum(size) for all ADL events per ticker

# Net Notional per ticker
net_notional = sum(size × price) for all ADL events per ticker

# Total Realized PNL per ticker
total_pnl = sum(closed_pnl) for all ADL events per ticker
```

### Filters Applied
1. **Direction = "Auto-Deleveraging"** (blockchain label)
2. **Exclude tickers starting with "@"** (spot positions)
3. **Time window**: 21:15:00 - 21:17:00 UTC

---

## 📈 Usage

### View Results

**Quick view** (CSV):
```bash
open adl_net_volume_by_ticker.csv
```

**Detailed report** (Markdown):
```bash
open ADL_NET_VOLUME_REPORT.md
```

### Rerun Analysis
```bash
python3 calculate_adl_volume.py
```

### Load in Python
```python
import pandas as pd

df = pd.read_csv('adl_net_volume_by_ticker.csv')
print(df.head())

# Total ADL notional
print(f"Total: ${df['net_notional_usd'].sum():,.0f}")

# Top 5 tickers
print(df.nlargest(5, 'net_notional_usd'))
```

---

## 🎓 For Academic Research

### Suitable For
- ✅ ADL mechanism analysis
- ✅ Market concentration studies
- ✅ Liquidity crisis behavior
- ✅ Cross-asset ADL impact
- ✅ Meme coin vs. established coin analysis

### Citation
```
ADL Net Volume Analysis (2025). "Auto-Deleveraging Volume by Ticker: 
October 10, 2025 Market Event." 
Data: SonarX Hyperliquid node_fills (blockchain-verified ADL events).
```

---

## 📧 Questions?

For questions about:
- **This analysis**: See `ADL_NET_VOLUME_REPORT.md`
- **Methodology**: See `calculate_adl_volume.py`
- **Full event analysis**: See `../HyperAnalyzeADL` repository

---

## 🔗 Related Analysis

- **Main ADL Analysis**: `~/Desktop/ADL Clean/` (BTC & SOL positions)
- **GitHub Repository**: https://github.com/ConejoCapital/HyperAnalyzeADL
- **Data Verification**: `~/Desktop/SonarX Data Verification/`

---

**Analysis Date**: November 7, 2025  
**Data Quality**: ⭐⭐⭐⭐⭐ (Blockchain-verified)  
**Time Coverage**: 2-minute sample (21:15-21:17 UTC)  
**Full Event**: Multiply by ~6x for 12-minute total

