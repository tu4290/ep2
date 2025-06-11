# Top 5 Metrics for Bearish Market Regime

## Introduction

A bearish market regime is characterized by sustained downward price movement, strong selling pressure, and negative sentiment. In this regime, we want metrics that can confirm the bearish bias, identify the strongest downward momentum, and provide early warning of potential regime shifts. The following five metric combinations provide maximum predictive power for navigating bearish markets.

## Core Metrics (Top 3)

### 1. Bearish Flow Momentum Index (BFMI)

**Formula:**
```
BFMI = (normalized_volmbs_15m * -0.4) + (normalized_valuebs_30m * -0.3) + (normalized_deltas_put_buy * 0.3)
```
Where:
- `normalized_volmbs_15m` = volmbs_15m / 20-day average absolute value of volmbs_15m
- `normalized_valuebs_30m` = valuebs_30m / 20-day average absolute value of valuebs_30m
- `normalized_deltas_put_buy` = deltas_put_buy / 20-day average of deltas_put_buy

**Impact Score: 9.7/10**

**Justification:**
- Combines three complementary bearish flow metrics that together provide a complete picture of selling pressure
- The negative weighting on volume and value components ensures that selling pressure produces positive BFMI values
- The put buying component ensures that options positioning aligns with bearish sentiment
- Normalization ensures consistent interpretation across different market conditions
- Particularly powerful in bearish regimes where flow momentum drives continuation

**Application:**
- BFMI > 1.5: Strong bearish momentum likely to continue
- BFMI acceleration (increasing at increasing rate): Potential for bearish breakdown
- BFMI > 2.0 with increasing rate of change: Ideal conditions for bearish options strategies
- BFMI diverging from price (BFMI declining while price falling): Warning of potential exhaustion

**Cross-Ticker Enhancement:**
Comparing BFMI between SPY/SPX and high-beta sectors like XLF (Financials) or XLY (Consumer Discretionary) provides insight into sector weakness within the bearish regime. When SPY BFMI and high-beta sector BFMI are both strong and aligned, the bearish regime has the strongest foundation.

### 2. Put Gamma Pressure Ratio (PGPR)

**Formula:**
```
PGPR = (put_gxoi * price_proximity_factor) / (call_gxoi * price_proximity_factor)
```
Where:
- `price_proximity_factor` = exp(-0.5 * ((strike - current_price) / (0.02 * current_price))²)
- This applies a Gaussian weighting to focus on strikes near the current price

**Impact Score: 9.6/10**

**Justification:**
- Measures the ratio of put gamma exposure to call gamma exposure near the current price
- In bearish regimes, put gamma typically dominates and creates downward "magnetism"
- The price proximity factor ensures we focus on the most relevant strikes
- Captures the options market structure that reinforces bearish price action
- Particularly effective in identifying "negative gamma" environments that accelerate downward moves

**Application:**
- PGPR > 1.5: Put gamma dominance supporting bearish price action
- PGPR > 2.0: Strong put gamma wall that can accelerate downward movement
- PGPR increasing while price consolidates: Potential for downward breakdown
- PGPR reaching extreme levels (>3.0): Potential for short-term exhaustion followed by continuation

**Cross-Ticker Enhancement:**
Comparing PGPR between SPX and VIX options provides insight into volatility expectations within the bearish regime. A high SPX PGPR combined with a high VIX call/put ratio indicates strong conviction in the bearish regime continuing with increasing volatility.

### 3. Institutional Bearish Positioning Index (IBPI)

**Formula:**
```
IBPI = (value_put_ratio * 0.3) + (normalized_value_put_bs * 0.4) + (negative_vanna_exposure_score * 0.3)
```
Where:
- `value_put_ratio` = value of put buys / value of put sells
- `normalized_value_put_bs` = value_put_bs / 20-day average absolute value of value_put_bs
- `negative_vanna_exposure_score` = normalized sum of negative vannaxoi across all strikes

**Impact Score: 9.4/10**

**Justification:**
- Captures institutional positioning through three complementary metrics
- The value put ratio component reveals conviction in put buying vs. selling
- The normalized value put buy-sell imbalance shows the capital commitment to bearish positioning
- The negative vanna exposure component captures the volatility-sensitive delta exposure that often drives institutional hedging
- Particularly effective at identifying sustainable bearish regimes backed by institutional money
- Excellent at distinguishing between retail panic and institutional-backed bearish trends

**Application:**
- IBPI > 1.5: Strong institutional bearish positioning
- IBPI consistently above 1.0 for multiple days: Sustainable bearish regime
- IBPI accelerating: Institutions increasing bearish exposure, likely to drive prices lower
- IBPI diverging from price action: Potential warning of smart money repositioning

