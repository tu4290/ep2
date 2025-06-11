# Enhanced Greek Metrics Analysis and Implementation Guide for Python Integration

## 1. Introduction

This comprehensive guide provides enhanced formulas and implementation details for accurately representing the impact of options Greek metrics on underlying asset price action. The formulas are specifically designed for integration into Python scripts, with a focus on SPY/SPX options trading.

## 2. Core Impact Weighting System

### 2.1 Fundamental Impact Weights

The foundation of our enhanced Greek metrics is a sophisticated weighting system that accounts for the asymmetric impact of bought versus sold options:

| Position Type | Base Impact Weight | Rationale |
|--------------|-------------------|-----------|
| Buy Call | 1.00 | Baseline reference (strongest bullish impact) |
| Sell Put | 0.65 | Moderate bullish impact (less dealer hedging) |
| Buy Put | 1.00 | Baseline reference (strongest bearish impact) |
| Sell Call | 0.65 | Moderate bearish impact (less dealer hedging) |

### 2.2 Proximity Factor Calculation

The proximity factor adjusts impact based on how close an option is to being at-the-money:

```python
def calculate_proximity_factor(strike, current_price, delta=None):
    """
    Calculate the proximity factor for a given strike.
    
    Parameters:
    -----------
    strike : float
        The strike price of the option
    current_price : float
        The current price of the underlying asset
    delta : float, optional
        The delta of the option, if available
        
    Returns:
    --------
    float
        The proximity factor (0.0 to 1.0)
    """
    # Basic proximity based on price distance
    basic_proximity = 1 - min(1, abs(strike - current_price) / (current_price * 0.05))
    
    # If delta is available, use enhanced proximity calculation
    if delta is not None:
        return basic_proximity * (0.5 + 0.5 * min(1, abs(delta)))
    
    return basic_proximity
```

### 2.3 Enhanced Greek-Specific Impact Weights

Different Greeks require different weighting factors due to their unique hedging dynamics:

| Greek | Buy Weight | Sell Weight | Buy/Sell Ratio | Rationale |
|-------|------------|-------------|----------------|-----------|
| Delta | 1.00 | 0.65 | 1.54 | Standard directional hedging |
| Gamma | 1.20 | 0.60 | 2.00 | Highest differential due to convexity hedging |
| Vega | 1.15 | 0.70 | 1.64 | Volatility exposure hedging |
| Theta | 0.90 | 0.80 | 1.13 | Lowest differential (time decay affects both) |

## 3. Enhanced Greek Impact Formulas

### 3.1 Delta Impact Formula

Delta represents the directional exposure and is the primary driver of hedging activity:

```python
def calculate_delta_impact(options_data, current_price):
    """
    Calculate the delta impact on the underlying asset.
    
    Parameters:
    -----------
    options_data : DataFrame
        DataFrame containing options data with columns:
        [strike, deltas_call_buy, deltas_call_sell, deltas_put_buy, deltas_put_sell]
    current_price : float
        Current price of the underlying asset
        
    Returns:
    --------
    DataFrame
        DataFrame with original data plus delta_impact column
    """
    result = options_data.copy()
    
    # Calculate proximity factor for each strike
    result['proximity'] = result['strike'].apply(
        lambda x: calculate_proximity_factor(x, current_price)
    )
    
    # Calculate delta impact
    result['delta_impact'] = (
        (result['deltas_call_buy'] * 1.00 * result['proximity']) - 
        (result['deltas_call_sell'] * 0.65 * result['proximity']) + 
        (result['deltas_put_sell'] * 0.65 * result['proximity']) - 
        (result['deltas_put_buy'] * 1.00 * result['proximity'])
    )
    
    return result
```

### 3.2 Gamma Impact Formula

Gamma represents the rate of change of delta and is crucial for identifying potential acceleration zones:

```python
def calculate_gamma_impact(options_data, current_price):
    """
    Calculate the gamma impact on the underlying asset.
    
    Parameters:
    -----------
    options_data : DataFrame
        DataFrame containing options data with columns:
        [strike, gammas_call_buy, gammas_call_sell, gammas_put_buy, gammas_put_sell]
    current_price : float
        Current price of the underlying asset
        
    Returns:
    --------
    DataFrame
        DataFrame with original data plus gamma_impact column
    """
    result = options_data.copy()
    
    # Calculate proximity factor for each strike
    if 'proximity' not in result.columns:
        result['proximity'] = result['strike'].apply(
            lambda x: calculate_proximity_factor(x, current_price)
        )
    
    # Calculate gamma impact
    result['gamma_impact'] = (
        (result['gammas_call_buy'] * 1.20 * result['proximity']) - 
        (result['gammas_call_sell'] * 0.60 * result['proximity']) + 
        (result['gammas_put_buy'] * 1.20 * result['proximity']) - 
        (result['gammas_put_sell'] * 0.60 * result['proximity'])
    )
    
    return result
```

### 3.3 Vega Impact Formula

Vega represents volatility exposure and helps identify potential volatility regime shifts:

```python
def calculate_vega_impact(options_data, current_price):
    """
    Calculate the vega impact on implied volatility.
    
    Parameters:
    -----------
    options_data : DataFrame
        DataFrame containing options data with columns:
        [strike, vegas_call_buy, vegas_call_sell, vegas_put_buy, vegas_put_sell]
    current_price : float
        Current price of the underlying asset
        
    Returns:
    --------
    DataFrame
        DataFrame with original data plus vega_impact column
    """
    result = options_data.copy()
    
    # Calculate proximity factor for each strike
    if 'proximity' not in result.columns:
        result['proximity'] = result['strike'].apply(
            lambda x: calculate_proximity_factor(x, current_price)
        )
    
    # Calculate vega impact
    result['vega_impact'] = (
        (result['vegas_call_buy'] * 1.15 * result['proximity']) - 
        (result['vegas_call_sell'] * 0.70 * result['proximity']) + 
        (result['vegas_put_buy'] * 1.15 * result['proximity']) - 
        (result['vegas_put_sell'] * 0.70 * result['proximity'])
    )
    
    return result
```

