# Enhanced Heatmap Combinations Analysis

## Overview

This document provides a comprehensive analysis of the enhanced heatmap combinations designed to improve the Elite Options Trading System. These heatmaps leverage ConvexValue's Greek exposure data to create more potent and actionable visualizations of market structure for day trading SPY/SPX options.

## Base ConvexValue Greek Exposure Data

ConvexValue provides several Greek exposure metrics that form the foundation for our enhanced heatmaps:

### Primary Greek Exposures
- **dxoi**: Delta multiplied by Open Interest
- **gxoi**: Gamma multiplied by Open Interest
- **vxoi**: Vega multiplied by Open Interest
- **txoi**: Theta multiplied by Open Interest

### Second-Order Greek Exposures
- **vannaxoi**: Vanna multiplied by Open Interest
- **vommaxoi**: Vomma multiplied by Open Interest
- **charmxoi**: Charm multiplied by Open Interest

### Volume-Based Greek Exposures
- **gxvolm**: Gamma multiplied by Volume
- **vxvolm**: Vega multiplied by Volume
- **txvolm**: Theta multiplied by Volume
- **dxvolm**: Delta multiplied by Volume

## Limitations of Base Heatmaps

While traditional heatmaps using these metrics provide valuable information, they have several limitations:

1. **Single-Dimensional Analysis**: Each Greek is typically analyzed in isolation
2. **Static Visualization**: No integration of real-time flow data
3. **Limited Context**: No consideration of price proximity or market conditions
4. **Binary Interpretation**: Simple color coding without nuanced strength indicators
5. **No Cross-Greek Integration**: Interactions between Greeks are not visualized

## Enhanced Heatmap Combinations Suite

To address these limitations, we've developed a comprehensive suite of enhanced heatmap combinations:

### 1. Gamma-Delta Hedging Pressure Heatmap (GDHP)

- **Formula**: `GDHP = (gxoi * price_proximity_factor) * sign(dxoi) * (1 + abs(dxoi)/max_dxoi)`
- **Purpose**: Identifies strikes where gamma and delta forces align to create maximum hedging pressure
- **Implementation Details**:
  ```python
  def calculate_gdhp(self, options_data, current_price):
      """Calculate Gamma-Delta Hedging Pressure Heatmap."""
      result = {}
      max_dxoi = max([abs(option['dxoi']) for option in options_data])
      
      for option in options_data:
          strike = option['strike']
          
          # Calculate price proximity factor (higher for strikes closer to current price)
          strike_distance = abs(strike - current_price)
          price_proximity_factor = np.exp(-0.5 * (strike_distance / (current_price * 0.01))**2)
          
          # Calculate GDHP
          gdhp = (option['gxoi'] * price_proximity_factor) * np.sign(option['dxoi']) * (1 + abs(option['dxoi'])/max_dxoi)
          
          result[strike] = gdhp
      
      return result
  ```
- **Visual Implementation**:
  - X-axis: Strike prices
  - Y-axis: None (single-row heatmap)
  - Color: Intense green for strong positive values, intense red for strong negative values
  - Add markers for current price and significant threshold levels
- **Interpretation**:
  - Strong positive values (green): Upward hedging pressure, potential support
  - Strong negative values (red): Downward hedging pressure, potential resistance
  - Intensity indicates strength of hedging pressure
  - Clusters of similar colors indicate zones rather than precise levels

### 2. Volatility Surface Tension Heatmap (VSTH)

- **Formula**: `VSTH = (vannaxoi * vommaxoi) / (vxoi + small_constant) * sign(vxoi)`
- **Purpose**: Reveals areas of the volatility surface under maximum tension
- **Implementation Details**:
  ```python
  def calculate_vsth(self, options_data):
      """Calculate Volatility Surface Tension Heatmap."""
      result = {}
      small_constant = 0.0001  # To avoid division by zero
      
      for option in options_data:
          strike = option['strike']
          expiration = option['expiration']
          
          # Calculate VSTH
          vsth = (option['vannaxoi'] * option['vommaxoi']) / (abs(option['vxoi']) + small_constant) * np.sign(option['vxoi'])
          
          if (strike, expiration) not in result:
              result[(strike, expiration)] = vsth
      
      return result
  ```
- **Visual Implementation**:
  - X-axis: Strike prices
  - Y-axis: Expiration dates (creating a full surface)
  - Color: Heat gradient from blue (low tension) to yellow to red (high tension)
  - Add contour lines connecting areas of equal tension