**Cross-Ticker Enhancement:**
Comparing IBPI between equities (SPY) and credit markets (HYG or LQD) provides insight into cross-asset confirmation of the bearish regime. When both equity and credit IBPI readings are strong, the bearish regime has broader financial system support and is more likely to continue.

## Complementary Metrics (Additional 2)

### 4. Bearish Regime Intensity Index (BRII)

**Formula:**
```
BRII = (volatility_acceleration_factor * 0.35) + (normalized_vommaxoi * 0.35) + (bid_ask_skew_factor * 0.3)
```
Where:
- `volatility_acceleration_factor` = (current volatility / 5-day average volatility) - 1
- `normalized_vommaxoi` = sum of vommaxoi / 20-day average of sum of absolute vommaxoi
- `bid_ask_skew_factor` = average(ask_size / (bid_size + ask_size)) over past 3 days

**Impact Score: 9.0/10**

**Justification:**
- Measures the intensity and potential acceleration of the bearish regime
- The volatility acceleration factor captures increasing fear in the market
- The normalized vomma exposure component reveals volatility of volatility expectations
- The bid-ask skew factor measures selling pressure in the order book
- Particularly valuable for identifying periods of potential bearish acceleration
- Excellent for timing aggressive bearish strategies during regime intensification

**Application:**
- BRII > 1.0: Intensifying bearish regime
- BRII > 1.5: Rapidly intensifying bearish environment suitable for aggressive bearish strategies
- BRII > 2.0: Potential panic selling environment with accelerating downside
- BRII declining while price falling: Warning of decreasing intensity in the bearish regime

**Cross-Ticker Enhancement:**
Comparing BRII between equities and volatility products (VIX futures or UVXY) provides insight into volatility expectations within the bearish regime. When equity BRII is strong and volatility product BRII is also strong, the bearish regime is likely to feature increasing volatility and potentially sharper downside moves.

### 5. Bearish Exhaustion Detection System (BEDS)

**Formula:**
```
BEDS = (short_term_flow_reversal_factor * 0.4) + (put_call_skew_normalization * 0.3) + (negative_gamma_depletion_factor * 0.3)
```
Where:
- `short_term_flow_reversal_factor` = (volmbs_5m / 3-day average of absolute volmbs_5m) * -1
- `put_call_skew_normalization` = (current put_call_ratio / 10-day average put_call_ratio) * -1
- `negative_gamma_depletion_factor` = (sum of negative gxoi / 5-day average sum of negative gxoi) * -1

**Impact Score: 8.8/10**

**Justification:**
- Designed specifically to identify potential exhaustion of bearish regimes
- The short-term flow reversal factor captures changing dynamics in recent flow
- The put-call skew normalization component identifies when put activity is normalizing
- The negative gamma depletion factor reveals when negative gamma positioning is unwinding
- Particularly valuable for identifying potential bottoming processes
- Excellent for optimizing timing of bearish position reduction or counter-trend trades

**Application:**
- BEDS > 1.0: Early signs of bearish exhaustion
- BEDS > 1.5: Significant bearish exhaustion signal, consider reducing bearish exposure
- BEDS > 2.0: Strong exhaustion signal, potential for counter-trend bounce
- BEDS accelerating while price making new lows: Classic positive divergence

**Cross-Ticker Enhancement:**
Comparing BEDS between broad market indices (SPY/SPX) and defensive sectors like Utilities (XLU) or Consumer Staples (XLP) provides insight into sector rotation that often occurs near bearish exhaustion points. When SPY BEDS is positive while defensive sector BEDS is neutral or negative, the probability of a broader market exhaustion increases.

## Synergistic Implementation

When implemented together, these five metrics create a comprehensive framework for navigating bearish market regimes:

1. **BFMI** provides the core directional confirmation and momentum assessment
2. **PGPR** reveals the options market structure supporting the bearish regime
3. **IBPI** confirms institutional backing of the bearish trend
4. **BRII** assesses the intensity and acceleration potential of the bearish regime
5. **BEDS** provides early warning of potential bearish exhaustion

The most powerful signals occur when multiple metrics align:
- All three core metrics strong positive: Highest conviction bearish environment
- Core metrics positive with increasing BRII: Accelerating bearish regime
- Core metrics positive but BEDS warning: Consider taking profits or reducing bearish exposure

This framework provides both confirmation of the bearish regime and early warning of potential exhaustion, allowing for optimal positioning throughout the regime's lifecycle.