### 3.4 Theta Impact Formula

Theta represents time decay exposure and helps identify potential time-based pressure:

```python
def calculate_theta_impact(options_data, current_price):
    """
    Calculate the theta impact on time decay dynamics.
    
    Parameters:
    -----------
    options_data : DataFrame
        DataFrame containing options data with columns:
        [strike, thetas_call_buy, thetas_call_sell, thetas_put_buy, thetas_put_sell]
    current_price : float
        Current price of the underlying asset
        
    Returns:
    --------
    DataFrame
        DataFrame with original data plus theta_impact column
    """
    result = options_data.copy()
    
    # Calculate proximity factor for each strike
    if 'proximity' not in result.columns:
        result['proximity'] = result['strike'].apply(
            lambda x: calculate_proximity_factor(x, current_price)
        )
    
    # Calculate theta impact
    result['theta_impact'] = (
        (result['thetas_call_buy'] * 0.90 * result['proximity']) - 
        (result['thetas_call_sell'] * 0.80 * result['proximity']) + 
        (result['thetas_put_buy'] * 0.90 * result['proximity']) - 
        (result['thetas_put_sell'] * 0.80 * result['proximity'])
    )
    
    return result
```

### 3.5 Volume and Value Impact Formulas

Volume and value metrics provide insights into positioning intensity:

```python
def calculate_volume_impact(options_data, current_price):
    """
    Calculate the volume impact on the underlying asset.
    
    Parameters:
    -----------
    options_data : DataFrame
        DataFrame containing options data with columns:
        [strike, volm_call_buy, volm_call_sell, volm_put_buy, volm_put_sell]
    current_price : float
        Current price of the underlying asset
        
    Returns:
    --------
    DataFrame
        DataFrame with original data plus volume_impact column
    """
    result = options_data.copy()
    
    # Calculate proximity factor for each strike
    if 'proximity' not in result.columns:
        result['proximity'] = result['strike'].apply(
            lambda x: calculate_proximity_factor(x, current_price)
        )
    
    # Calculate volume impact
    result['volume_impact'] = (
        (result['volm_call_buy'] * 1.00 * result['proximity']) - 
        (result['volm_call_sell'] * 0.65 * result['proximity']) + 
        (result['volm_put_sell'] * 0.65 * result['proximity']) - 
        (result['volm_put_buy'] * 1.00 * result['proximity'])
    )
    
    return result

def calculate_value_impact(options_data, current_price):
    """
    Calculate the value (premium) impact on the underlying asset.
    
    Parameters:
    -----------
    options_data : DataFrame
        DataFrame containing options data with columns:
        [strike, value_call_buy, value_call_sell, value_put_buy, value_put_sell]
    current_price : float
        Current price of the underlying asset
        
    Returns:
    --------
    DataFrame
        DataFrame with original data plus value_impact column
    """
    result = options_data.copy()
    
    # Calculate proximity factor for each strike
    if 'proximity' not in result.columns:
        result['proximity'] = result['strike'].apply(
            lambda x: calculate_proximity_factor(x, current_price)
        )
    
    # Calculate value impact
    result['value_impact'] = (
        (result['value_call_buy'] * 1.10 * result['proximity']) - 
        (result['value_call_sell'] * 0.70 * result['proximity']) + 
        (result['value_put_sell'] * 0.70 * result['proximity']) - 
        (result['value_put_buy'] * 1.10 * result['proximity'])
    )
    
    return result
```

## 4. Composite Impact Metrics

### 4.1 Comprehensive Impact Score

This formula combines all Greek impacts into a single score:

```python
def calculate_composite_impact(options_data, current_price, normalize=True):
    """
    Calculate a composite impact score combining all Greek metrics.
    
    Parameters:
    -----------
    options_data : DataFrame
        DataFrame containing all required options data
    current_price : float
        Current price of the underlying asset
    normalize : bool, optional
        Whether to normalize the component impacts before combining
        
    Returns:
    --------
    DataFrame
        DataFrame with original data plus composite_impact column
    """
    # Calculate individual impacts
    result = calculate_delta_impact(options_data, current_price)
    result = calculate_gamma_impact(result, current_price)
    result = calculate_vega_impact(result, current_price)
    result = calculate_theta_impact(result, current_price)
    result = calculate_value_impact(result, current_price)
    
    # Normalize if requested
    if normalize:
        for col in ['delta_impact', 'gamma_impact', 'vega_impact', 'theta_impact', 'value_impact']:
            max_abs = result[col].abs().max()
            if max_abs > 0:
                result[f'{col}_norm'] = result[col] / max_abs
            else:
                result[f'{col}_norm'] = 0
        
        # Calculate composite impact using normalized values
        result['composite_impact'] = (
            0.35 * result['delta_impact_norm'] + 
            0.25 * result['gamma_impact_norm'] + 
            0.20 * result['vega_impact_norm'] + 
            0.10 * result['theta_impact_norm'] + 
            0.10 * result['value_impact_norm']
        )
    else:
        # Scale the impacts to comparable magnitudes
        result['composite_impact'] = (
            0.35 * result['delta_impact'] + 
            0.25 * result['gamma_impact'] + 
            0.20 * result['vega_impact'] / 1000 + 
            0.10 * result['theta_impact'] / 1000 + 
            0.10 * result['value_impact'] / 10000
        )
    
    return result
```

### 4.2 Strike Magnetism Index (SMI)

This enhanced formula identifies strikes with strong "magnetic" properties:

```python
def calculate_strike_magnetism(options_data, current_price):
    """
    Calculate the Strike Magnetism Index (SMI) for each strike.
    
    Parameters:
    -----------
    options_data : DataFrame
        DataFrame containing options data with gamma and delta metrics
    current_price : float
        Current price of the underlying asset
        
    Returns:
    --------
    DataFrame
        DataFrame with original data plus smi column
    """
    result = options_data.copy()
    
    # Calculate proximity factor for each strike
    if 'proximity' not in result.columns:
        result['proximity'] = result['strike'].apply(
            lambda x: calculate_proximity_factor(x, current_price)
        )
    
    # Calculate net gamma exposure (gxoi)
    if 'gxoi' not in result.columns:
        result['gxoi'] = result['gammas_call_buy'] + result['gammas_put_buy'] - \
                         result['gammas_call_sell'] - result['gammas_put_sell']
    
    # Calculate net delta exposure (dxoi)
    if 'dxoi' not in result.columns:
        result['dxoi'] = result['deltas_call_buy'] + result['deltas_put_sell'] - \
                         result['deltas_call_sell'] - result['deltas_put_buy']
    
    # Calculate open interest change factor
    if 'oi' in result.columns and 'oi_ch' in result.columns:
        result['oi_change_factor'] = 1 + result['oi_ch'].abs() / result['oi'].replace(0, 1)
    else:
        result['oi_change_factor'] = 1.0
    
    # Calculate Strike Magnetism Index
    result['smi'] = (
        result['gxoi'] * np.sign(result['dxoi']) * 
        result['oi_change_factor'] * 
        result['proximity']
    )
    
    return result
```

### 4.3 Volatility Pressure Index (VPI)

This formula identifies potential volatility expansion or contraction zones:

```python
def calculate_volatility_pressure(options_data, current_price):
    """
    Calculate the Volatility Pressure Index (VPI) for each strike.
    
    Parameters:
    -----------
    options_data : DataFrame
        DataFrame containing options data with vega and gamma metrics
    current_price : float
        Current price of the underlying asset
        
    Returns:
    --------
    DataFrame
        DataFrame with original data plus vpi column
    """
    result = options_data.copy()
    
    # Calculate vega impact if not already done
    if 'vega_impact' not in result.columns:
        result = calculate_vega_impact(result, current_price)
    
    # Calculate gamma impact if not already done
    if 'gamma_impact' not in result.columns:
        result = calculate_gamma_impact(result, current_price)
    
    # Calculate Volatility Pressure Index
    result['vpi'] = (
        result['vega_impact'] * np.sign(result['gamma_impact']) * 
        result['proximity']
    )
    
    # Normalize VPI
    max_abs_vpi = result['vpi'].abs().max()
    if max_abs_vpi > 0:
        result['vpi_norm'] = result['vpi'] / max_abs_vpi
    else:
        result['vpi_norm'] = 0
    
    return result
```

## 5. Advanced Analysis Functions

### 5.1 Key Level Identification

This function identifies key price levels based on Greek impacts:

```python
def identify_key_levels(options_data, current_price, threshold=0.7):
    """
    Identify key price levels based on Greek impacts.
    
    Parameters:
    -----------
    options_data : DataFrame
        DataFrame containing options data with calculated impacts
    current_price : float
        Current price of the underlying asset
    threshold : float, optional
        Threshold for identifying key levels (0.0 to 1.0)
        
    Returns:
    --------
    dict
        Dictionary containing support and resistance levels
    """
    # Calculate composite impact if not already done
    if 'composite_impact' not in options_data.columns:
        data = calculate_composite_impact(options_data, current_price)
    else:
        data = options_data.copy()
    
    # Calculate SMI if not already done
    if 'smi' not in data.columns:
        data = calculate_strike_magnetism(data, current_price)
    
    # Normalize SMI
    max_abs_smi = data['smi'].abs().max()
    if max_abs_smi > 0:
        data['smi_norm'] = data['smi'] / max_abs_smi
    else:
        data['smi_norm'] = 0
    
    # Identify support levels (positive SMI, below current price)
    support_candidates = data[
        (data['smi_norm'] > threshold) & 
        (data['strike'] < current_price)
    ].sort_values('smi_norm', ascending=False)
    
    # Identify resistance levels (negative SMI, above current price)
    resistance_candidates = data[
        (data['smi_norm'] < -threshold) & 
        (data['strike'] > current_price)
    ].sort_values('smi_norm', ascending=True)
    
    # Group nearby levels (within 0.5% of each other)
    support_levels = []
    resistance_levels = []
    
    if not support_candidates.empty:
        current_group = [support_candidates.iloc[0]]
        for i in range(1, len(support_candidates)):
            if (abs(support_candidates.iloc[i]['strike'] - current_group[-1]['strike']) / 
                current_price < 0.005):
                current_group.append(support_candidates.iloc[i])
            else:
                # Calculate average strike and combined strength for the group
                avg_strike = sum(item['strike'] for item in current_group) / len(current_group)
                combined_strength = sum(item['smi_norm'] for item in current_group)
                support_levels.append({
                    'strike': avg_strike,
                    'strength': combined_strength,
                    'proximity': abs(current_price - avg_strike) / current_price
                })
                current_group = [support_candidates.iloc[i]]
        
        # Add the last group
        if current_group:
            avg_strike = sum(item['strike'] for item in current_group) / len(current_group)
            combined_strength = sum(item['smi_norm'] for item in current_group)
            support_levels.append({
                'strike': avg_strike,
                'strength': combined_strength,
                'proximity': abs(current_price - avg_strike) / current_price
            })
    
    # Similar process for resistance levels
    if not resistance_candidates.empty:
        current_group = [resistance_candidates.iloc[0]]
        for i in range(1, len(resistance_candidates)):
            if (abs(resistance_candidates.iloc[i]['strike'] - current_group[-1]['strike']) / 
                current_price < 0.005):
                current_group.append(resistance_candidates.iloc[i])
            else:
                avg_strike = sum(item['strike'] for item in current_group) / len(current_group)
                combined_strength = sum(item['smi_norm'] for item in current_group)
                resistance_levels.append({
                    'strike': avg_strike,
                    'strength': abs(combined_strength),  # Use absolute value for easier comparison
                    'proximity': abs(current_price - avg_strike) / current_price
                })
                current_group = [resistance_candidates.iloc[i]]
        
        # Add the last group
        if current_group:
            avg_strike = sum(item['strike'] for item in current_group) / len(current_group)
            combined_strength = sum(item['smi_norm'] for item in current_group)
            resistance_levels.append({
                'strike': avg_strike,
                'strength': abs(combined_strength),
                'proximity': abs(current_price - avg_strike) / current_price
            })
    
    return {
        'support': sorted(support_levels, key=lambda x: x['strength'], reverse=True),
        'resistance': sorted(resistance_levels, key=lambda x: x['strength'], reverse=True),
        'current_price': current_price
    }
```

