# Total Impact Analysis: Liquidations + ADL (October 10, 2025)

> Associated script: `analysis_scripts/total_impact_analysis.py`

---

## 🔥 TOTAL IMPACT SUMMARY

### Combined Statistics

| Metric | Liquidations | ADL | **TOTAL IMPACT** |
|--------|--------------|-----|------------------|
| **Events** | 63,637 | 34,983 | **98,620** |
| **Net Notional** | $5,511,042,925 | $2,103,111,431 | **$7,614,154,356** |
| **Total PNL** | $-607,907,145 | $834,295,749 | **$226,388,604** |
| **Unique Tickers** | 171 | 162 | **171** |

### Key Findings

**💰 Total Market Impact**: **$7.61B** in forced position closures

**📊 Breakdown**:
- **Liquidations**: 72.4% ($5,511,042,925)
- **Auto-Deleveraging (ADL)**: 27.6% ($2,103,111,431)

**🎯 Event Rate**:
- **98,620 total events** in 12 minutes
- **Average**: 8218 events per minute
- **Peak**: ~137.0 events per second

---

## 📊 LIQUIDATIONS (Detailed)

**Total Liquidated**: $5,511,042,925  
**Total Events**: 63,637  
**Realized PNL**: $-607,907,145

### Top 20 Liquidated Tickers

| Rank | Ticker | Net Notional | # Events | Total PNL | % of Total |
|------|--------|--------------|----------|-----------|------------|
| 31 | BTC | $1,789,607,764 | 5,419 | $-48,960,745 | 32.5% |
| 47 | ETH | $1,058,159,259 | 3,462 | $-62,989,691 | 19.2% |
| 123 | SOL | $618,098,440 | 5,563 | $-48,903,702 | 11.2% |
| 62 | HYPE | $492,093,329 | 8,975 | $-48,478,563 | 8.9% |
| 155 | XPL | $178,676,124 | 4,248 | $-60,119,468 | 3.2% |
| 109 | PUMP | $147,483,588 | 3,300 | $-30,822,701 | 2.7% |
| 44 | ENA | $122,705,743 | 1,246 | $-50,306,625 | 2.2% |
| 18 | AVAX | $105,138,453 | 989 | $-22,520,758 | 1.9% |
| 16 | ASTER | $86,368,570 | 2,465 | $-20,108,789 | 1.6% |
| 156 | XRP | $83,070,003 | 1,035 | $-17,515,713 | 1.5% |
| 49 | FARTCOIN | $72,871,032 | 2,819 | $-28,699,449 | 1.3% |
| 159 | ZEC | $66,918,683 | 896 | $-3,087,806 | 1.2% |
| 79 | LTC | $65,844,050 | 689 | $-7,670,773 | 1.2% |
| 78 | LINK | $63,905,377 | 1,221 | $-8,753,015 | 1.2% |
| 38 | DOGE | $52,836,035 | 507 | $-17,941,752 | 1.0% |
| 129 | SUI | $40,061,701 | 952 | $-7,854,137 | 0.7% |
| 87 | MNT | $28,048,756 | 527 | $-5,766,147 | 0.5% |
| 69 | IP | $27,374,620 | 344 | $-3,905,296 | 0.5% |
| 133 | TAO | $25,566,049 | 665 | $-5,177,573 | 0.5% |
| 43 | EIGEN | $24,685,558 | 266 | $-9,642,065 | 0.4% |


---

## 🎯 AUTO-DELEVERAGING (ADL) - Detailed

**Total ADL'd**: $2,103,111,431  
**Total Events**: 34,983  
**Realized PNL**: $834,295,749

### Top 20 ADL'd Tickers

| Rank | Ticker | Net Notional | # Events | Total PNL | % of Total |
|------|--------|--------------|----------|-----------|------------|
| 29 | BTC | $620,890,948 | 2,443 | $72,834,224 | 29.5% |
| 45 | ETH | $458,008,925 | 1,498 | $110,553,425 | 21.8% |
| 118 | SOL | $276,200,961 | 3,031 | $69,136,518 | 13.1% |
| 59 | HYPE | $189,932,888 | 6,229 | $51,665,287 | 9.0% |
| 147 | XPL | $65,849,039 | 2,984 | $119,388,213 | 3.1% |
| 105 | PUMP | $57,293,422 | 1,868 | $31,523,223 | 2.7% |
| 42 | ENA | $42,494,476 | 360 | $50,203,244 | 2.0% |
| 17 | AVAX | $36,642,783 | 407 | $23,779,339 | 1.7% |
| 47 | FARTCOIN | $31,991,224 | 1,999 | $68,272,961 | 1.5% |
| 148 | XRP | $31,422,285 | 607 | $13,342,514 | 1.5% |
| 15 | ASTER | $27,183,536 | 431 | $15,384,169 | 1.3% |
| 74 | LINK | $21,522,161 | 259 | $12,555,116 | 1.0% |
| 75 | LTC | $21,130,168 | 197 | $6,682,417 | 1.0% |
| 150 | ZEC | $18,910,183 | 400 | $2,537,940 | 0.9% |
| 36 | DOGE | $16,487,948 | 249 | $10,539,485 | 0.8% |
| 124 | SUI | $13,366,242 | 442 | $9,885,987 | 0.6% |
| 98 | PENGU | $10,586,142 | 372 | $9,165,467 | 0.5% |
| 83 | MNT | $10,115,188 | 211 | $5,580,602 | 0.5% |
| 65 | IP | $9,347,850 | 270 | $6,369,495 | 0.4% |
| 128 | TAO | $8,664,279 | 167 | $5,847,182 | 0.4% |


