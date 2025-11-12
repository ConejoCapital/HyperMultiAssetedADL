# Insurance Fund Impact - October 10, 2025 Cascade

## 💰 Executive Summary

**First-ever quantification of insurance fund coverage required during a Hyperliquid ADL cascade.**

### The Numbers

| Metric | Value |
|--------|-------|
| **Accounts in negative equity** | **886** |
| **Total negative equity** | **-$128,608,070.32** |
| **Insurance fund coverage required** | **$128.6M** |
| **% of ADL'd accounts underwater** | **2.71%** |
| **Largest underwater account** | -$7.4M |
| **Average underwater account** | -$145,219 |

---

## 🔬 Methodology: Real-Time Account Reconstruction

This analysis is the first to reconstruct account states in **real-time** during a cascade, enabling accurate detection of negative equity at the exact ADL moment.

### Data Processing

**Input Data:**
- **Clearinghouse snapshot** (Block 758750000, 20:04:54 UTC)
  - 437,356 accounts with account values
  - $5.1B total account value
  - 70 minutes before cascade
  
- **Event stream** (20:04:54 - 21:20:00 UTC)
  - 2,611,504 events processed
  - Fills (with `closedPnl`)
  - Funding events
  - Deposits/Withdrawals
  - ADL events
  - Liquidation events

### Real-Time Reconstruction Process

For each of 437,356 accounts, we reconstructed account state chronologically:

```python
# Start with snapshot
account_value = snapshot_account_values[user]

# Process every event chronologically
for event in sorted_events:
    if event.type == 'fill':
        account_value += event.closedPnl
        account_value -= event.fee
        update_position(event)
    
    elif event.type == 'funding':
        account_value += event.funding_amount
    
    elif event.type == 'deposit':
        account_value += event.amount
    
    elif event.type == 'withdrawal':
        account_value -= event.amount
    
    # Calculate unrealized PNL for ALL positions
    unrealized_pnl = sum(
        calculate_pnl(position, last_price[coin])
        for coin, position in user_positions.items()
    )
    
    # Total equity = cash + unrealized PNL
    total_equity = account_value + unrealized_pnl
    
    # Detect negative equity
    if total_equity < 0:
        insurance_fund_impact += abs(total_equity)
```

### Key Innovation

**Previous analyses** used snapshot values (70 minutes stale)  
**This analysis** reconstructs account values at **every moment** during the cascade

This enables:
- ✅ Precise leverage ratios at ADL moment
- ✅ Accurate negative equity detection
- ✅ Insurance fund impact quantification
- ✅ Real-time risk assessment

---

## 📊 Negative Equity Distribution

### By Size

| Equity Range | # Accounts | Total Negative Equity |
|--------------|------------|----------------------|
| $0 to -$10k | 234 | -$1.2M |
| -$10k to -$50k | 312 | -$9.8M |
| -$50k to -$100k | 156 | -$11.4M |
| -$100k to -$500k | 142 | -$38.7M |
| -$500k to -$1M | 28 | -$19.8M |
| < -$1M | 14 | -$47.7M |

**Top 14 accounts** (< -$1M each) account for **37% of total insurance impact**.

### Timeline of Negative Equity Emergence

Negative equity accounts emerged in waves as the cascade progressed:

| Time Range | New Underwater Accounts | Cumulative |
|------------|-------------------------|------------|
| 21:15:00 - 21:16:00 | 142 | 142 |
| 21:16:01 - 21:17:00 | 387 | 529 |
| 21:17:01 - 21:18:00 | 224 | 753 |
| 21:18:01 - 21:20:00 | 133 | 886 |

**Peak underwater rate**: 21:16:00 - 21:17:00 (387 accounts went negative in 60 seconds)

---

## 🎯 What This Reveals About ADL Mechanics

### 1. ADL Prioritizes Profit, Not Risk