- **Interpretation**:
  - High positive values (red): Areas where volatility changes would have maximum bullish impact
  - High negative values (blue): Areas where volatility changes would have maximum bearish impact
  - Intensity indicates sensitivity to volatility changes
  - Contour lines help identify volatility skew patterns

### 3. Charm-Theta Decay Acceleration Heatmap (CTDAH)

- **Formula**: `CTDAH = (charmxoi * sign(txoi)) * (1 + abs(txoi)/max_txoi) * time_to_expiration_factor`
- **Purpose**: Identifies options where time decay effects are accelerating delta exposure
- **Implementation Details**:
  ```python
  def calculate_ctdah(self, options_data, current_date):
      """Calculate Charm-Theta Decay Acceleration Heatmap."""
      result = {}
      max_txoi = max([abs(option['txoi']) for option in options_data])
      
      for option in options_data:
          strike = option['strike']
          expiration = option['expiration']
          
          # Calculate days to expiration
          days_to_expiration = (expiration - current_date).days
          
          # Calculate time to expiration factor (higher for near-term options)
          time_to_expiration_factor = 1 / (1 + 0.1 * days_to_expiration)
          
          # Calculate CTDAH
          ctdah = (option['charmxoi'] * np.sign(option['txoi'])) * (1 + abs(option['txoi'])/max_txoi) * time_to_expiration_factor
          
          if (strike, expiration) not in result:
              result[(strike, expiration)] = ctdah
      
      return result
  ```
- **Visual Implementation**:
  - X-axis: Strike prices
  - Y-axis: Expiration dates
  - Color: Purple for strong positive values, yellow for strong negative values
  - Add time-based intensity that increases as expiration approaches
- **Interpretation**:
  - High positive values (purple): Accelerating positive delta change with time decay
  - High negative values (yellow): Accelerating negative delta change with time decay
  - Intensity increases as expiration approaches
  - Clusters indicate potential pinning or repelling strikes

### 4. Delta Imbalance Flow Heatmap (DIFH)

- **Formula**: `DIFH = (deltas_call_buy + deltas_put_sell) - (deltas_call_sell + deltas_put_buy)`
- **Purpose**: Shows the net directional pressure from options transactions
- **Implementation Details**:
  ```python
  def calculate_difh(self, options_data):
      """Calculate Delta Imbalance Flow Heatmap."""
      result = {}
      
      for option in options_data:
          strike = option['strike']
          
          # Calculate bullish delta flow
          bullish_delta_flow = option['deltas_call_buy'] + option['deltas_put_sell']
          
          # Calculate bearish delta flow
          bearish_delta_flow = option['deltas_call_sell'] + option['deltas_put_buy']
          
          # Calculate DIFH
          difh = bullish_delta_flow - bearish_delta_flow
          
          if strike not in result:
              result[strike] = difh
      
      return result
  ```
- **Visual Implementation**:
  - X-axis: Strike prices
  - Y-axis: Time (to show evolution throughout the day)
  - Color: Green for positive values, red for negative values
  - Add intensity based on absolute magnitude
- **Interpretation**:
  - Positive values (green): Net bullish positioning (long calls and short puts)
  - Negative values (red): Net bearish positioning (short calls and long puts)
  - Intensity reveals the strength of directional conviction
  - Time dimension shows how positioning evolves throughout the day

### 5. Composite Greek Imbalance Heatmap (CGIH)

- **Formula**: `CGIH = normalize(dxoi) + normalize(gxoi) * 2 + normalize(vxoi) * 0.5 + normalize(txoi) * 0.3`
- **Purpose**: Combines all major Greeks with appropriate weighting
- **Implementation Details**:
  ```python
  def calculate_cgih(self, options_data):
      """Calculate Composite Greek Imbalance Heatmap."""
      result = {}
      
      # Get max values for normalization
      max_dxoi = max([abs(option['dxoi']) for option in options_data])
      max_gxoi = max([abs(option['gxoi']) for option in options_data])
      max_vxoi = max([abs(option['vxoi']) for option in options_data])
      max_txoi = max([abs(option['txoi']) for option in options_data])
      
      for option in options_data:
          strike = option['strike']
          
          # Normalize Greeks
          norm_dxoi = option['dxoi'] / max_dxoi
          norm_gxoi = option['gxoi'] / max_gxoi
          norm_vxoi = option['vxoi'] / max_vxoi
          norm_txoi = option['txoi'] / max_txoi
          
          # Calculate CGIH with weights
          cgih = norm_dxoi + norm_gxoi * 2 + norm_vxoi * 0.5 + norm_txoi * 0.3
          
          if strike not in result:
              result[strike] = cgih
      
      return result
  ```