### 5.2 Gamma Exposure Profile

This function creates a comprehensive gamma exposure profile:

```python
def calculate_gamma_exposure_profile(options_data, current_price, price_range=0.05):
    """
    Calculate a gamma exposure profile across a range of potential prices.
    
    Parameters:
    -----------
    options_data : DataFrame
        DataFrame containing options data with gamma metrics
    current_price : float
        Current price of the underlying asset
    price_range : float, optional
        Price range to analyze as a percentage of current price
        
    Returns:
    --------
    DataFrame
        DataFrame with price levels and corresponding gamma exposure
    """
    # Calculate gamma impact if not already done
    if 'gamma_impact' not in options_data.columns:
        data = calculate_gamma_impact(options_data, current_price)
    else:
        data = options_data.copy()
    
    # Define price range to analyze
    min_price = current_price * (1 - price_range)
    max_price = current_price * (1 + price_range)
    price_steps = 100
    price_levels = np.linspace(min_price, max_price, price_steps)
    
    # Initialize results
    results = []
    
    # Calculate gamma exposure at each price level
    for price in price_levels:
        # Recalculate proximity factors for this price
        data['temp_proximity'] = data['strike'].apply(
            lambda x: calculate_proximity_factor(x, price)
        )
        
        # Calculate gamma impact at this price
        gamma_exposure = sum(
            (data['gammas_call_buy'] * 1.20 * data['temp_proximity']) - 
            (data['gammas_call_sell'] * 0.60 * data['temp_proximity']) + 
            (data['gammas_put_buy'] * 1.20 * data['temp_proximity']) - 
            (data['gammas_put_sell'] * 0.60 * data['temp_proximity'])
        )
        
        results.append({
            'price': price,
            'gamma_exposure': gamma_exposure,
            'price_pct_change': (price / current_price - 1) * 100
        })
    
    return pd.DataFrame(results)
```

### 5.3 Volatility Regime Detection

This function detects the current volatility regime:

```python
def detect_volatility_regime(options_data, current_price):
    """
    Detect the current volatility regime based on options data.
    
    Parameters:
    -----------
    options_data : DataFrame
        DataFrame containing options data with vega metrics
    current_price : float
        Current price of the underlying asset
        
    Returns:
    --------
    dict
        Dictionary containing volatility regime information
    """
    # Calculate vega impact if not already done
    if 'vega_impact' not in options_data.columns:
        data = calculate_vega_impact(options_data, current_price)
    else:
        data = options_data.copy()
    
    # Calculate VPI if not already done
    if 'vpi' not in data.columns:
        data = calculate_volatility_pressure(data, current_price)
    
    # Calculate net vega exposure
    net_vega = data['vega_impact'].sum()
    
    # Calculate vega skew (difference between upside and downside vega)
    upside_vega = data[data['strike'] > current_price]['vega_impact'].sum()
    downside_vega = data[data['strike'] < current_price]['vega_impact'].sum()
    vega_skew = upside_vega - downside_vega
    
    # Calculate VPI distribution
    vpi_positive = data[data['vpi'] > 0]['vpi'].sum()
    vpi_negative = data[data['vpi'] < 0]['vpi'].sum()
    vpi_ratio = vpi_positive / abs(vpi_negative) if vpi_negative != 0 else float('inf')
    
    # Determine volatility regime
    if vpi_ratio > 2.0 and net_vega > 0:
        regime = "Strong Volatility Expansion"
        regime_score = min(1.0, vpi_ratio / 5.0)
    elif vpi_ratio > 1.5 and net_vega > 0:
        regime = "Moderate Volatility Expansion"
        regime_score = min(0.8, vpi_ratio / 5.0)
    elif vpi_ratio < 0.5 and net_vega < 0:
        regime = "Strong Volatility Contraction"
        regime_score = min(1.0, 1.0 / (vpi_ratio + 0.1))
    elif vpi_ratio < 0.67 and net_vega < 0:
        regime = "Moderate Volatility Contraction"
        regime_score = min(0.8, 1.0 / (vpi_ratio + 0.1))
    elif abs(vega_skew) / (abs(upside_vega) + abs(downside_vega)) > 0.3:
        if vega_skew > 0:
            regime = "Upside Volatility Skew"
        else:
            regime = "Downside Volatility Skew"
        regime_score = min(0.9, abs(vega_skew) / (abs(upside_vega) + abs(downside_vega)))
    else:
        regime = "Neutral Volatility"
        regime_score = 0.5
    
    return {
        'regime': regime,
        'score': regime_score,
        'net_vega': net_vega,
        'vega_skew': vega_skew,
        'vpi_ratio': vpi_ratio
    }
```

## 6. Visualization Functions

### 6.1 Strike Impact Heatmap

This function creates a heatmap of Greek impacts across strikes:

```python
def plot_strike_impact_heatmap(options_data, current_price, figsize=(14, 8)):
    """
    Create a heatmap visualization of Greek impacts across strikes.
    
    Parameters:
    -----------
    options_data : DataFrame
        DataFrame containing options data with calculated impacts
    current_price : float
        Current price of the underlying asset
    figsize : tuple, optional
        Figure size
        
    Returns:
    --------
    matplotlib.figure.Figure
        The created figure
    """
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    # Ensure all impacts are calculated
    data = calculate_composite_impact(options_data, current_price)
    
    # Select relevant columns and normalize
    impact_cols = ['delta_impact', 'gamma_impact', 'vega_impact', 'theta_impact', 'value_impact']
    plot_data = data[['strike'] + impact_cols].copy()
    
    # Normalize each impact column
    for col in impact_cols:
        max_abs = plot_data[col].abs().max()
        if max_abs > 0:
            plot_data[f'{col}_norm'] = plot_data[col] / max_abs
        else:
            plot_data[f'{col}_norm'] = 0
    
    # Prepare data for heatmap
    plot_data = plot_data.set_index('strike')
    norm_cols = [f'{col}_norm' for col in impact_cols]
    heatmap_data = plot_data[norm_cols].copy()
    
    # Rename columns for better display
    heatmap_data.columns = ['Delta', 'Gamma', 'Vega', 'Theta', 'Value']
    
    # Create figure
    fig, ax = plt.subplots(figsize=figsize)
    
    # Create heatmap
    sns.heatmap(heatmap_data.T, cmap='RdBu_r', center=0, vmin=-1, vmax=1, 
                linewidths=0.5, cbar_kws={'label': 'Normalized Impact'})
    
    # Add current price line
    plt.axvline(x=heatmap_data.index.get_loc(current_price, method='nearest'), 
                color='black', linestyle='--', linewidth=2, label='Current Price')
    
    # Add labels and title
    plt.title('Greek Impact Heatmap by Strike', fontsize=16)
    plt.xlabel('Strike Price', fontsize=12)
    plt.ylabel('Greek Metric', fontsize=12)
    
    # Add legend
    plt.legend(loc='upper right')
    
    return fig
```

### 6.2 Gamma Exposure Profile Visualization

This function visualizes the gamma exposure profile:

```python
def plot_gamma_exposure_profile(options_data, current_price, price_range=0.05, figsize=(14, 8)):
    """
    Create a visualization of the gamma exposure profile.
    
    Parameters:
    -----------
    options_data : DataFrame
        DataFrame containing options data with gamma metrics
    current_price : float
        Current price of the underlying asset
    price_range : float, optional
        Price range to analyze as a percentage of current price
    figsize : tuple, optional
        Figure size
        
    Returns:
    --------
    matplotlib.figure.Figure
        The created figure
    """
    import matplotlib.pyplot as plt
    
    # Calculate gamma exposure profile
    profile = calculate_gamma_exposure_profile(options_data, current_price, price_range)
    
    # Create figure
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot gamma exposure profile
    ax.plot(profile['price'], profile['gamma_exposure'], linewidth=2.5, color='blue')
    
    # Fill areas based on sign
    ax.fill_between(profile['price'], profile['gamma_exposure'], 0, 
                    where=(profile['gamma_exposure'] >= 0), 
                    color='green', alpha=0.3, label='Positive Gamma')
    ax.fill_between(profile['price'], profile['gamma_exposure'], 0, 
                    where=(profile['gamma_exposure'] < 0), 
                    color='red', alpha=0.3, label='Negative Gamma')
    
    # Add current price line
    ax.axvline(x=current_price, color='black', linestyle='--', linewidth=2, label='Current Price')
    
    # Add zero line
    ax.axhline(y=0, color='gray', linestyle='-', linewidth=1)
    
    # Add labels and title
    ax.set_title('Gamma Exposure Profile', fontsize=16)
    ax.set_xlabel('Price', fontsize=12)
    ax.set_ylabel('Gamma Exposure', fontsize=12)
    
    # Add legend
    ax.legend(loc='upper right')
    
    # Add grid
    ax.grid(True, alpha=0.3)
    
    # Add price percentage labels on secondary x-axis
    ax2 = ax.twiny()
    ax2.set_xlim(ax.get_xlim())
    ax2.set_xticks(profile['price'][::10])
    ax2.set_xticklabels([f"{x:.1f}%" for x in profile['price_pct_change'][::10]])
    ax2.set_xlabel('Price Change %', fontsize=12)
    
    return fig
```

### 6.3 Composite Impact Visualization

This function creates a comprehensive visualization of all impacts:

```python
def plot_composite_impact(options_data, current_price, figsize=(16, 12)):
    """
    Create a comprehensive visualization of all impacts.
    
    Parameters:
    -----------
    options_data : DataFrame
        DataFrame containing options data with calculated impacts
    current_price : float
        Current price of the underlying asset
    figsize : tuple, optional
        Figure size
        
    Returns:
    --------
    matplotlib.figure.Figure
        The created figure
    """
    import matplotlib.pyplot as plt
    
    # Ensure all impacts are calculated
    data = calculate_composite_impact(options_data, current_price)
    data = calculate_strike_magnetism(data, current_price)
    data = calculate_volatility_pressure(data, current_price)
    
    # Create figure with subplots
    fig, axs = plt.subplots(3, 1, figsize=figsize, gridspec_kw={'height_ratios': [2, 1, 1]})
    
    # Plot 1: Composite Impact
    axs[0].bar(data['strike'], data['composite_impact'], width=current_price*0.002, 
               color=data['composite_impact'].apply(lambda x: 'green' if x > 0 else 'red'))
    axs[0].axvline(x=current_price, color='black', linestyle='--', linewidth=2, label='Current Price')
    axs[0].axhline(y=0, color='gray', linestyle='-', linewidth=1)
    axs[0].set_title('Composite Impact by Strike', fontsize=16)
    axs[0].set_xlabel('Strike Price', fontsize=12)
    axs[0].set_ylabel('Composite Impact', fontsize=12)
    axs[0].legend(loc='upper right')
    axs[0].grid(True, alpha=0.3)
    
    # Plot 2: Strike Magnetism Index
    axs[1].bar(data['strike'], data['smi'], width=current_price*0.002, 
               color=data['smi'].apply(lambda x: 'green' if x > 0 else 'red'))
    axs[1].axvline(x=current_price, color='black', linestyle='--', linewidth=2, label='Current Price')
    axs[1].axhline(y=0, color='gray', linestyle='-', linewidth=1)
    axs[1].set_title('Strike Magnetism Index', fontsize=16)
    axs[1].set_xlabel('Strike Price', fontsize=12)
    axs[1].set_ylabel('SMI', fontsize=12)
    axs[1].legend(loc='upper right')
    axs[1].grid(True, alpha=0.3)
    
    # Plot 3: Volatility Pressure Index
    axs[2].bar(data['strike'], data['vpi'], width=current_price*0.002, 
               color=data['vpi'].apply(lambda x: 'green' if x > 0 else 'red'))
    axs[2].axvline(x=current_price, color='black', linestyle='--', linewidth=2, label='Current Price')
    axs[2].axhline(y=0, color='gray', linestyle='-', linewidth=1)
    axs[2].set_title('Volatility Pressure Index', fontsize=16)
    axs[2].set_xlabel('Strike Price', fontsize=12)
    axs[2].set_ylabel('VPI', fontsize=12)
    axs[2].legend(loc='upper right')
    axs[2].grid(True, alpha=0.3)
    
    # Adjust layout
    plt.tight_layout()
    
    return fig
```

