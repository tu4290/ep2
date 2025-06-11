# Market Regime Analysis: ConvexValue Metrics Categorization

## Introduction

This document categorizes ConvexValue metrics based on their relevance and predictive power for different market regimes. The categorization focuses on identifying metrics that can both detect current regimes and provide actionable signals within each regime type.

## Market Regime Definitions

Before categorizing metrics, it's important to clearly define each market regime:

1. **Bullish Regime**: Characterized by sustained upward price movement with relatively low volatility, strong buying pressure, and positive sentiment. Price typically trades above key moving averages with higher lows.

2. **Bearish Regime**: Characterized by sustained downward price movement with varying volatility, strong selling pressure, and negative sentiment. Price typically trades below key moving averages with lower highs.

3. **Trending Regime**: Characterized by strong directional movement (either up or down) with momentum continuation, low mean reversion, and consistent directional flow. Can be either bullish trending or bearish trending.

4. **Choppy/Range-Bound Regime**: Characterized by price oscillation within a defined range, high mean reversion, lack of directional conviction, and balanced buying/selling pressure.

## Metric Categories for Regime Analysis

### 1. Directional Flow Metrics

These metrics reveal the balance of buying versus selling pressure and are crucial for all regime types:

- **Net Flow Metrics**: volmbs_5m, volmbs_15m, volmbs_30m, volmbs_60m, valuebs_5m, valuebs_15m, valuebs_30m, valuebs_60m, value_bs, volm_bs
- **Directional Ratios**: value_call_ratio, value_put_ratio, volm_call_ratio, volm_put_ratio, vflowratio
- **Delta-Based Flow**: deltas_buy, deltas_sell, deltas_call_buy, deltas_put_sell, deltas_call_sell, deltas_put_buy
- **Composite Flow**: flownet (Value of Call Buys + Value of Put Sells - Value of Call Sells - Value of Put Buys)

**Regime Relevance**:
- Bullish: Sustained positive values in net flow metrics
- Bearish: Sustained negative values in net flow metrics
- Trending: Strong and consistent directional bias in flow metrics
- Choppy: Oscillating values around zero with no sustained direction

### 2. Options Positioning Metrics

These metrics reveal how market participants are positioned through options, providing insight into sentiment and expected moves:

- **Greek Exposure**: dxoi, gxoi, vxoi, txoi, call_dxoi, put_dxoi, call_gxoi, put_gxoi
- **Greek Flow**: dxvolm, gxvolm, vannaxvolm, vommaxvolm, charmxvolm
- **Put/Call Metrics**: put_call_ratio, value_call_bs, value_put_bs, volm_call_bs, volm_put_bs

**Regime Relevance**:
- Bullish: High call_dxoi, low put_call_ratio, positive value_call_bs
- Bearish: High put_dxoi, high put_call_ratio, positive value_put_bs
- Trending: Consistent directional bias in Greek exposure metrics
- Choppy: Balanced Greek exposures with no clear directional bias

### 3. Volatility Regime Metrics

These metrics help identify the volatility component of market regimes:

- **Volatility Metrics**: volatility, front_volatility, back_volatility
- **Volatility Derivatives**: vanna, vomma, charm
- **Volatility Exposure**: vannaxoi, vommaxoi, charmxoi, vxoi

**Regime Relevance**:
- Bullish: Moderate to low volatility with positive vanna
- Bearish: Elevated volatility with negative vanna
- Trending: Consistent volatility pattern (either increasing or decreasing)
- Choppy: Oscillating volatility with mean reversion in vanna and vomma

### 4. Market Structure Metrics

These metrics reveal the underlying market structure that defines regimes:

- **Liquidity Metrics**: bid_size, ask_size, spread
- **Open Interest Metrics**: oi, oi_ch
- **Price Action Metrics**: day_high_price, day_low_price, day_open_price, day_close_price, tick_direction

**Regime Relevance**:
- Bullish: Increasing oi, tight spreads, higher day_close_price vs day_open_price
- Bearish: Decreasing oi, widening spreads, lower day_close_price vs day_open_price
- Trending: Consistent oi_ch direction, persistent tick_direction bias
- Choppy: Oscillating oi_ch, alternating tick_direction, price contained within range

### 5. Cross-Asset Correlation Metrics

These metrics involve comparing data across different assets to identify regime characteristics:

- **Index vs. Sector Comparison**: Comparing flow metrics between broad market (SPY/SPX) and sector ETFs
- **Equity vs. VIX Relationship**: Comparing equity flow with VIX-related metrics
- **Cross-Market Flows**: Comparing flows across related markets (e.g., ES futures vs. SPY options)

**Regime Relevance**:
- Bullish: Positive correlation in bullish flows across related assets
- Bearish: Positive correlation in bearish flows across related assets
- Trending: Strong flow alignment across related assets
- Choppy: Divergent or uncorrelated flows across related assets

### 6. Time-Series Transformation Metrics

These are derived metrics that transform the raw data to reveal regime characteristics:

- **Rate of Change**: Calculating the first derivative of flow metrics
- **Acceleration**: Calculating the second derivative of flow metrics
- **Mean Reversion**: Measuring deviation from moving averages of flow metrics
- **Cumulative Metrics**: Running sum of intraday flow metrics

**Regime Relevance**:
- Bullish: Positive and stable rate of change in bullish flow metrics
- Bearish: Negative and stable rate of change in bullish flow metrics
- Trending: Consistent sign in both rate of change and acceleration
- Choppy: Oscillating rate of change with mean reversion tendencies

## Conclusion

This categorization provides a framework for identifying the most relevant ConvexValue metrics for each market regime. The next step is to select and justify the top 5 metrics or combinations for each regime, focusing on those that provide the most predictive power and actionable signals.