---

## 🔍 COMBINED TOP 10 TICKERS (By Total Impact)


| Rank | Ticker | Liquidations | ADL | **TOTAL IMPACT** | Events | Total PNL |
|------|--------|--------------|-----|------------------|--------|-----------|
| 122 | BTC | $1,789,607,764 | $620,890,948 | **$2,410,498,711** | 7,862 | $23,873,479 |
| 106 | ETH | $1,058,159,259 | $458,008,925 | **$1,516,168,184** | 4,960 | $47,563,734 |
| 111 | SOL | $618,098,440 | $276,200,961 | **$894,299,401** | 8,594 | $20,232,815 |
| 71 | HYPE | $492,093,329 | $189,932,888 | **$682,026,217** | 15,204 | $3,186,724 |
| 26 | XPL | $178,676,124 | $65,849,039 | **$244,525,164** | 7,232 | $59,268,745 |
| 73 | PUMP | $147,483,588 | $57,293,422 | **$204,777,010** | 5,168 | $700,522 |
| 137 | ENA | $122,705,743 | $42,494,476 | **$165,200,219** | 1,606 | $-103,381 |
| 163 | AVAX | $105,138,453 | $36,642,783 | **$141,781,235** | 1,396 | $1,258,581 |
| 59 | XRP | $83,070,003 | $31,422,285 | **$114,492,288** | 1,642 | $-4,173,199 |
| 24 | ASTER | $86,368,570 | $27,183,536 | **$113,552,105** | 2,896 | $-4,724,620 |


---

## 📈 Market Concentration

**Top 3 Assets** (BTC, ETH, SOL):

- **BTC**: $2,410,498,711 (31.7%)
- **ETH**: $1,516,168,184 (19.9%)
- **SOL**: $894,299,401 (11.7%)

**Combined Top 3**: $4,820,966,296 (63.3% of total impact)

**Top 10 Assets**: $6,487,320,535 (85.2% of total)

---

## 🎓 For Academic Research

### Research Value

This dataset represents the **most complete picture** of a major liquidation cascade event:

1. **Scale**: $7.61 billion in forced closures
2. **Speed**: 98,620 events in 12 minutes
3. **Coverage**: All 171 affected tickers
4. **Quality**: 100% blockchain-verified

### Key Questions This Answers

1. **What triggers ADL?** Compare liquidation timeline vs ADL timeline
2. **How much loss was socialized?** ADL represents counterparty failures
3. **Which assets cascaded?** Track liquidations → ADL by asset
4. **System effectiveness?** Protocol handled $7.61B in 12 minutes

---

## 🔬 Methodology

### Data Source
- **File**: `node_fills_20251010_21.lz4` (Hyperliquid S3)
- **Total fills processed**: 1.42M fills in time window
- **Liquidations**: Fills with "Liquidated" in direction field
- **ADL**: Fills with "Auto-Deleveraging" in direction field
- **Exclusions**: @ tokens (spot positions)

### Categorization
- **100% blockchain-verified**: Uses explicit labels from chain
- **No heuristics**: Direct categorization from fill metadata
- **Complete dataset**: Full 12-minute window analyzed

### Calculations
- **Net Notional**: Sum of (size × price) for all events
- **Total PNL**: Sum of realized PNL from forced closures
- **Event counts**: Number of individual fill events

---

## ✅ Data Quality

✅ **Complete**: Full 12-minute event (not sampled)  
✅ **Verified**: Blockchain labels only (no guessing)  
✅ **Comprehensive**: Both liquidations AND ADL  
✅ **Multi-asset**: All 171 affected tickers  
✅ **Reproducible**: Code and methodology provided

---

## 📁 Files Generated

1. **TOTAL_IMPACT_ANALYSIS.md** - This comprehensive report
2. **liquidations_full_12min.csv** - All 63,637 liquidation events
3. **adl_fills_full_12min_raw.csv** - All 34,983 ADL events
4. **combined_impact_by_ticker.csv** - Ticker-level summary

---

## 🚀 Key Takeaways

### The Cascade Effect

1. **Initial Liquidations**: $5,511,042,925 (63,637 events)
2. **Subsequent ADL**: $2,103,111,431 (34,983 events)
3. **Total Market Impact**: $7,614,154,356

### Speed of Event

- **Duration**: 12 minutes
- **Event rate**: 8218 per minute
- **Peak activity**: ~137.0 events per second

### Asset Concentration

- **Top 3**: 63.3% of total impact
- **Top 10**: 85.2% of total impact
- **Long tail**: 161 other assets affected

---

**Generated**: 2025-11-08 14:50:47  
**Source**: Hyperliquid S3 (node_fills_20251010_21.lz4)  
**Analysis**: Total Impact Calculator (Liquidations + ADL)