## 7. Integration with Dash/Plotly

### 7.1 Plotly Heatmap Implementation

This function creates an interactive Plotly heatmap for Dash integration:

```python
def create_plotly_impact_heatmap(options_data, current_price):
    """
    Create an interactive Plotly heatmap of Greek impacts.
    
    Parameters:
    -----------
    options_data : DataFrame
        DataFrame containing options data with calculated impacts
    current_price : float
        Current price of the underlying asset
        
    Returns:
    --------
    plotly.graph_objects.Figure
        The created Plotly figure
    """
    import plotly.graph_objects as go
    import numpy as np
    
    # Ensure all impacts are calculated
    data = calculate_composite_impact(options_data, current_price)
    
    # Select relevant columns and normalize
    impact_cols = ['delta_impact', 'gamma_impact', 'vega_impact', 'theta_impact', 'value_impact']
    plot_data = data[['strike'] + impact_cols].copy()
    
    # Normalize each impact column
    for col in impact_cols:
        max_abs = plot_data[col].abs().max()
        if max_abs > 0:
            plot_data[f'{col}_norm'] = plot_data[col] / max_abs
        else:
            plot_data[f'{col}_norm'] = 0
    
    # Prepare data for heatmap
    strikes = plot_data['strike'].tolist()
    metrics = ['Delta', 'Gamma', 'Vega', 'Theta', 'Value']
    z_data = []
    
    for col in [f'{c}_norm' for c in impact_cols]:
        z_data.append(plot_data[col].tolist())
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=z_data,
        x=strikes,
        y=metrics,
        colorscale='RdBu_r',
        zmid=0,
        zmin=-1,
        zmax=1,
        colorbar=dict(
            title='Normalized Impact',
            titleside='right',
            titlefont=dict(size=14),
            tickfont=dict(size=12),
        ),
        hovertemplate='Strike: %{x}<br>Metric: %{y}<br>Impact: %{z:.2f}<extra></extra>'
    ))
    
    # Add current price marker
    fig.add_shape(
        type="line",
        x0=current_price,
        y0=-0.5,
        x1=current_price,
        y1=len(metrics)-0.5,
        line=dict(color="black", width=2, dash="dash"),
    )
    
    # Add annotation for current price
    fig.add_annotation(
        x=current_price,
        y=len(metrics)-0.5,
        text=f"Current Price: {current_price}",
        showarrow=True,
        arrowhead=1,
        ax=0,
        ay=-40
    )
    
    # Update layout
    fig.update_layout(
        title=dict(
            text='Greek Impact Heatmap by Strike',
            font=dict(size=20, color='#2c3e50'),
            x=0.5,
            xanchor='center'
        ),
        plot_bgcolor='rgba(240, 240, 240, 0.8)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2c3e50'),
        margin=dict(l=40, r=40, t=60, b=40),
        xaxis=dict(
            title='Strike Price',
            titlefont=dict(size=14),
            gridcolor='white',
            linecolor='white',
        ),
        yaxis=dict(
            title='Greek Metric',
            titlefont=dict(size=14),
            gridcolor='white',
            linecolor='white',
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=14,
            font_family="Arial"
        )
    )
    
    return fig
```

### 7.2 Plotly Gamma Exposure Profile

This function creates an interactive Plotly visualization of gamma exposure:

```python
def create_plotly_gamma_profile(options_data, current_price, price_range=0.05):
    """
    Create an interactive Plotly visualization of gamma exposure profile.
    
    Parameters:
    -----------
    options_data : DataFrame
        DataFrame containing options data with gamma metrics
    current_price : float
        Current price of the underlying asset
    price_range : float, optional
        Price range to analyze as a percentage of current price
        
    Returns:
    --------
    plotly.graph_objects.Figure
        The created Plotly figure
    """
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    
    # Calculate gamma exposure profile
    profile = calculate_gamma_exposure_profile(options_data, current_price, price_range)
    
    # Create figure
    fig = go.Figure()
    
    # Add gamma exposure trace
    fig.add_trace(go.Scatter(
        x=profile['price'],
        y=profile['gamma_exposure'],
        mode='lines',
        name='Gamma Exposure',
        line=dict(color='blue', width=3),
        hovertemplate='Price: %{x:.2f}<br>Gamma Exposure: %{y:.2f}<extra></extra>'
    ))
    
    # Add filled areas for positive and negative gamma
    fig.add_trace(go.Scatter(
        x=profile['price'],
        y=profile['gamma_exposure'],
        mode='none',
        name='Positive Gamma',
        fill='tozeroy',
        fillcolor='rgba(0, 255, 0, 0.3)',
        hoverinfo='skip',
        visible=True,
        showlegend=True
    ))
    
    # Add current price marker
    fig.add_shape(
        type="line",
        x0=current_price,
        y0=min(profile['gamma_exposure']),
        x1=current_price,
        y1=max(profile['gamma_exposure']),
        line=dict(color="black", width=2, dash="dash"),
    )
    
    # Add zero line
    fig.add_shape(
        type="line",
        x0=min(profile['price']),
        y0=0,
        x1=max(profile['price']),
        y1=0,
        line=dict(color="gray", width=1),
    )
    
    # Add annotation for current price
    fig.add_annotation(
        x=current_price,
        y=max(profile['gamma_exposure']),
        text=f"Current Price: {current_price}",
        showarrow=True,
        arrowhead=1,
        ax=0,
        ay=-40
    )
    
    # Update layout
    fig.update_layout(
        title=dict(
            text='Gamma Exposure Profile',
            font=dict(size=20, color='#2c3e50'),
            x=0.5,
            xanchor='center'
        ),
        plot_bgcolor='rgba(240, 240, 240, 0.8)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2c3e50'),
        margin=dict(l=40, r=40, t=60, b=40),
        xaxis=dict(
            title='Price',
            titlefont=dict(size=14),
            gridcolor='white',
            linecolor='white',
            tickformat='.2f'
        ),
        yaxis=dict(
            title='Gamma Exposure',
            titlefont=dict(size=14),
            gridcolor='white',
            linecolor='white',
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=14,
            font_family="Arial"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Add secondary x-axis for percentage change
    fig.update_layout(
        xaxis2=dict(
            title='Price Change %',
            titlefont=dict(size=14),
            overlaying='x',
            side='top',
            showgrid=False,
            tickvals=profile['price'][::10],
            ticktext=[f"{x:.1f}%" for x in profile['price_pct_change'][::10]],
        )
    )
    
    return fig
```

