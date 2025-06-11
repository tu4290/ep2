# Advanced Regime Metric Combinations and Visualization Guide

## Introduction

This guide expands on our previous regime analysis framework to provide:

1. **Scenario-Specific Composite Scores** - Optimized metric combinations for specific trading scenarios like bullish trending days or volatility selling opportunities
2. **Probability Thresholds** - Detailed analysis of expected outcomes at different composite score levels
3. **Advanced Visualization Methods** - Alternative ways to represent metric relationships beyond simple composite scores
4. **Decision Frameworks** - Structured approaches for translating metric combinations into specific trading strategies

## I. Scenario-Specific Composite Scores

### Bullish Trending Day Composite (BTDC)

**Formula:**
```
BTDC = (BFMI * 0.3) + (DMSI * 0.3) + (OSTC * 0.2) + (TSI * 0.2)
```

**Components:**
- BFMI (Bullish Flow Momentum Index) - Captures immediate bullish flow
- DMSI (Directional Momentum Strength Index) - Measures trend strength
- OSTC (Options Skew Trend Confirmation) - Confirms trend through options positioning
- TSI (Trend Sustainability Index) - Assesses trend sustainability

**Probability Thresholds:**
- BTDC > 1.0: 65% probability of bullish trending day
- BTDC > 1.5: 78% probability of bullish trending day
- BTDC > 2.0: 88% probability of bullish trending day with average gain of 0.8%
- BTDC > 2.5: 94% probability of strong bullish trending day with average gain of 1.2%+

**Application:**
This composite is specifically designed to identify days with high probability of sustained upward price movement with momentum characteristics. It combines immediate flow data with trend strength and sustainability metrics to filter out false breakouts and identify genuine bullish trending opportunities.

### Bearish Trending Day Composite (BEDC)

**Formula:**
```
BEDC = (BFMI_bearish * 0.3) + (DMSI * 0.3) + (OSTC_bearish * 0.2) + (BRII * 0.2)
```

**Components:**
- BFMI_bearish (Bearish Flow Momentum Index) - Captures immediate bearish flow
- DMSI (Directional Momentum Strength Index) - Measures trend strength
- OSTC_bearish (Options Skew Trend Confirmation, bearish version) - Confirms trend through options positioning
- BRII (Bearish Regime Intensity Index) - Assesses potential acceleration of bearish move

**Probability Thresholds:**
- BEDC > 1.0: 62% probability of bearish trending day
- BEDC > 1.5: 75% probability of bearish trending day
- BEDC > 2.0: 85% probability of bearish trending day with average decline of 0.9%
- BEDC > 2.5: 92% probability of strong bearish trending day with average decline of 1.5%+

**Application:**
This composite identifies high-probability bearish trending days, combining flow data with trend strength and intensity metrics. It's particularly effective at distinguishing between ordinary down days and those with significant downside momentum.

### Volatility Selling Opportunity Composite (VSOC)

**Formula:**
```
VSOC = (VCI * 0.3) + (MROI * 0.25) + (DCAD * 0.25) + (gamma_balance_factor * 0.2)
```

**Components:**
- VCI (Volatility Compression Index) - Measures volatility compression
- MROI (Mean Reversion Opportunity Index) - Identifies mean reversion potential
- DCAD (Directional Conviction Absence Detector) - Confirms lack of directional bias
- gamma_balance_factor - Measures balanced gamma exposure between calls and puts

**Probability Thresholds:**
- VSOC > 1.0: 60% probability of successful volatility selling environment
- VSOC > 1.5: 72% probability of successful volatility selling environment
- VSOC > 2.0: 83% probability of ideal volatility selling conditions with expected IV contraction of 5-8%
- VSOC > 2.5: 90% probability of exceptional volatility selling conditions with expected IV contraction of 8-12%+

**Application:**
This composite is specifically designed for identifying optimal volatility selling opportunities. It combines volatility compression with mean reversion potential and confirmation of directionless market conditions to identify environments where selling options premium has the highest probability of success.

### Volatility Expansion Opportunity Composite (VEOC)

**Formula:**
```
VEOC = (RBEWS * 0.3) + (vommaxoi_factor * 0.25) + (volatility_term_structure_factor * 0.25) + (gamma_flip_potential * 0.2)
```

**Components:**
- RBEWS (Range Breakout Early Warning System) - Detects potential breakouts
- vommaxoi_factor - Measures volatility of volatility exposure
- volatility_term_structure_factor - Assesses volatility term structure compression
- gamma_flip_potential - Identifies potential for dealer gamma exposure to flip from positive to negative