Even with 886 accounts underwater, ADL targeted **profitable positions** (96.7% of ADL'd positions were profitable).

**Why?**
- Insurance fund covers losses from underwater accounts
- ADL extracts profit from winners to offset those losses
- System design: socialize losses via profitable counterparties

### 2. Insurance Fund as First Line of Defense

```
Liquidation cascade begins
  ↓
Some accounts go negative (can't cover losses)
  ↓
Insurance fund absorbs negative equity
  ↓
ADL activates to replenish insurance fund
  ↓
Profitable positions force-closed
  ↓
Proceeds restore insurance fund
```

**This cascade required $128.6M in insurance fund coverage.**

If insurance fund balance was < $128.6M → loss socialization to all traders would occur.

### 3. Leverage vs Underwater Status

| Leverage Range | % ADL'd | % Underwater |
|----------------|---------|--------------|
| < 1x | 52.3% | 1.8% |
| 1x - 2x | 18.4% | 2.4% |
| 2x - 5x | 21.2% | 3.9% |
| 5x - 10x | 6.1% | 5.7% |
| > 10x | 2.0% | 8.2% |

**Even low-leverage accounts** went underwater during this cascade, though higher leverage correlated with higher underwater probability.

---

## 🚨 Implications for Traders

### What This Means for You

**If you're profitable during a cascade:**
- ✅ You're an ADL target (even at 0.16x median leverage)
- ✅ Your profits will be used to cover underwater accounts
- ✅ This is not a bug—it's the system design

**If you're underwater during a cascade:**
- ⚠️ Your negative equity goes to insurance fund
- ⚠️ If insurance fund depleted → losses socialize to all traders
- ⚠️ No recourse—losses are final

**Risk Management:**
- 📉 Low leverage ≠ immunity from negative equity in extreme moves
- 📉 Insurance fund size = maximum loss socialization buffer
- 📉 During cascades, even conservative positions can go underwater

---

## 📁 Data Access

**Complete analysis available:**

```bash
# Download from GitHub
git clone https://github.com/ConejoCapital/HyperMultiAssetedADL.git
cd HyperMultiAssetedADL

# Load real-time analysis
import pandas as pd
df = pd.read_csv('adl_detailed_analysis_REALTIME.csv')

# Find underwater accounts
underwater = df[df['is_negative_equity'] == True]
print(f"Underwater accounts: {len(underwater):,}")
print(f"Total insurance impact: ${underwater['total_equity'].sum():,.2f}")
```

**Key Files:**
- `adl_detailed_analysis_REALTIME.csv` - 32,673 ADL events with real-time metrics
- `full_analysis_realtime.py` - Complete reconstruction methodology
- `realtime_analysis_summary.json` - Summary statistics

---

## 🔬 Technical Details

### Account Value Reconstruction Formula

```python
# Starting state (from snapshot)
account_value = snapshot_account_values[user]
positions = snapshot_positions[user]

# Update through time
for event in chronological_events:
    # 1. Update cash from realized PNL
    if event.type == 'fill':
        account_value += event.closedPnl - event.fee
        positions[event.coin] = event.startPosition
    
    # 2. Update cash from funding
    elif event.type == 'funding':
        account_value += event.funding_amount
    
    # 3. Update cash from deposits/withdrawals
    elif event.type in ['deposit', 'withdrawal', 'transfer']:
        account_value += event.amount
    
    # 4. Calculate unrealized PNL
    for coin, position in positions.items():
        current_price = last_traded_price[coin]
        entry_price = position.entry_price
        
        if position.size > 0:  # Long
            unrealized_pnl = position.size * (current_price - entry_price)
        else:  # Short
            unrealized_pnl = abs(position.size) * (entry_price - current_price)
    
    # 5. Total equity
    total_equity = account_value + sum(unrealized_pnl for all positions)
    
    # 6. Detect negative equity
    if total_equity < 0:
        is_underwater = True
        insurance_impact = abs(total_equity)
```

### Validation

**Cross-checks performed:**
- ✅ Account value changes match `closedPnl` sum
- ✅ Position sizes match `startPosition` from fills
- ✅ Unrealized PNL calculated using last traded price
- ✅ Total equity = account_value + total_unrealized_pnl
- ✅ Negative equity detected only when total equity < 0

**Limitations:**
- Mark price vs last traded price (may differ slightly)
- Funding rate updates between events (approximated)
- Position entry price for pre-snapshot positions (calculated from fills)

---

## 🎓 Research Significance

### First-Ever Achievements

1. **Real-time account reconstruction** during a DeFi cascade
2. **Insurance fund impact quantification** ($128.6M)
3. **Negative equity detection** at exact ADL moment (886 accounts)
4. **Risk pool analysis** showing 2.71% underwater rate

### Future Research Directions

- [ ] Compare insurance fund impact across different cascade sizes
- [ ] Analyze relationship between underwater % and cascade severity
- [ ] Model insurance fund depletion risk
- [ ] Study loss socialization mechanisms when insurance fund insufficient
- [ ] Compare with other protocols (dYdX, GMX, Synthetix)

---

## 📖 Citation

```
Insurance Fund Impact Analysis (2025). "Real-Time Account Reconstruction:
Quantifying Negative Equity in the October 10, 2025 Hyperliquid Cascade."
Data: Clearinghouse snapshot (Block 758750000) + 2.6M chronological events.
Method: Real-time account value reconstruction through event replay.
Key Finding: 886 accounts underwater, $128.6M insurance fund coverage required.
```

---

## 📞 Contact & Contributions

**Questions?** Open an issue on GitHub: [HyperMultiAssetedADL](https://github.com/ConejoCapital/HyperMultiAssetedADL)

**Improvements?** Pull requests welcome!

**Hyperliquid Team:** If you'd like to validate or correct any findings, please reach out.

---

**Generated**: November 12, 2025  
**Analysis Period**: October 10, 2025, 21:15:00 - 21:20:00 UTC  
**Data Source**: Hyperliquid blockchain + clearinghouse snapshot

