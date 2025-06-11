# Top 5 Metrics for Trending Market Regime

## Introduction

A trending market regime is characterized by strong directional movement (either up or down) with momentum continuation, low mean reversion, and consistent directional flow. Unlike purely bullish or bearish regimes, the trending regime focuses on the strength and sustainability of the directional move regardless of direction. The following five metric combinations provide maximum predictive power for identifying and trading trending markets.

## Core Metrics (Top 3)

### 1. Directional Momentum Strength Index (DMSI)

**Formula:**
```
DMSI = abs(normalized_volmbs_15m) * (1 + directional_consistency_factor) * (1 + flow_acceleration_factor)
```
Where:
- `normalized_volmbs_15m` = volmbs_15m / 20-day average absolute value of volmbs_15m
- `directional_consistency_factor` = abs(correlation between volmbs_5m, volmbs_15m, and volmbs_30m)
- `flow_acceleration_factor` = abs((current volmbs_15m / 3-day average of volmbs_15m) - 1)

**Impact Score: 9.8/10**

**Justification:**
- Measures the absolute strength of directional momentum regardless of direction
- The normalized volume component captures the magnitude of directional pressure
- The directional consistency factor ensures alignment across multiple timeframes
- The flow acceleration factor identifies increasing momentum that drives strong trends
- Particularly powerful for identifying high-conviction trending environments
- Works equally well for both uptrends and downtrends

**Application:**
- DMSI > 1.5: Strong trending environment likely to continue
- DMSI > 2.0: Powerful trend with significant momentum
- DMSI acceleration: Trend likely gaining strength
- DMSI > 2.5: Extremely strong trend suitable for aggressive trend-following strategies

**Cross-Ticker Enhancement:**
Comparing DMSI between related instruments (e.g., SPY, QQQ, and IWM) provides insight into market breadth within the trending regime. When multiple major indices show strong DMSI readings, the trend has broader market support and is more likely to continue.

### 2. Options Skew Trend Confirmation (OSTC)

**Formula:**
```
OSTC = sign(price_change_5day) * (abs(call_put_skew_ratio - historical_average) * (1 + vanna_alignment_factor))
```
Where:
- `price_change_5day` = percentage price change over the last 5 days
- `call_put_skew_ratio` = (call_gxoi / put_gxoi) for uptrends or (put_gxoi / call_gxoi) for downtrends
- `historical_average` = 20-day average of call_put_skew_ratio
- `vanna_alignment_factor` = correlation between vannaxoi and price direction over past 5 days

**Impact Score: 9.6/10**

**Justification:**
- Measures how options positioning is confirming the current trend direction
- The sign component ensures the metric is positive when options skew confirms the price trend
- The skew ratio deviation from historical average reveals unusual positioning
- The vanna alignment factor adds weight when volatility-sensitive delta exposure supports the trend
- Particularly effective at identifying trends with strong options market support
- Excellent for distinguishing between sustainable trends and short-term fluctuations

**Application:**
- OSTC > 1.0: Options market confirming the current trend
- OSTC > 1.5: Strong options market confirmation of trend
- OSTC increasing while price trending: Strengthening conviction in trend continuation
- OSTC < 0: Options market positioning contradicting the price trend (warning sign)

**Cross-Ticker Enhancement:**
Comparing OSTC between the underlying asset and related volatility products provides insight into volatility expectations within the trending regime. For example, comparing SPY OSTC with VIX options positioning can reveal whether the options market expects the trend to continue with stable or changing volatility.

### 3. Institutional Trend Participation Index (ITPI)

**Formula:**
```
ITPI = sign(price_change_5day) * (normalized_value_bs * 0.4 + normalized_dxvolm * 0.3 + oi_trend_factor * 0.3)
```
Where:
- `price_change_5day` = percentage price change over the last 5 days
- `normalized_value_bs` = value_bs / 20-day average absolute value of value_bs
- `normalized_dxvolm` = dxvolm / 20-day average absolute value of dxvolm
- `oi_trend_factor` = (current oi / 5-day average oi - 1) * 10

**Impact Score: 9.4/10**

**Justification:**
- Captures institutional participation in the current trend
- The sign component ensures the metric is positive when institutional flow aligns with the price trend
- The normalized value component reveals capital commitment to the trend
- The normalized delta-volume component shows directional conviction
- The open interest trend factor identifies new position building that supports trend continuation
- Particularly effective at identifying trends with strong institutional backing
- Excellent for distinguishing between retail-driven moves and institutional trends