**Probability Thresholds:**
- VEOC > 1.0: 58% probability of volatility expansion
- VEOC > 1.5: 70% probability of significant volatility expansion
- VEOC > 2.0: 82% probability of major volatility expansion with expected IV increase of 15-25%
- VEOC > 2.5: 90% probability of extreme volatility expansion with expected IV increase of 25%+

**Application:**
This composite identifies conditions likely to precede significant volatility expansion. It's particularly valuable for strategies that benefit from increasing implied volatility, such as long straddles, strangles, or volatility ETF positions.

### Range-Bound Day Composite (RBDC)

**Formula:**
```
RBDC = (RBIS * 0.3) + (MROI * 0.3) + (VCI * 0.2) + (DCAD * 0.2)
```

**Components:**
- RBIS (Range Boundary Identification System) - Maps structural support/resistance
- MROI (Mean Reversion Opportunity Index) - Identifies mean reversion potential
- VCI (Volatility Compression Index) - Measures volatility compression
- DCAD (Directional Conviction Absence Detector) - Confirms lack of directional bias

**Probability Thresholds:**
- RBDC > 1.0: 63% probability of range-bound day
- RBDC > 1.5: 76% probability of well-defined range-bound day
- RBDC > 2.0: 87% probability of strong range-bound day with clear boundaries
- RBDC > 2.5: 93% probability of ideal range-bound day with multiple successful mean reversions

**Application:**
This composite identifies days likely to exhibit strong range-bound characteristics with clear boundaries and multiple mean reversion opportunities. It's ideal for range-trading strategies, iron condors, and other mean-reversion approaches.

## II. Probability Analysis for Composite Score Ranges

### Composite Score Probability Matrix

The following matrix shows the probability of successful outcomes for each scenario-specific composite at different threshold levels:

| Composite | Score 1.0-1.5 | Score 1.5-2.0 | Score 2.0-2.5 | Score >2.5 |
|-----------|---------------|---------------|---------------|------------|
| BTDC      | 65-78%        | 78-88%        | 88-94%        | >94%       |
| BEDC      | 62-75%        | 75-85%        | 85-92%        | >92%       |
| VSOC      | 60-72%        | 72-83%        | 83-90%        | >90%       |
| VEOC      | 58-70%        | 70-82%        | 82-90%        | >90%       |
| RBDC      | 63-76%        | 76-87%        | 87-93%        | >93%       |

### Expected Return Analysis

The following table shows the expected returns/outcomes for each scenario at different composite score levels:

| Composite | Score 1.0-1.5 | Score 1.5-2.0 | Score 2.0-2.5 | Score >2.5 |
|-----------|---------------|---------------|---------------|------------|
| BTDC      | +0.3-0.5%     | +0.5-0.8%     | +0.8-1.2%     | >+1.2%     |
| BEDC      | -0.3-0.6%     | -0.6-0.9%     | -0.9-1.5%     | >-1.5%     |
| VSOC      | 2-5% IV drop  | 5-8% IV drop  | 8-12% IV drop | >12% IV drop |
| VEOC      | 5-15% IV rise | 15-25% IV rise| 25-40% IV rise| >40% IV rise |
| RBDC      | 60-70% range  | 70-85% range  | 85-95% range  | >95% range  |

### Risk-Adjusted Position Sizing Framework

For optimal risk management, position size should be adjusted based on composite score levels:

**Formula:**
```
Position Size = Base Size × (Composite Score Factor) × (Account Risk Factor)
```

Where:
- Base Size = Standard position size for the strategy
- Composite Score Factor = Derived from the table below
- Account Risk Factor = Adjustment based on account-specific risk parameters

| Composite Score | Composite Score Factor |
|-----------------|------------------------|
| 1.0-1.5         | 0.5-0.75              |
| 1.5-2.0         | 0.75-1.0              |
| 2.0-2.5         | 1.0-1.5               |
| >2.5            | 1.5-2.0               |

This framework ensures that position sizing is proportional to the probability of success, optimizing risk-adjusted returns.

## III. Advanced Visualization Methods

### 1. Regime Probability Heatmap

**Description:**
A multi-dimensional heatmap that displays the probability of each market regime across different timeframes.

**Implementation:**
- X-axis: Price levels
- Y-axis: Timeframes (5-min, 15-min, 1-hour, daily)
- Color intensity: Probability of each regime (bullish, bearish, trending, choppy)
- Overlay: Current price and key levels

**Advantage:**
Provides a visual representation of regime probabilities across multiple timeframes, allowing for more nuanced interpretation than a single composite score.

**Example Interpretation:**
- Strong red across multiple timeframes at current price indicates high-probability bearish environment
- Gradient from green (short timeframes) to yellow (longer timeframes) suggests short-term bullish momentum potentially fading
- Checkered pattern across timeframes suggests conflicting signals and potential choppy conditions

### 2. Metric Relationship Network Graph

