# Top 5 Metrics for Bullish Market Regime

## Introduction

A bullish market regime is characterized by sustained upward price movement, strong buying pressure, and positive sentiment. In this regime, we want metrics that can confirm the bullish bias, identify the strongest upward momentum, and provide early warning of potential regime shifts. The following five metric combinations provide maximum predictive power for navigating bullish markets.

## Core Metrics (Top 3)

### 1. Bullish Flow Momentum Index (BFMI)

**Formula:**
```
BFMI = (normalized_volmbs_15m * 0.4) + (normalized_valuebs_30m * 0.3) + (normalized_deltas_call_buy * 0.3)
```
Where:
- `normalized_volmbs_15m` = volmbs_15m / 20-day average absolute value of volmbs_15m
- `normalized_valuebs_30m` = valuebs_30m / 20-day average absolute value of valuebs_30m
- `normalized_deltas_call_buy` = deltas_call_buy / 20-day average of deltas_call_buy

**Impact Score: 9.8/10**

**Justification:**
- Combines three complementary bullish flow metrics that together provide a complete picture of buying pressure
- The 15-minute volume component captures immediate directional pressure
- The 30-minute value component adds capital commitment weight to filter out noise
- The call buying component ensures that options positioning aligns with bullish sentiment
- Normalization ensures consistent interpretation across different market conditions
- Particularly powerful in bullish regimes where flow momentum drives continuation

**Application:**
- BFMI > 1.5: Strong bullish momentum likely to continue
- BFMI acceleration (increasing at increasing rate): Potential for bullish breakout
- BFMI > 2.0 with increasing rate of change: Ideal conditions for bullish options strategies
- BFMI diverging from price (BFMI declining while price rising): Warning of potential exhaustion

**Cross-Ticker Enhancement:**
Comparing BFMI between SPY/SPX and sector ETFs like XLK (Technology) or XLF (Financials) provides insight into sector rotation within the bullish regime. When SPY BFMI and leading sector BFMI are both strong and aligned, the bullish regime has the strongest foundation.

### 2. Call Gamma Pressure Ratio (CGPR)

**Formula:**
```
CGPR = (call_gxoi * price_proximity_factor) / (put_gxoi * price_proximity_factor)
```
Where:
- `price_proximity_factor` = exp(-0.5 * ((strike - current_price) / (0.02 * current_price))²)
- This applies a Gaussian weighting to focus on strikes near the current price

**Impact Score: 9.5/10**

**Justification:**
- Measures the ratio of call gamma exposure to put gamma exposure near the current price
- In bullish regimes, call gamma typically dominates and creates upward "magnetism"
- The price proximity factor ensures we focus on the most relevant strikes
- Captures the options market structure that reinforces bullish price action
- Particularly effective in identifying "gamma squeeze" potential in strong bullish regimes

**Application:**
- CGPR > 1.5: Call gamma dominance supporting bullish price action
- CGPR > 2.0: Strong call gamma wall that can accelerate upward movement
- CGPR increasing while price consolidates: Potential for upward breakout
- CGPR reaching extreme levels (>3.0): Potential for short-term exhaustion followed by continuation

**Cross-Ticker Enhancement:**
Comparing CGPR between SPX and VIX options provides insight into volatility expectations within the bullish regime. A high SPX CGPR combined with a low VIX put/call ratio indicates strong conviction in the bullish regime continuing.

### 3. Institutional Bullish Positioning Index (IBPI)

**Formula:**
```
IBPI = (value_call_ratio * 0.3) + (normalized_value_call_bs * 0.4) + (vanna_exposure_score * 0.3)
```
Where:
- `value_call_ratio` = value of call buys / value of call sells
- `normalized_value_call_bs` = value_call_bs / 20-day average absolute value of value_call_bs
- `vanna_exposure_score` = normalized sum of positive vannaxoi across all strikes

**Impact Score: 9.3/10**

**Justification:**
- Captures institutional positioning through three complementary metrics
- The value call ratio component reveals conviction in call buying vs. selling
- The normalized value call buy-sell imbalance shows the capital commitment to bullish positioning
- The vanna exposure component captures the volatility-sensitive delta exposure that often drives institutional hedging
- Particularly effective at identifying sustainable bullish regimes backed by institutional money
- Excellent at distinguishing between retail-driven rallies and institutional-backed bullish trends

**Application:**
- IBPI > 1.5: Strong institutional bullish positioning
- IBPI consistently above 1.0 for multiple days: Sustainable bullish regime
- IBPI accelerating: Institutions increasing bullish exposure, likely to drive prices higher
- IBPI diverging from price action: Potential warning of smart money repositioning

