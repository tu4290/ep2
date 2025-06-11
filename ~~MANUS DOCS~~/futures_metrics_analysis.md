# ConvexValue Futures Metrics Analysis for ES (E-mini S&P 500)

## Introduction

This document analyzes ConvexValue data parameters specifically for ES futures trading, focusing on identifying the most impactful metrics for price action. Unlike options-heavy instruments like SPX, futures trading is more straightforward with direct buying and selling (raw deltas), though there are still options components to consider.

## Categorization of Available Metrics

The ConvexValue data parameters can be categorized as follows:

### 1. Market Data Metrics
- Price metrics (bid_price, ask_price, price, day_open_price, day_high_price, day_low_price, day_close_price)
- Volume metrics (day_volume, volm, volm_5m, volm_15m, volm_30m, volm_60m)
- Liquidity metrics (bid_size, ask_size, spread)
- Market activity indicators (tick_direction, change)

### 2. Directional Flow Metrics
- Delta-based metrics (deltas, deltas_buy, deltas_sell, dxvolm)
- Buy/sell imbalance metrics (volm_bs, volmbs_5m, volmbs_15m, volmbs_30m, volmbs_60m)
- Value-based metrics (value_bs, valuebs_5m, valuebs_15m, valuebs_30m, valuebs_60m)

### 3. Options-Related Metrics
- Greek exposure metrics (gammas, vegas, thetas, rhos)
- Open interest metrics (oi, oi_ch, dxoi, gxoi)
- Options flow metrics (value_call_bs, value_put_bs, volm_call_bs, volm_put_bs)
- Options ratio metrics (value_call_ratio, value_put_ratio, volm_call_ratio, volm_put_ratio)

### 4. Time-Based Metrics
- Intraday metrics (metrics with 5m, 15m, 30m, 60m suffixes)
- Day-based metrics (metrics with day_ prefix)
- Historical comparison metrics (prev_day_ prefix metrics)

## Analysis of Metrics for Futures Trading

For ES futures specifically, the most relevant metrics will focus on:

1. **Direct price impact** - Metrics that show immediate buying/selling pressure
2. **Liquidity dynamics** - Metrics that reveal market depth and potential for price movement
3. **Institutional positioning** - Metrics that indicate large player activity
4. **Short-term momentum** - Metrics that capture developing trends
5. **Options influence** - Metrics that show how options positioning affects futures price

Unlike equity options, futures have standardized contract sizes and more direct hedging relationships, making raw flow metrics particularly important.