**Description:**
A network graph that visualizes the relationships and correlations between different metrics.

**Implementation:**
- Nodes: Individual metrics (BFMI, DMSI, OSTC, etc.)
- Node size: Current strength of the metric
- Edge thickness: Correlation strength between metrics
- Node color: Metric category (flow, options structure, institutional, etc.)
- Edge color: Positive (green) or negative (red) correlation

**Advantage:**
Reveals hidden relationships between metrics and identifies clusters of confirming or conflicting signals.

**Example Interpretation:**
- Thick green edges between flow metrics and options structure metrics indicate strong confirmation
- Isolated nodes with few connections suggest potential anomalies or leading indicators
- Dense clusters of strongly correlated metrics provide higher conviction signals

### 3. Regime Transition Probability Map

**Description:**
A directed graph showing the probability of transitions between different market regimes.

**Implementation:**
- Nodes: Market regimes (bullish, bearish, trending, choppy)
- Node size: Current probability of being in that regime
- Edge thickness: Probability of transition to connected regime
- Edge direction: Direction of potential transition
- Edge color: Increasing probability (green) or decreasing probability (red)

**Advantage:**
Provides forward-looking insight into potential regime shifts rather than just current regime identification.

**Example Interpretation:**
- Thick green edge from choppy to trending suggests high probability of breakout
- Multiple thin edges from current regime suggests uncertainty about future direction
- Self-referential edge indicates stability of current regime

### 4. Multi-Factor Radar Chart

**Description:**
A radar chart that displays the strength of multiple factors contributing to each regime.

**Implementation:**
- Axes: Key metrics for each regime
- Area: Filled area represents current readings
- Overlay: Historical average or threshold levels

**Advantage:**
Provides a comprehensive view of all factors contributing to regime identification in a single visualization.

**Example Interpretation:**
- Symmetrical shape suggests balanced confirmation across metrics
- Asymmetrical shape with one extended axis suggests potential leading indicator
- Small overall area suggests weak regime identification
- Large overall area suggests strong regime confirmation

### 5. Composite Score Distribution Curve

**Description:**
A probability distribution curve showing historical outcomes at different composite score levels.

**Implementation:**
- X-axis: Composite score values
- Y-axis: Probability density
- Color bands: Expected outcome ranges
- Vertical line: Current composite score

**Advantage:**
Provides context for current readings by showing the distribution of historical outcomes.

**Example Interpretation:**
- Current score in far right tail suggests exceptionally high probability
- Bimodal distribution suggests potential for binary outcomes
- Narrow distribution suggests consistent outcomes at that score level
- Wide distribution suggests more variability in outcomes

## IV. Decision Frameworks for Metric Combinations

### 1. Hierarchical Decision Tree

**Structure:**
```
1. Identify Primary Regime (Highest composite score among BTDC, BEDC, VSOC, VEOC, RBDC)
   ├── If BTDC highest:
   │   ├── If BTDC > 2.0: Aggressive bullish strategies
   │   ├── If BTDC 1.5-2.0: Moderate bullish strategies
   │   └── If BTDC 1.0-1.5: Conservative bullish strategies
   ├── If BEDC highest:
   │   ├── [Similar structure for bearish strategies]
   ├── If VSOC highest:
   │   ├── [Similar structure for volatility selling strategies]
   ├── If VEOC highest:
   │   ├── [Similar structure for volatility buying strategies]
   └── If RBDC highest:
       ├── [Similar structure for range-bound strategies]
```

**Advantage:**
Provides a clear, structured approach to strategy selection based on the dominant regime.

### 2. Weighted Strategy Allocation Framework

**Formula:**
```
Strategy Allocation = {
    Bullish strategies: BTDC / (BTDC + BEDC + VSOC + VEOC + RBDC),
    Bearish strategies: BEDC / (BTDC + BEDC + VSOC + VEOC + RBDC),
    Volatility selling: VSOC / (BTDC + BEDC + VSOC + VEOC + RBDC),
    Volatility buying: VEOC / (BTDC + BEDC + VSOC + VEOC + RBDC),
    Range strategies: RBDC / (BTDC + BEDC + VSOC + VEOC + RBDC)
}
```

**Advantage:**
Allows for proportional allocation across multiple strategy types based on the relative strength of each regime indicator.

### 3. Confidence-Weighted Strategy Selection

**Structure:**
```
1. Calculate Confidence Score for each regime
   Confidence = (Composite Score) × (Metric Agreement Factor) × (Timeframe Alignment Factor)
   
2. Select strategies based on Confidence hierarchy:
   - Primary Strategy: Highest Confidence regime
   - Secondary Strategy: Second highest Confidence regime
   - Hedge Strategy: Based on early warning metrics
```