**Application:**
- ITPI > 1.0: Institutional participation supporting the current trend
- ITPI > 1.5: Strong institutional backing of the trend
- ITPI increasing while price trending: Institutions increasing participation in the trend
- ITPI < 0: Institutional positioning contradicting the price trend (warning sign)

**Cross-Ticker Enhancement:**
Comparing ITPI between large caps and small caps provides insight into the breadth of institutional participation. When both SPY and IWM show strong ITPI readings, the trend has broader institutional support across market capitalizations.

## Complementary Metrics (Additional 2)

### 4. Trend Sustainability Index (TSI)

**Formula:**
```
TSI = (1 - mean_reversion_factor) * (1 + gamma_reinforcement_factor) * (1 + volatility_trend_alignment)
```
Where:
- `mean_reversion_factor` = absolute correlation between price returns and subsequent reversals over past 10 days
- `gamma_reinforcement_factor` = correlation between price direction and gamma exposure changes over past 5 days
- `volatility_trend_alignment` = sign(price_change_5day) * (current volatility / 10-day average volatility - 1)

**Impact Score: 9.1/10**

**Justification:**
- Measures the sustainability and potential longevity of the current trend
- The mean reversion factor identifies low mean reversion (characteristic of strong trends)
- The gamma reinforcement factor captures options market dynamics that can reinforce trends
- The volatility trend alignment component identifies healthy volatility conditions for trend continuation
- Particularly valuable for assessing how long a trend might continue
- Excellent for optimizing position sizing and risk allocation in trend-following strategies

**Application:**
- TSI > 1.2: Highly sustainable trend likely to continue
- TSI > 1.5: Extremely sustainable trend environment suitable for larger position sizing
- TSI declining while price still trending: Warning of decreasing sustainability
- TSI < 0.8: Trend becoming less sustainable, consider reducing exposure

**Cross-Ticker Enhancement:**
Comparing TSI across multiple timeframes provides insight into the trend's time horizon. When both short-term (1-3 day) and medium-term (5-10 day) TSI readings are strong, the trend has multi-timeframe sustainability.

### 5. Trend Exhaustion Warning System (TEWS)

**Formula:**
```
TEWS = (momentum_divergence_factor * 0.4) + (options_positioning_shift * 0.3) + (volume_climax_factor * 0.3)
```
Where:
- `momentum_divergence_factor` = correlation between price changes and volmbs_15m over past 5 days * -1
- `options_positioning_shift` = rate of change in put_call_ratio over past 3 days * sign(price_change_5day)
- `volume_climax_factor` = (current volm_15m / 10-day average volm_15m - 1) * sign(price_change_5day)

**Impact Score: 8.9/10**

**Justification:**
- Designed specifically to identify potential exhaustion of trending regimes
- The momentum divergence factor captures when flow is no longer confirming price action
- The options positioning shift component identifies when options sentiment is changing
- The volume climax factor detects potential exhaustion spikes in volume
- Particularly valuable for identifying potential trend reversals
- Excellent for optimizing exits from trend-following positions

**Application:**
- TEWS > 1.0: Early warning of potential trend exhaustion
- TEWS > 1.5: Significant trend exhaustion signal, consider reducing trend exposure
- TEWS > 2.0: Strong exhaustion signal, potential for trend reversal
- TEWS accelerating while price making new trend extremes: Classic divergence pattern

**Cross-Ticker Enhancement:**
Comparing TEWS between the trending asset and sector rotation can provide early warning of trend exhaustion. For example, in an uptrend, if technology stocks (XLK) show high TEWS readings while defensive sectors show low TEWS, it may indicate an upcoming trend change.

## Synergistic Implementation

When implemented together, these five metrics create a comprehensive framework for navigating trending market regimes:

1. **DMSI** provides the core trend strength and momentum assessment
2. **OSTC** reveals how options positioning is supporting the trend
3. **ITPI** confirms institutional participation in the trend
4. **TSI** assesses the sustainability and potential longevity of the trend
5. **TEWS** provides early warning of potential trend exhaustion

The most powerful signals occur when multiple metrics align:
- All three core metrics strong positive: Highest conviction trending environment
- Core metrics positive with high TSI: Sustainable trend suitable for larger positions
- Core metrics positive but TEWS warning: Consider taking partial profits or tightening stops

This framework provides both confirmation of the trending regime and early warning of potential exhaustion, allowing for optimal positioning throughout the trend's lifecycle.
