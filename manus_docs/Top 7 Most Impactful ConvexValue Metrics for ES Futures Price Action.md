# Top 7 Most Impactful ConvexValue Metrics for ES Futures Price Action

## Introduction

After thorough analysis of the ConvexValue data parameters for ES futures trading, I've identified the seven most impactful metrics for price action. These selections are based on their direct influence on futures price movement, their ability to reveal institutional positioning, and their effectiveness as leading indicators for short-term price direction.

## Top 7 Metrics Ranked by Impact

### 1. **volmbs_15m** (Volume of Buys minus Sells - last 15 minutes)

**Impact Score: 9.5/10**

**Justification:**
- Provides the most actionable short-term directional bias by showing the net buying/selling pressure
- The 15-minute window offers the optimal balance between noise filtering and responsiveness
- Directly correlates with price momentum in futures markets where positioning is more transparent than options
- Captures institutional activity as large players typically execute over several minutes rather than seconds
- Serves as an excellent leading indicator for price reversals when diverging from price action

**Application:**
- Strong positive values indicate aggressive buying pressure likely to drive prices higher
- Strong negative values signal selling pressure that typically precedes downward price movement
- Divergences between this metric and price action often precede significant reversals
- Acceleration in this metric (rate of change increasing) frequently precedes breakout moves

### 2. **deltas_buy** (Day Sum of Buy Deltas Traded)

**Impact Score: 9.2/10**

**Justification:**
- Represents the cumulative directional exposure from buy-side activity
- In futures markets, delta exposure translates directly to price impact as dealers hedge positions
- Provides insight into institutional positioning as large players typically accumulate substantial delta exposure
- More stable than time-windowed metrics, showing the overall daily bias
- Particularly important for ES futures where delta hedging drives significant price movement

**Application:**
- Sustained increases throughout the day indicate building bullish positioning
- Plateaus or decreases after strong increases often signal exhaustion of buying pressure
- Comparing to historical averages reveals unusual institutional activity
- Divergences between deltas_buy and price action often precede significant moves

### 3. **valuebs_30m** (Value of Buys minus Sells - last 30 minutes)

**Impact Score: 8.8/10**

**Justification:**
- Measures the capital commitment behind trading activity, filtering out small retail noise
- The 30-minute window captures institutional positioning better than shorter timeframes
- Value-weighted flow is more significant than raw volume in determining price impact
- Particularly important for ES futures where large capital flows drive market direction
- Serves as an excellent confirmation signal for price breakouts or reversals

**Application:**
- High positive values indicate strong capital commitment to upward price movement
- High negative values signal significant selling pressure with substantial capital backing
- Comparing to average daily values helps identify unusual institutional activity
- Divergences between this metric and price often precede significant price reversals

### 4. **dxvolm** (Delta multiplied by Volume)

**Impact Score: 8.5/10**

**Justification:**
- Combines directional exposure (delta) with trading activity (volume)
- Provides a more nuanced view of market impact than either metric alone
- Filters out high-volume but low-impact trades (e.g., market-neutral strategies)
- Particularly relevant for ES futures where both volume and delta exposure matter
- Excellent for identifying "smart money" positioning that will impact price

**Application:**
- High positive values indicate strong directional conviction with substantial volume
- Spikes in this metric often precede significant price movements
- Comparing to moving averages helps identify unusual positioning
- Particularly useful for identifying accumulation or distribution phases

### 5. **bid_size / ask_size ratio** (Ratio of Latest Bid Size to Latest Ask Size)

**Impact Score: 8.3/10**

**Justification:**
- Provides real-time insight into order book imbalances
- Directly impacts short-term price action through order flow dynamics
- Reveals institutional positioning as large players often show their hand in the order book
- Particularly important for ES futures where order book dynamics drive price discovery
- Serves as an excellent short-term predictor of price direction

**Application:**
- Ratio > 1.5 indicates strong buying pressure likely to drive prices up
- Ratio < 0.67 signals selling pressure likely to push prices down
- Sudden changes in this ratio often precede price reversals
- Persistent imbalances typically lead to trending price action

### 6. **oi_ch** (Open Interest Change)

**Impact Score: 8.0/10**

**Justification:**
- Reveals whether new positions are being established or existing ones closed
- Critical for understanding if price movement is driven by new money or profit-taking
- Particularly important for ES futures where contract rollover and position management drive significant price action
- Provides insight into market sentiment and conviction
- Excellent for identifying sustainable trends versus short-term fluctuations

**Application:**
- Rising prices with increasing open interest confirms bullish trend strength
- Falling prices with increasing open interest confirms bearish trend strength
- Rising prices with decreasing open interest suggests a weakening uptrend
- Falling prices with decreasing open interest indicates a weakening downtrend

### 7. **gxoi** (Gamma multiplied by Open Interest)

**Impact Score: 7.8/10**

**Justification:**
- While ES is primarily futures-driven, options gamma exposure still impacts price action
- Reveals potential price magnets and inflection points due to dealer hedging
- Particularly important near major option strikes and expiration dates
- Provides insight into potential volatility regimes and price stability zones
- Helps identify price levels where acceleration or deceleration may occur

**Application:**
- High positive values indicate price stability around that level (dampening effect)
- High negative values suggest potential price instability and acceleration away from that level
- Clusters of high gamma exposure often create price magnets during expiration periods
- Changes in the gamma profile often precede shifts in price behavior and volatility

## Conclusion

These seven metrics provide a comprehensive view of ES futures price action drivers, capturing institutional positioning, order flow dynamics, momentum, and options influence. When analyzed together, they offer powerful insights into potential price movements and market structure.
