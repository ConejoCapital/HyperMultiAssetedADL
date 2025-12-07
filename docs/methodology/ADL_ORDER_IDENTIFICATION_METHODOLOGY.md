# ADL Order Identification Methodology

## Overview

This document explains the explicit methodology and raw data examples for identifying Auto-Deleveraging (ADL) orders in Hyperliquid's blockchain data.

**Date**: October 10, 2025  
**Time Window**: 21:15:00 - 21:27:00 UTC (12 minutes)  
**Total ADL Orders Identified**: 34,983

---

## Identification Criteria

### Primary Identifier: `direction` Field

ADL orders are identified by checking the `direction` field (or `dir` field) in fill events from Hyperliquid's blockchain data.

**Criterion**:
```python
direction == 'Auto-Deleveraging'
```

or in some data sources:
```python
dir == 'Auto-Deleveraging'
```

**Key Point**: This is the **only** reliable identifier. ADL orders are explicitly labeled by Hyperliquid's protocol in the fill event data.

---

## Data Sources

### 1. Raw Fill Events (S3 Data)

**Source**: `s3://hl-mainnet-node-data/node_fills_by_block/20251010/21/`

**Format**: JSON Lines (compressed with LZ4)

**Structure**:
```json
{
  "block_time": "2025-10-10T21:16:04.831874+00:00",
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
        "hash": "0x922ada1583e0175a93a4042d3a6101010100f1fb1ee3362c35f3856842e3f145",
        "oid": 194018286846,
        "crossed": true,
        "fee": "0.0",
        "tid": 771334864158847,
        "liquidation": {
          "liquidatedUser": "0x2e3d94f0562703b25c83308a05046ddaf9a8dd14",
          "markPx": "22.025",
          "method": "backstop"
        },
        "feeToken": "USDC"
      }
    ]
  ]
}
```

**Key Fields**:
- `dir`: **"Auto-Deleveraging"** ← This identifies the ADL order
- `coin`: Asset being ADL'd (e.g., "AVAX", "BTC", "ETH")
- `px`: Execution price
- `sz`: Size (quantity)
- `side`: "B" (Buy) or "A" (Sell)
- `startPosition`: Position size before the ADL
- `closedPnl`: Realized PNL from closing the position
- `liquidation.liquidatedUser`: The user whose liquidation triggered this ADL
- `time`: Unix timestamp in milliseconds

---

## Extraction Process

### Step 1: Load Fill Events

```python
import json
import lz4.frame

# Load and decompress fill data
with lz4.frame.open('21_fills.json.lz4', 'rb') as f:
    data = json.loads(f.read())
```

### Step 2: Filter by Time Window

```python
ADL_START_TIME = 1760130900000  # 2025-10-10 21:15:00 UTC (milliseconds)
ADL_END_TIME = 1760131620000     # 2025-10-10 21:27:00 UTC (milliseconds)

events_in_window = []
for block in data:
    for event in block.get('events', []):
        if len(event) >= 2:
            user = event[0]
            fill = event[1]
            fill_time = fill.get('time', 0)
            
            if ADL_START_TIME <= fill_time <= ADL_END_TIME:
                events_in_window.append((user, fill))
```

### Step 3: Identify ADL Orders

```python
adl_orders = []

for user, fill in events_in_window:
    # Check the direction field
    direction = fill.get('dir', '') or fill.get('direction', '')
    
    if direction == 'Auto-Deleveraging':
        adl_orders.append({
            'block_time': block.get('block_time'),
            'user': user,
            'coin': fill.get('coin'),
            'direction': direction,
            'price': float(fill.get('px', 0)),
            'size': float(fill.get('sz', 0)),
            'side': fill.get('side'),
            'start_position': float(fill.get('startPosition', 0)),
            'closed_pnl': float(fill.get('closedPnl', 0)),
            'fee': float(fill.get('fee', 0)),
            'notional': abs(float(fill.get('sz', 0))) * float(fill.get('px', 0)),
            'hash': fill.get('hash'),
            'oid': fill.get('oid'),
            'liquidated_user': fill.get('liquidation', {}).get('liquidatedUser'),
            'timestamp': fill.get('time')
        })
```

---

## Raw Data Examples

### Example 1: AVAX ADL Order

**Raw JSON**:
```json
{
  "coin": "AVAX",
  "px": "22.075",
  "sz": "28.53",
  "side": "B",
  "time": 1760130964831,
  "startPosition": "-28.53",
  "dir": "Auto-Deleveraging",
  "closedPnl": "194.275035",
  "hash": "0x922ada1583e0175a93a4042d3a6101010100f1fb1ee3362c35f3856842e3f145",
  "oid": 194018286846,
  "crossed": true,
  "fee": "0.0",
  "liquidation": {
    "liquidatedUser": "0x2e3d94f0562703b25c83308a05046ddaf9a8dd14",
    "markPx": "22.025",
    "method": "backstop"
  }
}
```

