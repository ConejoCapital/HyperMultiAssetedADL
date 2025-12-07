# Verification: Are Losing Positions Labeled as ADL?

**Date**: December 7, 2025  
**Question**: According to researcher, both sides of an ADL event get labeled as "Auto-Deleveraging". Is this true?

---

## ✅ VERIFICATION RESULT: NO

**Conclusion**: Losing positions are **NOT** labeled as "Auto-Deleveraging". They are labeled as "Liquidated" instead.

---

## Analysis Results

### ADL Events Analysis

**Source**: Raw S3 data (`node_fills_20251010_21.lz4`)  
**Total ADL Events**: 34,983  
**Filter**: `direction == "Auto-Deleveraging"`

**Findings**:
- ✅ **100%** of ADL events have `liquidation_data` (34,983 / 34,983)
- ✅ **100%** of ADL events have `liquidated_user` (34,983 / 34,983)
- ✅ **0%** have `user == liquidated_user` (0 / 34,983) - **NO losing positions**
- ✅ **100%** have `user != liquidated_user` (34,983 / 34,983) - **ALL winning positions**

### Liquidations Analysis

**Source**: `liquidations_full_12min.csv`  
**Total Liquidation Events**: 63,637

**Findings**:
- ✅ **0%** labeled as "Auto-Deleveraging" (0 / 63,637)
- ✅ **100%** labeled as "Liquidated" variants:
  - "Liquidated Isolated Long"
  - "Liquidated Isolated Short"
  - etc.

### Cross-Verification

**User Overlap Check**:
- ADL users: 19,337 unique users
- Liquidation users: 63,637 unique users
- Users in BOTH: Some users appear in both (different positions/coins)

**Key Insight**: A user can be:
- Liquidated on one position (labeled "Liquidated")
- ADL'd on a different position (labeled "Auto-Deleveraging")

But the **same position** cannot be both liquidated AND ADL'd.

---

## What This Means

### ADL Labeling

**"Auto-Deleveraging" label is ONLY for winning positions**:
- The position providing liquidity (counterparty to liquidation)
- The position being force-closed to cover losses
- Always: `user != liquidated_user`

**"Liquidated" label is for losing positions**:
- The position that was underwater and got liquidated
- The position that triggered the ADL mechanism
- Always: `user == liquidated_user` (in liquidation events)

### The ADL Mechanism

```
Liquidation Event:
  User A (losing position) → Labeled: "Liquidated Isolated Long/Short"
  User B (winning position) → Labeled: "Auto-Deleveraging"
  
Both fills happen at the same timestamp, but:
- User A's fill has direction = "Liquidated..."
- User B's fill has direction = "Auto-Deleveraging"
```

---

## Researcher's Statement vs Reality

### Researcher's Claim
> "Both sides have their fill labeled as ADL"

### Reality
❌ **INCORRECT**

**Actual Behavior**:
- **Losing position** (liquidated user): Labeled as **"Liquidated"**
- **Winning position** (ADL'd user): Labeled as **"Auto-Deleveraging"**

### Why the Confusion?

The researcher may have been confused because:
1. Both fills happen at the **same timestamp**
2. Both fills are part of the **same ADL mechanism**
3. Both fills reference each other (via `liquidated_user` field)
4. But they have **different direction labels**

---

## Data Evidence

### ADL Events (34,983)
```
Direction: "Auto-Deleveraging"
User type: 100% winning positions (user != liquidated_user)
Closed PNL: Average +$23,848 (profitable)
```

### Liquidation Events (63,637)
```
Direction: "Liquidated Isolated Long/Short" (NOT "Auto-Deleveraging")
User type: 100% losing positions (user == liquidated_user in liquidation context)
Closed PNL: Average -$9,555 (losses)
```

---

## Conclusion

✅ **VERIFIED**: Losing positions are **NOT** labeled as "Auto-Deleveraging"

- All ADL events (`direction == "Auto-Deleveraging"`) are winning positions
- All liquidation events (`direction == "Liquidated..."`) are losing positions
- The labels are **mutually exclusive** and correctly identify the position type

**Our analysis is correct**: We only capture winning positions when filtering for `direction == "Auto-Deleveraging"`.

---

## Recommendation

If the researcher insists that losing positions are labeled as ADL, we should:
1. Ask them to provide a specific example (user, timestamp, coin)
2. Check if they're looking at a different data source
3. Verify if there's a different field or label we're missing

But based on our comprehensive analysis of the raw S3 data, **losing positions are NOT labeled as ADL**.