### 7.3 Dash Layout Implementation

Here's a sample Dash layout implementation:

```python
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np

# Import the functions defined above
# ...

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# Define the layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Enhanced Options Greek Analysis Dashboard", className="text-center mb-4"), width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Input Parameters"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Label("Current Price:"),
                            dbc.Input(id="current-price", type="number", value=500, step=0.01)
                        ], width=6),
                        dbc.Col([
                            html.Label("Price Range (%):"),
                            dbc.Input(id="price-range", type="number", value=5, step=0.1)
                        ], width=6)
                    ]),
                    dbc.Button("Update Analysis", id="update-button", color="primary", className="mt-3")
                ])
            ], className="mb-4")
        ], width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Greek Impact Heatmap"),
                dbc.CardBody([
                    dcc.Graph(id="impact-heatmap")
                ])
            ], className="mb-4")
        ], width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Gamma Exposure Profile"),
                dbc.CardBody([
                    dcc.Graph(id="gamma-profile")
                ])
            ], className="mb-4")
        ], width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Key Levels"),
                dbc.CardBody([
                    html.Div(id="key-levels-output")
                ])
            ], className="mb-4")
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Volatility Regime"),
                dbc.CardBody([
                    html.Div(id="volatility-regime-output")
                ])
            ], className="mb-4")
        ], width=6)
    ])
], fluid=True)

# Define callback to update all visualizations
@app.callback(
    [Output("impact-heatmap", "figure"),
     Output("gamma-profile", "figure"),
     Output("key-levels-output", "children"),
     Output("volatility-regime-output", "children")],
    [Input("update-button", "n_clicks")],
    [State("current-price", "value"),
     State("price-range", "value")]
)
def update_analysis(n_clicks, current_price, price_range):
    # Load or generate sample data
    # In a real implementation, this would load data from your data source
    options_data = generate_sample_data(current_price)
    
    # Calculate all metrics
    data = calculate_composite_impact(options_data, current_price)
    data = calculate_strike_magnetism(data, current_price)
    data = calculate_volatility_pressure(data, current_price)
    
    # Create heatmap
    heatmap_fig = create_plotly_impact_heatmap(data, current_price)
    
    # Create gamma profile
    gamma_fig = create_plotly_gamma_profile(data, current_price, price_range/100)
    
    # Identify key levels
    key_levels = identify_key_levels(data, current_price)
    
    # Format key levels output
    key_levels_html = []
    
    # Add support levels
    key_levels_html.append(html.H5("Support Levels:"))
    for i, level in enumerate(key_levels['support'][:3]):  # Show top 3
        key_levels_html.append(html.Div([
            html.Strong(f"Level {i+1}: "),
            f"${level['strike']:.2f} (Strength: {level['strength']:.2f})"
        ], className="mb-2"))
    
    # Add resistance levels
    key_levels_html.append(html.H5("Resistance Levels:", className="mt-3"))
    for i, level in enumerate(key_levels['resistance'][:3]):  # Show top 3
        key_levels_html.append(html.Div([
            html.Strong(f"Level {i+1}: "),
            f"${level['strike']:.2f} (Strength: {level['strength']:.2f})"
        ], className="mb-2"))
    
    # Detect volatility regime
    vol_regime = detect_volatility_regime(data, current_price)
    
    # Format volatility regime output
    vol_regime_html = [
        html.H5(f"Current Regime: {vol_regime['regime']}"),
        html.Div([
            html.Strong("Confidence Score: "),
            f"{vol_regime['score']:.2f}"
        ], className="mb-2"),
        html.Div([
            html.Strong("Net Vega Exposure: "),
            f"{vol_regime['net_vega']:.2f}"
        ], className="mb-2"),
        html.Div([
            html.Strong("Vega Skew: "),
            f"{vol_regime['vega_skew']:.2f}"
        ], className="mb-2"),
        html.Div([
            html.Strong("VPI Ratio: "),
            f"{vol_regime['vpi_ratio']:.2f}"
        ], className="mb-2")
    ]
    
    return heatmap_fig, gamma_fig, key_levels_html, vol_regime_html

# Helper function to generate sample data
def generate_sample_data(current_price):
    # Generate strikes around current price
    strikes = np.linspace(current_price * 0.9, current_price * 1.1, 21)
    
    # Initialize data
    data = []
    
    for strike in strikes:
        # Calculate proximity
        proximity = 1 - min(1, abs(strike - current_price) / (current_price * 0.05))
        
        # Generate sample values
        row = {
            'strike': strike,
            'deltas_call_buy': np.random.normal(500, 100) * proximity if strike < current_price * 1.05 else np.random.normal(300, 100) * proximity,
            'deltas_call_sell': np.random.normal(300, 80) * proximity if strike < current_price * 1.05 else np.random.normal(400, 100) * proximity,
            'deltas_put_buy': np.random.normal(400, 100) * proximity if strike > current_price * 0.95 else np.random.normal(300, 100) * proximity,
            'deltas_put_sell': np.random.normal(250, 80) * proximity if strike > current_price * 0.95 else np.random.normal(350, 100) * proximity,
            'gammas_call_buy': np.random.normal(100, 30) * proximity,
            'gammas_call_sell': np.random.normal(60, 20) * proximity,
            'gammas_put_buy': np.random.normal(90, 30) * proximity,
            'gammas_put_sell': np.random.normal(55, 20) * proximity,
            'vegas_call_buy': np.random.normal(5000, 1000) * proximity,
            'vegas_call_sell': np.random.normal(3000, 800) * proximity,
            'vegas_put_buy': np.random.normal(4500, 1000) * proximity,
            'vegas_put_sell': np.random.normal(2800, 800) * proximity,
            'thetas_call_buy': np.random.normal(-3000, 500) * proximity,
            'thetas_call_sell': np.random.normal(1800, 400) * proximity,
            'thetas_put_buy': np.random.normal(-2600, 500) * proximity,
            'thetas_put_sell': np.random.normal(1600, 400) * proximity,
            'value_call_buy': np.random.normal(150000, 30000) * proximity,
            'value_call_sell': np.random.normal(90000, 20000) * proximity,
            'value_put_buy': np.random.normal(120000, 30000) * proximity,
            'value_put_sell': np.random.normal(75000, 20000) * proximity,
            'volm_call_buy': np.random.normal(1000, 200) * proximity,
            'volm_call_sell': np.random.normal(600, 150) * proximity,
            'volm_put_buy': np.random.normal(800, 200) * proximity,
            'volm_put_sell': np.random.normal(500, 150) * proximity,
            'oi': np.random.normal(5000, 1000) * proximity,
            'oi_ch': np.random.normal(200, 100) * proximity
        }
        
        data.append(row)
    
    return pd.DataFrame(data)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
```