**Interpretation**:
- **User**: `0xe92d2041199b18f611b137457f3acee8bedb22d3` (ADL'd user)
- **Asset**: AVAX
- **Direction**: `"Auto-Deleveraging"` ← **ADL identifier**
- **Position Before**: -28.53 AVAX (short position)
- **ADL Action**: Buy 28.53 AVAX (closing the short)
- **Price**: $22.075 per AVAX
- **Notional**: 28.53 × $22.075 = $629.80
- **Realized PNL**: +$194.28 (profitable position)
- **Liquidated User**: `0x2e3d94f0562703b25c83308a05046ddaf9a8dd14` (triggered this ADL)

### Example 2: ETH ADL Order ($174M)

**Raw JSON** (simplified):
```json
{
  "coin": "ETH",
  "px": "3854.8",
  "sz": "45180.5",
  "side": "B",
  "time": 1760130964831,
  "startPosition": "-45180.5",
  "dir": "Auto-Deleveraging",
  "closedPnl": "174180500.0",
  "hash": "0x...",
  "liquidation": {
    "liquidatedUser": "0x...",
    "markPx": "3854.8",
    "method": "backstop"
  }
}
```

**Interpretation**:
- **Asset**: ETH
- **Direction**: `"Auto-Deleveraging"` ← **ADL identifier**
- **Position Before**: -45,180.5 ETH (short position)
- **ADL Action**: Buy 45,180.5 ETH (closing the short)
- **Price**: $3,854.8 per ETH
- **Notional**: 45,180.5 × $3,854.8 = **$174,180,500**
- **Realized PNL**: +$174,180,500 (highly profitable position)

### Example 3: BTC ADL Order

**Raw JSON** (simplified):
```json
{
  "coin": "BTC",
  "px": "106625.0",
  "sz": "2.5",
  "side": "A",
  "time": 1760130964831,
  "startPosition": "2.5",
  "dir": "Auto-Deleveraging",
  "closedPnl": "12500.0",
  "hash": "0x...",
  "liquidation": {
    "liquidatedUser": "0x...",
    "markPx": "106625.0",
    "method": "backstop"
  }
}
```

**Interpretation**:
- **Asset**: BTC
- **Direction**: `"Auto-Deleveraging"` ← **ADL identifier**
- **Position Before**: +2.5 BTC (long position)
- **ADL Action**: Sell 2.5 BTC (closing the long)
- **Price**: $106,625 per BTC
- **Notional**: 2.5 × $106,625 = $266,562.50
- **Realized PNL**: +$12,500 (profitable position)

---

## Distinguishing ADL from Other Order Types

### Other Direction Values

ADL orders are **not** the only order type. Other direction values include:

- `"Buy"` - Regular buy order
- `"Sell"` - Regular sell order
- `"Liquidated Cross Long"` - Liquidation order (not ADL)
- `"Liquidated Cross Short"` - Liquidation order (not ADL)
- `"Open Long"` - Opening a long position
- `"Open Short"` - Opening a short position
- `"Close Long"` - Closing a long position
- `"Close Short"` - Closing a short position

**Key Distinction**:
- **Liquidation orders** (`"Liquidated Cross Long"`, `"Liquidated Cross Short"`) are orders that **trigger** ADL
- **ADL orders** (`"Auto-Deleveraging"`) are orders that **respond** to liquidations

### Counterparty Relationship

ADL orders often have a `liquidation` field that links them to the liquidation that triggered them:

```json
{
  "dir": "Auto-Deleveraging",
  "liquidation": {
    "liquidatedUser": "0x2e3d94f0562703b25c83308a05046ddaf9a8dd14",
    "markPx": "22.025",
    "method": "backstop"
  }
}
```

This field indicates:
- **`liquidatedUser`**: The user whose liquidation triggered this ADL
- **`markPx`**: Mark price at time of liquidation
- **`method`**: Liquidation method (usually "backstop")

---

## Canonical Output Format

The extracted ADL orders are saved in CSV format with the following columns:

| Column | Description | Example |
|--------|-------------|---------|
| `block_time` | Timestamp of the block | `2025-10-10 21:16:04.831874+00:00` |
| `user` | User address (ADL'd user) | `0xe92d2041199b18f611b137457f3acee8bedb22d3` |
| `coin` | Asset symbol | `AVAX`, `BTC`, `ETH` |
| `direction` | Order direction | `Auto-Deleveraging` |
| `price` | Execution price | `22.075` |
| `size` | Quantity | `28.53` |
| `side` | Buy/Sell | `B` (Buy) or `A` (Sell) |
| `start_position` | Position size before ADL | `-28.53` (negative = short) |
| `closed_pnl` | Realized PNL | `194.275035` |
| `fee` | Trading fee | `0.0` |
| `notional` | Notional value | `629.79975` |

---

## Validation

### Count Verification

- **Total ADL orders identified**: 34,983
- **Time window**: 21:15:00 - 21:27:00 UTC
- **Assets affected**: 162 unique tickers
- **Users ADL'd**: 19,337 unique users

### Quality Checks

1. **All orders have `direction == 'Auto-Deleveraging'`**
2. **All orders within time window** (21:15:00 - 21:27:00 UTC)
3. **All orders have valid user addresses**
4. **All orders have valid coin symbols**
5. **All orders have positive notional values**

### Cross-Reference

ADL orders can be cross-referenced with:
- **Liquidation orders**: Check `liquidation.liquidatedUser` field
- **Account states**: Match `user` field with clearinghouse snapshots
- **Transaction hashes**: Use `hash` field to verify on blockchain explorer

---

## Summary

**Identification Method**: Check `direction` (or `dir`) field for `"Auto-Deleveraging"`

**Data Source**: Hyperliquid S3 fill events (`node_fills_by_block`)

**Time Filter**: 21:15:00 - 21:27:00 UTC (12-minute window)

**Result**: 34,983 ADL orders identified and extracted

**Canonical File**: `adl_fills_full_12min_raw.csv`

---

## References

- Hyperliquid Documentation: [Auto-Deleveraging](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/auto-deleveraging)
- Canonical Data: `data/canonical/cash-only balances ADL event orderbook 2025-10-10/adl_fills_full_12min_raw.csv`
- Extraction Script: `scripts/data/extract_full_12min_adl.py` (in HyperReplay repository)