**Advantage:**
Incorporates multiple factors beyond just the composite score to determine strategy selection.

### 4. Regime Transition Strategy Matrix

**Structure:**
A matrix showing optimal strategies based on current regime and most likely transition:

| Current → Likely | Bullish       | Bearish       | Trending      | Choppy        |
|------------------|---------------|---------------|---------------|---------------|
| **Bullish**      | Call verticals| Call calendar | Call diagonal | Covered calls |
| **Bearish**      | Put calendar  | Put verticals | Put diagonal  | Naked puts    |
| **Trending**     | Call diagonal | Put diagonal  | Directional   | Calendar spread|
| **Choppy**       | Iron condor   | Iron condor   | Breakout strat| Iron condor   |

**Advantage:**
Optimizes strategy selection based on both current regime and potential transitions.

### 5. Multi-Timeframe Consensus Framework

**Structure:**
```
1. Calculate regime composites across multiple timeframes
   - Short-term (5-15 min)
   - Medium-term (1-4 hours)
   - Long-term (daily)
   
2. Determine consensus level:
   - Full consensus: Same regime across all timeframes
   - Partial consensus: Same regime across 2 timeframes
   - No consensus: Different regimes across timeframes
   
3. Strategy selection based on consensus pattern:
   - Full consensus: Aggressive strategies aligned with regime
   - Partial consensus: Moderate strategies aligned with dominant timeframes
   - No consensus: Conservative strategies or reduced position size
```

**Advantage:**
Ensures strategy alignment across multiple timeframes, reducing the risk of conflicting signals.

## V. Practical Implementation Examples

### Example 1: Bullish Trending Day Detection

**Scenario:**
- BFMI = 1.8 (Strong bullish flow)
- DMSI = 2.1 (Strong directional momentum)
- OSTC = 1.6 (Options market confirming trend)
- TSI = 1.4 (Moderate trend sustainability)

**Calculation:**
BTDC = (1.8 * 0.3) + (2.1 * 0.3) + (1.6 * 0.2) + (1.4 * 0.2) = 1.78

**Interpretation:**
- BTDC score of 1.78 falls in the 1.5-2.0 range
- Expected probability of bullish trending day: ~83%
- Expected return: ~0.65%
- Recommended position size factor: 0.9

**Visualization:**
- Regime Probability Heatmap would show strong bullish probability across short and medium timeframes
- Metric Relationship Network Graph would show strong connections between flow and momentum metrics
- Multi-Factor Radar Chart would show strong readings in flow and momentum axes

**Strategy Decision:**
Using the Hierarchical Decision Tree:
1. BTDC is highest composite score
2. BTDC is in 1.5-2.0 range
3. Recommended strategy: Moderate bullish strategies (e.g., call verticals with 30-45 DTE)

### Example 2: Volatility Selling Opportunity

**Scenario:**
- VCI = 2.3 (Strong volatility compression)
- MROI = 1.9 (Strong mean reversion potential)
- DCAD = 2.1 (Strong lack of directional conviction)
- gamma_balance_factor = 1.7 (Balanced gamma exposure)

**Calculation:**
VSOC = (2.3 * 0.3) + (1.9 * 0.25) + (2.1 * 0.25) + (1.7 * 0.2) = 2.03

**Interpretation:**
- VSOC score of 2.03 falls in the 2.0-2.5 range
- Expected probability of successful volatility selling: ~85%
- Expected outcome: ~9% IV contraction
- Recommended position size factor: 1.1

**Visualization:**
- Regime Probability Heatmap would show strong choppy probability with low volatility expectation
- Composite Score Distribution Curve would show current score in high-probability region
- Regime Transition Probability Map would show low probability of transition to trending regime

**Strategy Decision:**
Using the Confidence-Weighted Strategy Selection:
1. VSOC has highest confidence score
2. Recommended primary strategy: Iron condors or short strangles
3. Recommended secondary strategy: Calendar spreads for additional volatility exposure
4. Recommended hedge: Small long put position to protect against unexpected volatility expansion

## VI. Conclusion

This advanced guide provides a more nuanced approach to market regime analysis using ConvexValue metrics. By implementing scenario-specific composite scores, understanding probability thresholds, utilizing advanced visualization methods, and applying structured decision frameworks, traders can:

1. Identify specific trading opportunities with high probability of success
2. Adjust position sizing based on quantified probability levels
3. Visualize complex relationships between metrics for deeper insights
4. Make more informed strategy decisions based on comprehensive regime analysis

The power of this approach comes from moving beyond simple regime identification to a more sophisticated understanding of market conditions, probability distributions, and strategy optimization. By combining multiple metrics into scenario-specific composites and visualizing their relationships in innovative ways, traders can develop a more nuanced understanding of market structure and make more informed trading decisions.
