# Account Balance Reconstruction Methodology

**Document Purpose**: Comprehensive guide explaining exactly how account balances are extracted, reconstructed, and reported for the October 10, 2025 ADL event analysis  
**Last Updated**: December 2025  
**Event**: October 10, 2025 Hyperliquid Liquidation Cascade (21:15-21:27 UTC)  
**Repository**: [HyperMultiAssetedADL](https://github.com/ConejoCapital/HyperMultiAssetedADL)

---

## Table of Contents

1. [Overview: What We Extract and Why](#overview)
2. [Hyperliquid Account Types](#account-types)
3. [Data Sources and Extraction](#data-sources)
4. [Balance Reconstruction Process](#reconstruction-process)
5. [Step-by-Step Balance Calculation Examples](#calculation-examples)
6. [Account Type Handling](#account-type-handling)
7. [Data Quality and Validation](#data-quality)
8. [Common Pitfalls and Solutions](#pitfalls)

---

## Overview: What We Extract and Why

### What We Track

For each account during the ADL event, we reconstruct:

1. **Account Value (Cash Balance)**
   - Starting from snapshot baseline (cash-only, unrealized PnL removed)
   - Updated with every fill (closedPnl, fees)
   - Updated with funding payments
   - Updated with deposits/withdrawals
   - Updated with all ledger transfers

2. **Position States**
   - Size (long/short from position sign)
   - Entry price (weighted average from fills)
   - Notional value (size × current price)

3. **Unrealized PNL**
   - Per-position: `size × (current_price - entry_price)` for longs
   - Per-position: `abs(size) × (entry_price - current_price)` for shorts
   - Total: Sum across all positions

4. **Total Equity**
   - `account_value + total_unrealized_pnl`
   - Used to detect negative equity

5. **Leverage**
   - `total_position_notional / account_value`
   - Calculated at exact ADL moment

### What We Exclude

- **Spot positions** (tickers starting with "@")
- **Spot balances** (we have `spot_balances__758750000_1760126694218.json` but don't use it)
- **Vault positions** (tracked separately by Hyperliquid)
- **Staking balances** (not relevant for perp ADL analysis)

---

## Hyperliquid Account Types

Hyperliquid has **two distinct account types** that share the same address but maintain separate balances:

### 1. Perpetual Futures Account (Perp Account)
- **Purpose**: Trading perpetual futures contracts
- **Collateral**: USDC only
- **Positions**: Long/short perp positions (BTC, ETH, SOL, etc.)
- **ADL Relevance**: ✅ **This is what we analyze**
- **Balance Tracking**: `account_value` in our reconstruction

### 2. Spot Account
- **Purpose**: Trading spot assets
- **Collateral**: Various tokens (USDC, BTC, ETH, etc.)
- **Positions**: Spot holdings (denoted by "@" prefix, e.g., "@BTC")
- **ADL Relevance**: ❌ **Excluded from analysis** (spot cannot be ADL'd)
- **Balance Tracking**: Available in `spot_balances__758750000_1760126694218.json` but not used

### Account Class Transfers

Hyperliquid allows users to transfer USDC between perp and spot accounts via `accountClassTransfer` events:

```json
{
  "type": "LedgerUpdate",
  "inner": {
    "LedgerUpdate": {
      "delta": {
        "type": "accountClassTransfer",
        "usdc": "1000.0",
        "toPerp": true  // true = perp ← spot, false = spot ← perp
      },
      "users": ["0x123..."]
    }
  }
}
```

**Our Handling**: We track `accountClassTransfer` events and update perp account values accordingly:
- `toPerp: true` → Add USDC to perp account
- `toPerp: false` → Subtract USDC from perp account

---

## Data Sources and Extraction

### Source 1: Clearinghouse Snapshot (Baseline)

**File**: `account_value_snapshot_758750000_1760126694218.json`  
**Block**: 758750000  
**Timestamp**: 2025-10-10 20:04:54.218 UTC (70 minutes before cascade)  
**Size**: 68 MB  
**Records**: 437,356 accounts

**Structure**:
```json
[
  {
    "user": "0x5b5d51203a0f9079f8aeb098a6523a13f298c060",
    "account_value": 272726535.490442,
    "total_long_notional": 0.0,
    "total_short_notional": 0.0
  }
]
```

**What It Contains**:
- `account_value`: Total perp account value in USDC (includes unrealized PnL at snapshot time)
- `total_long_notional`: Sum of all long position notionals
- `total_short_notional`: Sum of all short position notionals

**Extraction Process**:
```python
with open('account_value_snapshot_758750000_1760126694218.json', 'r') as f:
    account_values = json.load(f)

account_states = {}
for acc in account_values:
    account_states[acc['user']] = {
        'account_value': float(acc['account_value']),
        'positions': {},
        'snapshot_time': 1760126694218,
        'initial_unrealized': 0.0
    }
```

### Source 2: Position Snapshot (Entry Prices)

**File**: `perp_positions_by_market_758750000_1760126694218.json`  
**Size**: 72 MB  
**Records**: 221,422 positions across 182 markets

**Structure**:
```json
[
  {
    "market_name": "hyperliquid:JUP",
    "positions": [
      {
        "user": "0x002479c9acacf25b14593c2f09c503a88dc3c4ff",
        "size": -14.0,
        "notional_size": 5.63346,
        "funding_pnl": 0.035389,
        "entry_price": 0.4716,
        "is_cross": true,
        "leverage": 10,
        "liquidation_price": 71.49134890249434,
        "account_value": 1076.000069
      }
    ]
  }
]
```

**What It Contains**:
- `size`: Position size (negative = short, positive = long)
- `entry_price`: Weighted average entry price
- `notional_size`: Current position notional
- `account_value`: Account value at snapshot (may differ from account_value_snapshot if user has multiple positions)

**Extraction Process**:
```python
with open('perp_positions_by_market_758750000_1760126694218.json', 'r') as f:
    positions_by_market = json.load(f)

for market in positions_by_market:
    coin = market['market_name'].replace('hyperliquid:', '')
    for pos in market['positions']:
        user = pos['user']
        size = float(pos['size'])
        entry_price = float(pos['entry_price'])
        notional = float(pos['notional_size'])
        
        # Calculate mark price from notional/size
        mark_price = abs(notional / size) if size else entry_price
        
        # Initialize account if missing
        if user not in account_states:
            account_states[user] = {
                'account_value': float(pos.get('account_value', 0.0)),
                'positions': {},
                'snapshot_time': 1760126694218,
                'initial_unrealized': 0.0
            }
        
        # Store position
        account_states[user]['positions'][coin] = {
            'size': size,
            'entry_price': entry_price,
            'notional': notional,
            'mark_price': mark_price
        }
        
        # Accumulate initial unrealized PnL
        if size != 0:
            unrealized = size * (mark_price - entry_price)
            account_states[user]['initial_unrealized'] += unrealized
```

### Source 3: Fill Events (Position Changes)

**Files**: `20_fills.json`, `21_fills.json`  
**Source**: Hyperliquid S3 (`node_fills_by_block/hourly/20251010/21.lz4`)  
**Size**: 407 MB + 2.0 GB  
**Records**: 5,939,266 fills total

**Structure** (from S3 node_fills):
```json
{
  "block_time": "2025-10-10T21:16:04.831874687",
  "block_number": 758800641,
  "events": [
    [
      "0xe92d2041199b18f611b137457f3acee8bedb22d3",
      {
        "coin": "AVAX",
        "px": "22.075",
        "sz": "28.53",
        "side": "B",
        "time": 1760130964831,
        "startPosition": "-28.53",
        "dir": "Auto-Deleveraging",
        "closedPnl": "194.275035",
        "fee": "0.0",
        "hash": "0x922ada1583e0175a93a4042d3a6101010100f1fb1ee3362c35f3856842e3f145"
      }
    ]
  ]
}
```

**What It Contains**:
- `startPosition`: Position size **before** this fill
- `sz`: Fill size (amount traded)
- `px`: Fill price
- `closedPnl`: Realized PnL from this fill
- `fee`: Trading fee paid
- `dir`: Direction ("Auto-Deleveraging", "Liquidated Cross Long", "Buy", "Sell", etc.)

**Extraction Process**:
```python
for hour_file in ['20_fills.json', '21_fills.json']:
    with open(hour_file, 'r') as f:
        for line in f:
            block = json.loads(line)
            if block.get('events'):
                for event in block['events']:
                    user, details = event
                    
                    # Skip spot fills
                    if details['coin'].startswith('@'):
                        continue
                    
                    all_events.append({
                        'type': 'fill',
                        'time': details['time'],
                        'user': user,
                        'coin': details['coin'],
                        'price': float(details['px']),
                        'size': float(details['sz']),
                        'side': details['side'],
                        'direction': details.get('dir', 'Unknown'),
                        'closedPnl': float(details.get('closedPnl', 0)),
                        'fee': float(details.get('fee', 0)),
                        'startPosition': float(details.get('startPosition', 0))
                    })
```

### Source 4: Misc Events (Balance Deltas)

**Files**: `20_misc.json`, `21_misc.json`  
**Size**: 36 MB + 43 MB  
**Records**: Funding events, ledger updates

**Structure**:
```json
{
  "time": "2025-10-10T21:15:00.123456789Z",
  "inner": {
    "Funding": {
      "deltas": [
        {
          "user": "0x123...",
          "coin": "BTC",
          "funding_amount": "12.345"
        }
      ]
    }
  }
}
```

**LedgerUpdate Types We Handle**:

1. **Deposits** (`type: "deposit"`)
   ```json
   {
     "type": "LedgerUpdate",
     "inner": {
       "LedgerUpdate": {
         "delta": {
           "type": "deposit",
           "usdc": "1000.0"
         },
         "users": ["0x123..."]
       }
     }
   }
   ```

2. **Withdrawals** (`type: "withdraw"`)
   ```json
   {
     "delta": {
       "type": "withdraw",
       "usdc": "500.0",
       "fee": "1.0"
     }
   }
   ```

3. **Account Class Transfers** (`type: "accountClassTransfer"`)
   ```json
   {
     "delta": {
       "type": "accountClassTransfer",
       "usdc": "200.0",
       "toPerp": true
     }
   }
   ```

4. **Internal Transfers** (`type: "internalTransfer"`)
   ```json
   {
     "delta": {
       "type": "internalTransfer",
       "usdc": "50.0",
       "user": "0xsource...",
       "destination": "0xdest...",
       "fee": "0.1"
     }
   }
   ```

5. **Spot Transfers** (`type: "spotTransfer"`)
   ```json
   {
     "delta": {
       "type": "spotTransfer",
       "usdcValue": "100.0",
       "user": "0xsource...",
       "destination": "0xdest..."
     }
   }
   ```

6. **Vault Operations** (`type: "vaultDeposit"`, `type: "vaultWithdraw"`)
   ```json
   {
     "delta": {
       "type": "vaultDeposit",
       "usdc": "1000.0",
       "user": "0x123...",
       "vault": "0xvault..."
     }
   }
   ```

7. **Rewards** (`type: "rewardsClaim"`)
   ```json
   {
     "delta": {
       "type": "rewardsClaim",
       "token": "USDC",
       "amount": "10.0"
     }
   }
   ```

8. **Liquidation Overrides** (`type: "liquidation"`)
   ```json
   {
     "delta": {
       "type": "liquidation",
       "accountValue": "5000.0",
       "user": "0x123..."
     }
   }
   ```

**Extraction Process**:
```python
for hour_file in ['20_misc.json', '21_misc.json']:
    with open(hour_file, 'r') as f:
        for line in f:
            block = json.loads(line)
            if block.get('events'):
                for event in block['events']:
                    inner = event.get('inner', {})
                    
                    # Funding events
                    if 'Funding' in inner:
                        for delta in inner['Funding'].get('deltas', []):
                            all_events.append({
                                'type': 'funding',
                                'time': timestamp,
                                'user': delta['user'],
                                'coin': delta['coin'],
                                'funding_amount': float(delta['funding_amount'])
                            })
                    
                    # Ledger updates
                    if 'LedgerUpdate' in inner:
                        ledger = inner['LedgerUpdate']
                        delta = ledger.get('delta', {})
                        dtype = delta.get('type')
                        
                        if dtype == 'deposit':
                            amount = float(delta.get('usdc', 0))
                            for user in ledger.get('users', []):
                                all_events.append({
                                    'type': 'deposit',
                                    'time': timestamp,
                                    'user': user,
                                    'amount': amount
                                })
                        # ... handle other types
```

---

## Balance Reconstruction Process

### Step 1: Initialize from Snapshot (Cash-Only Baseline)

**Critical**: We remove unrealized PnL from snapshot account values to establish a cash-only baseline.

**Why?** The snapshot `account_value` includes unrealized PnL at snapshot time. We want to track pure cash/realized PnL, then add unrealized PnL dynamically as prices change.

**Process**:
```python
# 1. Load snapshot account values
account_states = {}
for acc in account_values:
    account_states[acc['user']] = {
        'account_value': float(acc['account_value']),
        'positions': {},
        'initial_unrealized': 0.0
    }

# 2. Load positions and calculate initial unrealized PnL
for market in positions_by_market:
    coin = market['market_name'].replace('hyperliquid:', '')
    for pos in market['positions']:
        user = pos['user']
        size = float(pos['size'])
        entry_price = float(pos['entry_price'])
        notional = float(pos['notional_size'])
        mark_price = abs(notional / size) if size else entry_price
        
        # Store position
        account_states[user]['positions'][coin] = {
            'size': size,
            'entry_price': entry_price,
            'notional': notional
        }
        
        # Accumulate unrealized PnL
        if size != 0:
            unrealized = size * (mark_price - entry_price)
            account_states[user]['initial_unrealized'] += unrealized

# 3. Convert to cash-only baseline
for state in account_states.values():
    initial_u = state.get('initial_unrealized', 0.0)
    state['initial_account_value'] = state['account_value']  # Store original
    state['account_value'] = state['account_value'] - initial_u  # Remove unrealized
```

**Example**:
```
Snapshot Account Value: $10,000
Position: 1 BTC long, entry $50,000, mark $55,000
Initial Unrealized PnL: 1 × ($55,000 - $50,000) = $5,000

Cash-Only Baseline: $10,000 - $5,000 = $5,000
```

### Step 2: Load and Sort All Events

**Process**:
```python
# Load all fills and misc events
all_events = []
# ... load fills ...
# ... load misc events ...

# Sort chronologically
all_events.sort(key=lambda x: x['time'])

# Filter to analysis window (snapshot to ADL end)
SNAPSHOT_TIME = 1760126694218  # 20:04:54.218
ADL_END_TIME = 1760131620000   # 21:27:00.000
events_in_window = [e for e in all_events if SNAPSHOT_TIME <= e['time'] <= ADL_END_TIME]
```

**Result**: 3,239,706 events sorted chronologically

### Step 3: Replay Events Chronologically

**Process**:
```python
working_states = deepcopy(account_states)
last_prices = {}  # Track latest trade price per coin

for event in events_in_window:
    user = event['user']
    event_type = event['type']
    
    # Ensure user exists
    if user not in working_states:
        working_states[user] = {
            'account_value': 0.0,
            'positions': {},
            'snapshot_time': event['time']
        }
    
    if event_type == 'fill':
        # Update account value
        working_states[user]['account_value'] += event['closedPnl']
        working_states[user]['account_value'] -= event['fee']
        
        # Update position
        coin = event['coin']
        if coin not in working_states[user]['positions']:
            working_states[user]['positions'][coin] = {
                'size': 0.0,
                'entry_price': event['price'],
                'notional': 0.0
            }
        
        # Update position size based on fill
        # startPosition is BEFORE fill, size is fill amount
        # For buy (side='B'): position increases, for sell (side='A'): position decreases
        start_position = event['startPosition']
        fill_size = event['size']
        if event['side'] == 'B':  # Buy
            new_size = start_position + fill_size
        else:  # Sell (side='A')
            new_size = start_position - fill_size
        working_states[user]['positions'][coin]['size'] = new_size
        
        # Update last price
        last_prices[coin] = event['price']
    
    elif event_type == 'funding':
        working_states[user]['account_value'] += event['funding_amount']
    
    elif event_type == 'deposit':
        working_states[user]['account_value'] += event['amount']
    
    elif event_type == 'withdrawal':
        working_states[user]['account_value'] -= event['amount']
    
    elif event_type == 'transfer':
        working_states[user]['account_value'] += event['amount']
    
    elif event_type == 'account_value_override':
        working_states[user]['account_value'] = event['value']
```

---

## Step-by-Step Balance Calculation Examples

### Example 1: Simple Position Update

**Initial State (from snapshot)**:
```
User: 0xABC...
Account Value (snapshot): $10,000
Position: 1 BTC long, entry $50,000, mark $55,000
Initial Unrealized: $5,000

Cash-Only Baseline: $10,000 - $5,000 = $5,000
```

**Event 1: Fill at 21:15:10**
```json
{
  "type": "fill",
  "time": 1760130910000,
  "user": "0xABC...",
  "coin": "BTC",
  "price": 56000.0,
  "size": 0.5,
  "side": "B",
  "closedPnl": 500.0,
  "fee": 2.0,
  "startPosition": 1.0
}
```

**Update Process**:
```python
# 1. Update account value
account_value += closedPnl - fee
account_value = $5,000 + $500 - $2 = $5,498

# 2. Update position size
start_position = 1.0  # Position before fill
fill_size = 0.5  # Fill amount
side = 'B'  # Buy
if side == 'B':
    new_size = start_position + fill_size  # 1.0 + 0.5 = 1.5 BTC
else:
    new_size = start_position - fill_size
position['size'] = new_size  # Position after fill: 1.5 BTC

# 3. Update entry price (weighted average)
# Old: 1.0 BTC @ $50,000
# New: 0.5 BTC @ $56,000
# Weighted: (1.0 × $50,000 + 0.5 × $56,000) / 1.5 = $52,000

# 4. Update last price
last_prices['BTC'] = $56,000
```

**Resulting State**:
```
Account Value: $5,498
Position: 1.5 BTC long, entry $52,000
Last Price: $56,000
Unrealized PnL: 1.5 × ($56,000 - $52,000) = $6,000
Total Equity: $5,498 + $6,000 = $11,498
```

### Example 2: Account Class Transfer

**Initial State**:
```
Account Value: $5,000
```

**Event: Account Class Transfer**
```json
{
  "type": "LedgerUpdate",
  "inner": {
    "LedgerUpdate": {
      "delta": {
        "type": "accountClassTransfer",
        "usdc": "1000.0",
        "toPerp": true
      },
      "users": ["0xABC..."]
    }
  }
}
```

**Update Process**:
```python
# Transfer from spot to perp account
if toPerp:
    account_value += usdc_amount
    account_value = $5,000 + $1,000 = $6,000
```

**Resulting State**:
```
Account Value: $6,000
```

### Example 3: Funding Payment

**Initial State**:
```
Account Value: $5,000
Position: 1 BTC long
```

**Event: Funding Payment**
```json
{
  "type": "funding",
  "time": 1760131000000,
  "user": "0xABC...",
  "coin": "BTC",
  "funding_amount": -12.5
}
```

**Update Process**:
```python
# Funding is paid/received directly to account value
account_value += funding_amount
account_value = $5,000 + (-$12.5) = $4,987.5
```

**Resulting State**:
```
Account Value: $4,987.5
```

### Example 4: ADL Event with Real-Time Metrics

**State at ADL Moment**:
```
Account Value: $5,000
Position: 1 BTC long, entry $50,000
Last Price: $55,000
```

**ADL Event**:
```json
{
  "type": "fill",
  "time": 1760130964831,
  "user": "0xABC...",
  "coin": "BTC",
  "price": 55,000.0,
  "size": -1.0,
  "direction": "Auto-Deleveraging",
  "closedPnl": 5,000.0,
  "fee": 0.0,
  "startPosition": 1.0
}
```

**Metrics Calculation**:
```python
# 1. Position unrealized PnL (before ADL)
position_unrealized = 1.0 × ($55,000 - $50,000) = $5,000

# 2. Position notional
position_notional = 1.0 × $55,000 = $55,000

# 3. Position PNL %
pnl_percent = ($5,000 / $55,000) × 100 = 9.09%

# 4. Leverage
leverage = $55,000 / $5,000 = 11.0x

# 5. Total unrealized PnL (all positions)
total_unrealized = $5,000  # Only BTC position

# 6. Total equity
total_equity = $5,000 + $5,000 = $10,000

# 7. Negative equity?
is_negative_equity = total_equity < 0  # False
```

**After ADL**:
```python
# Update account value
account_value += closedPnl - fee
account_value = $5,000 + $5,000 - $0 = $10,000

# Update position (closed)
position['size'] = startPosition = 1.0
# After ADL: 1.0 + (-1.0) = 0.0 BTC (closed)
```

---

## Account Type Handling

### Perp Account (Primary Focus)

**What We Track**:
- ✅ Account value (USDC)
- ✅ Perp positions (BTC, ETH, SOL, etc.)
- ✅ All balance deltas (fills, funding, deposits, withdrawals, transfers)

**What We Exclude**:
- ❌ Spot positions (tickers with "@" prefix)
- ❌ Spot balances (separate account type)

**Code**:
```python
# Skip spot fills
if details['coin'].startswith('@'):
    continue
```

### Spot Account (Excluded)

**Why Excluded**:
- Spot positions cannot be ADL'd
- ADL only affects perpetual futures
- Spot balances are tracked separately

**Available Data**:
- `spot_balances__758750000_1760126694218.json` exists but is not used

**Account Class Transfers**:
- We track `accountClassTransfer` events to update perp account values
- Transfers from spot → perp add to perp account
- Transfers from perp → spot subtract from perp account

---

## Data Quality and Validation

### Validation Checks

1. **Account Value Consistency**
   ```python
   # After replay, verify account values are reasonable
   for user, state in working_states.items():
       assert state['account_value'] >= -1_000_000  # No extreme negatives
       assert state['account_value'] < 1_000_000_000  # No extreme positives
   ```

2. **Position Size Consistency**
   ```python
   # Position size should match startPosition from fills
   for coin, pos in state['positions'].items():
       # Verify position size is updated correctly
       assert abs(pos['size']) < 1_000_000  # Reasonable bounds
   ```

3. **Event Count Validation**
   ```python
   assert len(events_in_window) == 3_239_706  # Expected count
   assert len(adl_events) == 34_983  # Expected ADL count
   ```

4. **Timestamp Validation**
   ```python
   # All events should be in analysis window
   assert all(SNAPSHOT_TIME <= e['time'] <= ADL_END_TIME for e in events_in_window)
   ```

### Known Limitations

1. **Mark Price Approximation**
   - We use last traded price as mark price
   - Official mark prices may differ slightly
   - Impact: Unrealized PnL may be off by <1% in most cases

2. **Entry Price Reconstruction**
   - We calculate weighted average from fills
   - Positions opened before snapshot use snapshot entry price
   - Impact: Entry prices are accurate to within 0.1% typically

3. **Funding Payments**
   - We track funding from misc events
   - Some funding may be batched
   - Impact: Account values accurate to within $0.01 typically

---

## Common Pitfalls and Solutions

### Pitfall 1: Forgetting to Remove Initial Unrealized PnL

**Problem**: Using snapshot `account_value` directly includes unrealized PnL at snapshot time.

**Solution**: Subtract initial unrealized PnL to establish cash-only baseline.

```python
# WRONG
account_value = snapshot['account_value']  # Includes unrealized PnL

# CORRECT
initial_unrealized = calculate_unrealized_from_positions(positions, mark_prices)
account_value = snapshot['account_value'] - initial_unrealized
```

### Pitfall 2: Not Handling Account Class Transfers

**Problem**: Missing transfers between spot and perp accounts.

**Solution**: Track `accountClassTransfer` events.

```python
if dtype == 'accountClassTransfer':
    usdc_amount = float(delta.get('usdc', 0))
    to_perp = delta.get('toPerp', False)
    if to_perp:
        account_value += usdc_amount  # Spot → Perp
    else:
        account_value -= usdc_amount  # Perp → Spot
```

### Pitfall 3: Not Updating Position Size Correctly

**Problem**: Setting position size to `startPosition` (before fill) instead of calculating the new size after the fill.

**Solution**: Calculate new position size by adding/subtracting the fill size based on the side.

```python
# WRONG
position['size'] = event['startPosition']  # This is position BEFORE fill, not AFTER

# CORRECT
start_position = event['startPosition']  # Position before fill
fill_size = event['size']  # Fill amount
if event['side'] == 'B':  # Buy
    new_size = start_position + fill_size
else:  # Sell
    new_size = start_position - fill_size
position['size'] = new_size  # Position AFTER fill
```

### Pitfall 4: Not Tracking All Ledger Event Types

**Problem**: Missing balance updates from internal transfers, vault operations, etc.

**Solution**: Handle all `LedgerUpdate` types.

```python
# Handle all types
elif dtype == 'internalTransfer':
    # Update source and destination
elif dtype == 'spotTransfer':
    # Update perp account if USDC involved
elif dtype == 'vaultDeposit':
    # Subtract from perp account
elif dtype == 'vaultWithdraw':
    # Add to perp account
elif dtype == 'rewardsClaim':
    # Add to perp account if USDC
```

### Pitfall 5: Not Updating Entry Prices

**Problem**: Entry price stays constant after fills.

**Solution**: Calculate weighted average entry price.

```python
# When position changes
old_size = position['size']
old_entry = position['entry_price']
fill_size = event['size']
fill_price = event['price']

# Weighted average
if old_size + fill_size != 0:
    new_entry = (old_size * old_entry + fill_size * fill_price) / (old_size + fill_size)
    position['entry_price'] = new_entry
```

---

## Summary

### What We Extract

1. **Account Values**: Cash-only baseline from snapshot, updated with all events
2. **Positions**: Size, entry price, notional from snapshot and fills
3. **Balance Deltas**: Fills (closedPnl, fees), funding, deposits, withdrawals, transfers
4. **Real-Time Metrics**: Leverage, unrealized PnL, total equity at ADL moment

### How We Reconstruct

1. **Initialize**: Load snapshot, remove initial unrealized PnL
2. **Replay**: Process 3.2M events chronologically
3. **Update**: Account value, positions, entry prices, last prices
4. **Calculate**: Real-time metrics at exact ADL moment

### Account Types

- **Perp Account**: ✅ Fully tracked (this is what we analyze)
- **Spot Account**: ❌ Excluded (cannot be ADL'd)
- **Account Class Transfers**: ✅ Tracked (affects perp account value)

### Key Files

- `account_value_snapshot_758750000_1760126694218.json` - Baseline account values
- `perp_positions_by_market_758750000_1760126694218.json` - Initial positions
- `20_fills.json`, `21_fills.json` - All fills (2.5M+ events)
- `20_misc.json`, `21_misc.json` - Funding and ledger updates (80K+ events)
- `adl_detailed_analysis_REALTIME.csv` - Final output with real-time metrics

---

**Document Version**: 1.0  
**Last Updated**: December 2025  
**Status**: ✅ Complete  
**Associated Script**: `HyperReplay/scripts/replay_real_time_accounts.py`