**Cross-Ticker Enhancement:**
Comparing IBPI between large caps (SPY) and small caps (IWM) provides insight into the breadth and conviction of the bullish regime. When both show strong IBPI readings, the bullish regime has broader market support and is more likely to continue.

## Complementary Metrics (Additional 2)

### 4. Bullish Regime Stability Index (BRSI)

**Formula:**
```
BRSI = (normalized_oi_ch * 0.3) + (volatility_trend_factor * 0.3) + (bid_ask_imbalance_factor * 0.4)
```
Where:
- `normalized_oi_ch` = 5-day sum of oi_ch / average 5-day sum of absolute oi_ch over past 60 days
- `volatility_trend_factor` = -1 * (current volatility / 20-day average volatility - 1)
- `bid_ask_imbalance_factor` = average(bid_size / (bid_size + ask_size)) over past 3 days

**Impact Score: 8.9/10**

**Justification:**
- Measures the stability and sustainability of the bullish regime
- The normalized open interest change component reveals whether new positions are being established
- The volatility trend factor turns positive when volatility is declining (typical in stable bullish regimes)
- The bid-ask imbalance factor measures buying pressure in the order book
- Particularly valuable for distinguishing between sustainable bullish regimes and short-covering rallies
- Excellent for identifying the "sweet spot" of bullish regimes where trend following strategies work best

**Application:**
- BRSI > 1.0: Stable bullish regime likely to continue
- BRSI > 1.5: Highly stable bullish environment ideal for trend-following strategies
- BRSI declining while price rising: Warning of decreasing stability in the bullish regime
- BRSI < 0.5: Bullish regime becoming unstable, consider reducing risk

**Cross-Ticker Enhancement:**
Comparing BRSI between equities and bonds (using TLT data) provides insight into cross-asset confirmation of the bullish regime. When equity BRSI is strong and bond BRSI is weak (indicating stable yields), the bullish regime typically has stronger macroeconomic support.

### 5. Early Reversal Warning System (ERWS)

**Formula:**
```
ERWS = (normalized_vommaxoi * 0.3) + (delta_gamma_alignment_factor * 0.4) + (short_term_flow_divergence * 0.3)
```
Where:
- `normalized_vommaxoi` = sum of vommaxoi / 20-day average of sum of absolute vommaxoi
- `delta_gamma_alignment_factor` = correlation between dxoi and gxoi across strikes
- `short_term_flow_divergence` = correlation between volmbs_5m and volmbs_15m over past 3 hours

**Impact Score: 8.7/10**

**Justification:**
- Designed specifically to provide early warning of potential regime shifts from bullish to another regime
- The normalized vomma exposure component captures volatility of volatility expectations
- The delta-gamma alignment factor reveals whether hedging pressures are becoming misaligned
- The short-term flow divergence component identifies when short-term flows contradict the established trend
- Particularly valuable for risk management in extended bullish regimes
- Excellent for optimizing exit timing near potential regime shifts

**Application:**
- ERWS < -1.0: Early warning of potential bullish regime exhaustion
- ERWS declining while price making new highs: Classic divergence warning
- ERWS < -1.5: Strong signal to reduce bullish exposure or implement hedges
- ERWS < -2.0: Significant probability of imminent regime shift

**Cross-Ticker Enhancement:**
Comparing ERWS between SPY and defensive sectors like XLU (Utilities) or XLP (Consumer Staples) provides insight into sector rotation that often precedes regime shifts. When SPY ERWS is negative while defensive sector ERWS is improving, the probability of a regime shift increases significantly.

## Synergistic Implementation

When implemented together, these five metrics create a comprehensive framework for navigating bullish market regimes:

1. **BFMI** provides the core directional confirmation and momentum assessment
2. **CGPR** reveals the options market structure supporting the bullish regime
3. **IBPI** confirms institutional backing of the bullish trend
4. **BRSI** assesses the stability and sustainability of the bullish regime
5. **ERWS** provides early warning of potential regime shifts

The most powerful signals occur when multiple metrics align:
- All three core metrics strong positive: Highest conviction bullish environment
- Core metrics positive with stable BRSI: Sustainable bullish regime
- Core metrics positive but ERWS warning: Consider taking profits or implementing partial hedges

This framework provides both confirmation of the bullish regime and early warning of potential changes, allowing for optimal positioning throughout the regime's lifecycle.