- **Visual Implementation**:
  - X-axis: Strike prices
  - Y-axis: None (single-row heatmap)
  - Color: Spectrum from deep blue (highly negative) to deep red (highly positive)
  - Add markers for current price and day's high/low
- **Interpretation**:
  - Positive values (red): Net bullish Greek exposure
  - Negative values (blue): Net bearish Greek exposure
  - Intensity indicates strength of combined Greek exposure
  - Transitions between colors indicate potential inflection points

### 6. Vanna-Charm Regime Shift Heatmap (VCRSH)

- **Formula**: `VCRSH = (vannaxoi * volatility_trend_factor) + (charmxoi * time_decay_factor)`
- **Purpose**: Identifies potential regime shifts due to volatility-time interactions
- **Implementation Details**:
  ```python
  def calculate_vcrsh(self, options_data, volatility_data, current_date):
      """Calculate Vanna-Charm Regime Shift Heatmap."""
      result = {}
      
      # Calculate volatility trend factor
      vol_trend = volatility_data['current_iv'] / volatility_data['historical_iv_20d']
      volatility_trend_factor = vol_trend if vol_trend > 1 else 1/vol_trend
      
      for option in options_data:
          strike = option['strike']
          expiration = option['expiration']
          
          # Calculate days to expiration
          days_to_expiration = (expiration - current_date).days
          
          # Calculate time decay factor (higher for near-term options)
          time_decay_factor = 1 / (1 + 0.1 * days_to_expiration)
          
          # Calculate VCRSH
          vcrsh = (option['vannaxoi'] * volatility_trend_factor) + (option['charmxoi'] * time_decay_factor)
          
          if (strike, expiration) not in result:
              result[(strike, expiration)] = vcrsh
      
      return result
  ```
- **Visual Implementation**:
  - X-axis: Strike prices
  - Y-axis: Expiration dates
  - Color: Cyan for positive regime shift potential, magenta for negative
  - Add overlay markers where values exceed significant thresholds
- **Interpretation**:
  - Positive values (cyan): Potential bullish regime shift
  - Negative values (magenta): Potential bearish regime shift
  - Intensity indicates likelihood of regime shift
  - Clusters across multiple expirations indicate stronger signals

### 7. Gamma Wall Intensity Heatmap (GWIH)

- **Formula**: `GWIH = abs(gxoi) * (1 + flow_confirmation_factor) * price_proximity_factor`
- **Purpose**: Enhanced gamma wall visualization that goes beyond simple gamma concentration
- **Implementation Details**:
  ```python
  def calculate_gwih(self, options_data, flow_data, current_price):
      """Calculate Gamma Wall Intensity Heatmap."""
      result = {}
      
      for option in options_data:
          strike = option['strike']
          
          # Calculate flow confirmation factor
          # Higher when recent flow confirms the gamma wall
          flow_at_strike = flow_data.get(strike, 0)
          flow_confirmation_factor = 0.5 * np.sign(option['gxoi'] * flow_at_strike) * min(1, abs(flow_at_strike) / 100)
          
          # Calculate price proximity factor
          strike_distance = abs(strike - current_price)
          price_proximity_factor = np.exp(-0.5 * (strike_distance / (current_price * 0.01))**2)
          
          # Calculate GWIH
          gwih = abs(option['gxoi']) * (1 + flow_confirmation_factor) * price_proximity_factor
          
          if strike not in result:
              result[strike] = gwih
      
      return result
  ```
- **Visual Implementation**:
  - X-axis: Strike prices
  - Y-axis: None (single-row heatmap)
  - Color: Intensity-based gradient from light to dark blue
  - Add vertical lines at major wall locations with thickness proportional to intensity
- **Interpretation**:
  - Darker blue indicates stronger gamma walls
  - Width indicates zone of influence rather than precise price
  - Flow-confirmed walls are more intense
  - Proximity to current price increases intensity

## Top 3 Consolidated Heatmap Combinations (Finalists)

After extensive analysis and testing, we've identified the three most powerful consolidated heatmap combinations that provide the highest impact for day trading SPY/SPX options:

### 1. Super Gamma-Delta Hedging Pressure Heatmap (SGDHP)

**Formula:**
```
SGDHP = (gxoi * price_proximity_factor) * sign(dxoi) * (1 + abs(dxoi)/max_dxoi) * (1 + recent_flow_confirmation)
```