## 8. Implementation Recommendations

### 8.1 Data Processing Pipeline

For optimal implementation, follow this data processing pipeline:

1. **Data Collection**:
   - Collect options data from ConvexValue at regular intervals (5-15 minutes recommended)
   - Store data in a structured format (e.g., pandas DataFrame, SQL database)
   - Include all required metrics (deltas, gammas, vegas, thetas, volume, value)

2. **Data Preprocessing**:
   - Clean and validate data (remove outliers, handle missing values)
   - Calculate proximity factors for each strike
   - Normalize metrics for consistent scaling

3. **Impact Calculation**:
   - Calculate individual Greek impacts using the enhanced formulas
   - Calculate composite impacts and specialized metrics (SMI, VPI)
   - Identify key levels and detect volatility regime

4. **Visualization**:
   - Create interactive visualizations using Plotly/Dash
   - Update visualizations at regular intervals
   - Highlight significant changes and key levels

5. **Alert System**:
   - Set up alerts for significant changes in impact metrics
   - Monitor for regime shifts and key level breaches
   - Provide actionable insights based on the analysis

### 8.2 Performance Optimization

For optimal performance:

1. **Vectorized Operations**:
   - Use pandas and numpy vectorized operations instead of loops
   - Precompute common factors used across multiple calculations
   - Use efficient data structures for lookups and aggregations

2. **Caching**:
   - Implement caching for expensive calculations
   - Cache intermediate results that are reused across functions
   - Consider using libraries like `functools.lru_cache` or Redis for caching

3. **Parallel Processing**:
   - Use multiprocessing for independent calculations
   - Consider using Dask for larger datasets
   - Implement asynchronous processing for data collection and visualization updates

4. **Memory Management**:
   - Avoid creating unnecessary copies of large DataFrames
   - Use inplace operations where appropriate
   - Implement cleanup routines for historical data

### 8.3 Integration with Existing Systems

To integrate with your existing Elite Options Trading System:

1. **Data Integration**:
   - Create a unified data model that combines ConvexValue data with other sources
   - Implement adapters for different data formats and sources
   - Establish a consistent update cycle across all data sources

2. **Visualization Integration**:
   - Use a modular approach to add new visualizations to existing dashboards
   - Implement consistent styling and interaction patterns
   - Provide context-switching between different analysis views

3. **Signal Integration**:
   - Incorporate enhanced Greek impact metrics into existing signal generation
   - Use composite impact scores as filters or confirmations for existing signals
   - Develop new signals based on the enhanced metrics

4. **Strategy Integration**:
   - Adapt existing strategies to account for the enhanced understanding of Greek impacts
   - Develop new strategies that specifically target high-impact strikes
   - Implement regime-specific strategy selection based on volatility regime detection

## 9. Conclusion

This comprehensive guide provides enhanced formulas and implementation details for accurately representing the impact of options Greek metrics on underlying asset price action. By implementing these formulas and visualization techniques, you can significantly improve your understanding of market structure and make more informed trading decisions.

The key innovations in this guide include:

1. **Enhanced Impact Weighting**: Accounting for the asymmetric impact of bought versus sold options
2. **Proximity-Based Adjustments**: Incorporating strike proximity to current price for more accurate impact assessment
3. **Composite Impact Metrics**: Combining multiple Greeks for a holistic view of market structure
4. **Advanced Analysis Functions**: Identifying key levels, detecting volatility regimes, and analyzing gamma exposure profiles
5. **Interactive Visualizations**: Creating informative and intuitive visualizations for better decision-making

By integrating these enhancements into your Python scripts, you can create a more powerful, reliable, and accurate representation of how options positioning impacts underlying asset price action.