**Detailed Implementation:**
```python
def calculate_sgdhp(self, options_data, flow_data, current_price):
    """Calculate Super Gamma-Delta Hedging Pressure Heatmap."""
    result = {}
    max_dxoi = max([abs(option['dxoi']) for option in options_data])
    
    for option in options_data:
        strike = option['strike']
        
        # Calculate price proximity factor (higher for strikes closer to current price)
        strike_distance = abs(strike - current_price)
        price_proximity_factor = np.exp(-0.5 * (strike_distance / (current_price * 0.01))**2)
        
        # Calculate recent flow confirmation factor
        recent_flow = flow_data.get(strike, {}).get('volmbs_5m', 0)
        flow_direction = np.sign(recent_flow)
        flow_magnitude = min(1, abs(recent_flow) / 100)  # Cap at 1 for normalization
        
        # Flow confirmation is positive when flow direction matches gamma-delta direction
        gamma_delta_direction = np.sign(option['gxoi'] * option['dxoi'])
        flow_confirmation = flow_magnitude if flow_direction == gamma_delta_direction else -flow_magnitude
        
        # Calculate SGDHP
        sgdhp = (
            (option['gxoi'] * price_proximity_factor) * 
            np.sign(option['dxoi']) * 
            (1 + abs(option['dxoi'])/max_dxoi) * 
            (1 + flow_confirmation)
        )
        
        result[strike] = sgdhp
    
    return result
```

**Visual Implementation:**
- X-axis: Strike prices
- Y-axis: None (single-row heatmap)
- Color: Intense green for strong positive values (upward pressure), intense red for strong negative values (downward pressure)
- Add vertical lines at levels exceeding 2 standard deviations
- Include current price marker and day's VWAP for reference

**Interpretation:**
- Strong positive values (green): Powerful upward hedging pressure, strong support
- Strong negative values (red): Powerful downward hedging pressure, strong resistance
- Intensity indicates strength of hedging pressure
- Flow confirmation increases confidence in the signal

**Market Impact:**
This heatmap identifies the most powerful price magnets and barriers in the market with exceptional accuracy. When price approaches these levels, the hedging activity will often create self-reinforcing momentum in the indicated direction. The addition of recent flow confirmation makes this significantly more potent than traditional gamma or delta heatmaps.

### 2. Integrated Volatility Surface Dynamics Heatmap (IVSDH)

**Formula:**
```
IVSDH = [(vannaxoi * vommaxoi) / (vxoi + small_constant)] * [1 + (charmxoi * time_decay_factor)]
```

**Detailed Implementation:**
```python
def calculate_ivsdh(self, options_data, current_date):
    """Calculate Integrated Volatility Surface Dynamics Heatmap."""
    result = {}
    small_constant = 0.0001  # To avoid division by zero
    
    for option in options_data:
        strike = option['strike']
        expiration = option['expiration']
        
        # Calculate days to expiration
        days_to_expiration = (expiration - current_date).days
        
        # Calculate time decay factor (higher for near-term options)
        time_decay_factor = 1 / (1 + 0.1 * days_to_expiration)
        
        # Calculate vanna-vomma component
        vanna_vomma_component = (option['vannaxoi'] * option['vommaxoi']) / (abs(option['vxoi']) + small_constant)
        
        # Calculate charm component
        charm_component = 1 + (option['charmxoi'] * time_decay_factor)
        
        # Calculate IVSDH
        ivsdh = vanna_vomma_component * charm_component
        
        if (strike, expiration) not in result:
            result[(strike, expiration)] = ivsdh
    
    return result
```

**Visual Implementation:**
- X-axis: Strike prices
- Y-axis: Expiration dates (creating a full surface)
- Color: Heat gradient from blue (stable) to yellow (moderate tension) to red (extreme tension)
- Add contour lines connecting areas of equal tension
- Include markers for current IV percentile and term structure slope

**Interpretation:**
- High positive values (red): Areas of extreme volatility surface tension with bullish bias
- High negative values (blue): Areas of extreme volatility surface tension with bearish bias
- Intensity indicates likelihood of volatility regime shift
- Time dimension shows how volatility dynamics evolve across expirations

**Market Impact:**
This heatmap identifies potential volatility regime shifts before they occur, showing exactly which strikes and expirations are most vulnerable to volatility changes. It's particularly valuable ahead of known catalysts like FOMC meetings or earnings. By combining vanna-vomma interactions with charm effects, it provides a comprehensive view of volatility surface dynamics.

### 3. Ultimate Greek Confluence Heatmap (UGCH)

**Formula:**
```
UGCH = normalize(dxoi) * 1.5 + normalize(gxoi) * 2 + normalize(vxoi) * 0.7 + normalize(txoi) * 0.5 + normalize(charmxoi) * 0.8 + normalize(vannaxoi) * 1.0
```

**Detailed Implementation:**
```python
def calculate_ugch(self, options_data):
    """Calculate Ultimate Greek Confluence Heatmap."""
    result = {}
    
    # Get max values for normalization
    max_dxoi = max([abs(option['dxoi']) for option in options_data])
    max_gxoi = max([abs(option['gxoi']) for option in options_data])
    max_vxoi = max([abs(option['vxoi']) for option in options_data])
    max_txoi = max([abs(option['txoi']) for option in options_data])
    max_charmxoi = max([abs(option['charmxoi']) for option in options_data])
    max_vannaxoi = max([abs(option['vannaxoi']) for option in options_data])
    
    for option in options_data:
        strike = option['strike']
        
        # Normalize Greeks
        norm_dxoi = option['dxoi'] / max_dxoi
        norm_gxoi = option['gxoi'] / max_gxoi
        norm_vxoi = option['vxoi'] / max_vxoi
        norm_txoi = option['txoi'] / max_txoi
        norm_charmxoi = option['charmxoi'] / max_charmxoi
        norm_vannaxoi = option['vannaxoi'] / max_vannaxoi
        
        # Calculate UGCH with weights
        ugch = (
            norm_dxoi * 1.5 + 
            norm_gxoi * 2.0 + 
            norm_vxoi * 0.7 + 
            norm_txoi * 0.5 + 
            norm_charmxoi * 0.8 + 
            norm_vannaxoi * 1.0
        )
        
        if strike not in result:
            result[strike] = ugch
    
    return result
```

**Visual Implementation:**
- X-axis: Strike prices
- Y-axis: None (single-row heatmap) or Expiration dates (for surface view)
- Color: Spectrum from deep blue (highly negative) through white (neutral) to deep red (highly positive)
- Add threshold markers at ±1.5 and ±2.5 standard deviations
- Include current price and recent price range overlay

**Interpretation:**
- Strong positive values (deep red): Powerful bullish structural level
- Strong negative values (deep blue): Powerful bearish structural level
- Intensity indicates strength of structural support/resistance
- Transitions between colors indicate potential inflection points

**Market Impact:**
This heatmap identifies the most significant structural levels in the market where multiple Greek forces align. These levels often act as major support/resistance and can cause significant acceleration or reversal when breached. By weighting each Greek appropriately based on its typical hedging impact, it creates a comprehensive view of market structure.

## Implementation Recommendations

### Data Requirements
- ConvexValue API access for Greek exposure data
- Historical data storage for normalization and comparison
- Real-time flow data for dynamic updates

### Calculation Frequency
- Calculate heatmaps every 5-15 minutes during market hours
- Recalculate on significant price moves (>0.5% in SPY/SPX)
- Full recalibration at market open and after major economic events

### Visualization Enhancements
- **Time-Series View**: Add the ability to view how these heatmaps evolved throughout the day or across multiple days
- **Threshold Alerts**: Create alerts when price approaches high-intensity areas on any heatmap
- **Composite Overlay**: Create a composite view that shows where all three heatmaps have high-intensity areas at the same strikes
- **Dynamic Scaling**: Implement adaptive scaling that adjusts based on the current market regime (high vs. low volatility)
- **Correlation Tracking**: Track how often price respects these levels and adjust weights accordingly

### Integration with Existing System
- Use heatmaps to identify key levels for the MSPI calculation
- Create dedicated visualization panels for the top 3 heatmaps
- Develop alert system for price approaching key levels

## Conclusion

The enhanced heatmap combinations represent a significant advancement in options market structure visualization, transforming ConvexValue's Greek exposure data into powerful, actionable visualizations for day trading SPY/SPX options. The top three consolidated heatmaps (SGDHP, IVSDH, and UGCH) provide a comprehensive view of hedging pressure, volatility dynamics, and structural levels that can significantly enhance trading decisions.

By implementing these heatmaps, traders will gain deeper insight into market structure and dealer positioning, leading to more precise entries, exits, and risk management. The combination of these heatmaps with the enhanced flow metrics and existing system components creates a cohesive, potent ecosystem for day trading short-term options.
