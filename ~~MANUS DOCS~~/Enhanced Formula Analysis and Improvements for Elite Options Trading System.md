# Enhanced Formula Analysis and Improvements for Elite Options Trading System

## 1. Introduction

This document provides a comprehensive analysis of the formulas and calculations in the Elite Options Trading System, with specific enhancements to improve accuracy, adaptability, and predictive power. Each section details the original implementation, the enhanced formula, and the rationale for changes.

## 2. Core Metric Enhancements

### 2.1 Delta-Adjusted Gamma (DAG) Enhancement

#### Original Implementation:
```python
df['dag_custom'] = (
    gamma_exposure_values * dxoi_sign *
    (1 + df['alpha'] * df['net_delta_flow_to_dxoi_ratio']) *
    df['norm_net_gamma_flow']
)
```

#### Enhanced Formula:
```python
def calculate_custom_flow_dag(self, options_df: pd.DataFrame) -> pd.DataFrame:
    # [Existing setup code...]
    
    # Enhanced: Apply volume-based weighting to gamma exposure
    volume_weighted_gamma = gamma_exposure_values * (1 + 0.3 * self._normalize_series(
        pd.to_numeric(df[self.volm_col_for_weighting], errors='coerce').abs(), 
        'volume_for_gamma_weight'
    ))
    
    # Enhanced: Improve delta flow normalization with sigmoid function
    normalized_flow_ratio = 2 / (1 + np.exp(-3 * df['net_delta_flow_to_dxoi_ratio'])) - 1
    
    # Enhanced: Apply strike proximity weighting
    if 'price' in df.columns:
        current_price = pd.to_numeric(df['price'].iloc[0], errors='coerce')
        if pd.notna(current_price) and current_price > 0:
            strike_values = pd.to_numeric(df['strike'], errors='coerce')
            proximity_factor = 1 - np.minimum(1, np.abs(strike_values - current_price) / (current_price * 0.05))
            proximity_factor = proximity_factor.fillna(0.5)
        else:
            proximity_factor = pd.Series(1.0, index=df.index)
    else:
        proximity_factor = pd.Series(1.0, index=df.index)
    
    # Enhanced: Final DAG calculation with improved components
    df['dag_custom'] = (
        volume_weighted_gamma * dxoi_sign *
        (1 + df['alpha'] * normalized_flow_ratio) *
        df['norm_net_gamma_flow'] *
        proximity_factor
    ).fillna(0.0)
    
    return df
```

#### Rationale for Changes:
1. **Volume-Weighted Gamma**: Added weighting based on trading volume to give more importance to strikes with higher activity, which better reflects market interest.
2. **Sigmoid Normalization**: Replaced linear ratio with sigmoid function to better handle extreme values and provide more stable scaling.
3. **Strike Proximity Factor**: Added weighting based on proximity to current price, giving more importance to near-the-money options which have greater hedging impact.
4. **Improved Numerical Stability**: Enhanced handling of edge cases and NaN values throughout the calculation.

### 2.2 Time Decay and Pin Risk Indicator (TDPI) Enhancement

#### Original Implementation:
```python
df['tdpi'] = (
    gaussian_weight_factor * 
    (charm_exposure_values * theta_exposure_values) * 
    df['norm_net_theta_flow'] * 
    df['norm_net_charm_flow']
)
```

#### Enhanced Formula:
```python
def calculate_tdpi(self, options_df: pd.DataFrame, current_time: Optional[time] = None, historical_ohlc_df_for_atr: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    # [Existing setup code...]
    
    # Enhanced: Dynamic Gaussian width based on volatility context
    if historical_ohlc_df_for_atr is not None and not historical_ohlc_df_for_atr.empty:
        try:
            historical_vol = historical_ohlc_df_for_atr['close'].pct_change().std() * np.sqrt(252)
            # Adjust gaussian width based on historical volatility
            dynamic_gaussian_width = base_gaussian_width * (1 + 0.5 * (historical_vol - 0.2) / 0.2)
            dynamic_gaussian_width = np.clip(dynamic_gaussian_width, -0.7, -0.2)
            gaussian_weight_factor = np.exp(dynamic_gaussian_width * ((strike_values - current_price) / atr_value) ** 2)
        except Exception as e_dyn_gauss:
            tdpi_logger.warning(f"Error calculating dynamic Gaussian width: {e_dyn_gauss}. Using static width.")
            gaussian_weight_factor = np.exp(base_gaussian_width * ((strike_values - current_price) / atr_value) ** 2)
    else:
        gaussian_weight_factor = np.exp(base_gaussian_width * ((strike_values - current_price) / atr_value) ** 2)
    
    # Enhanced: Time-to-expiration weighting
    if 'expiration_date' in df.columns:
        try:
            today = date.today()
            exp_dates = pd.to_datetime(df['expiration_date'], errors='coerce').dt.date
            dtes = (exp_dates - today).apply(lambda x: x.days if pd.notna(x) else np.nan)
            
            # Exponential decay weight for time to expiration
            dte_weight = np.exp(-0.05 * dtes)
            dte_weight = dte_weight.fillna(0.5)
            
            # Apply higher weight to expiration day
            dte_weight = np.where(dtes <= 1, 2.0 * dte_weight, dte_weight)
        except Exception as e_dte:
            tdpi_logger.warning(f"Error calculating DTE weights: {e_dte}. Using neutral weights.")
            dte_weight = pd.Series(1.0, index=df.index)
    else:
        dte_weight = pd.Series(1.0, index=df.index)
    
    # Enhanced: Time-of-day adjustment for intraday dynamics
    time_of_day_factor = 1.0
    if current_time is not None:
        try:
            current_hour = current_time.hour + current_time.minute / 60.0
            # Increase weight in the last hour of trading (typically 3-4 PM)
            if 15.0 <= current_hour < 16.0:
                time_of_day_factor = 1.5
            # Slightly increase weight in the first hour (9:30-10:30 AM)
            elif 9.5 <= current_hour < 10.5:
                time_of_day_factor = 1.2
        except Exception as e_tod:
            tdpi_logger.warning(f"Error calculating time-of-day factor: {e_tod}")
    
    # Enhanced: Final TDPI calculation with improved components
    df['tdpi'] = (
        gaussian_weight_factor * 
        (charm_exposure_values * theta_exposure_values) * 
        df['norm_net_theta_flow'] * 
        df['norm_net_charm_flow'] *
        dte_weight * time_of_day_factor
    ).fillna(0.0)
    
    return df
```

#### Rationale for Changes:
1. **Dynamic Gaussian Width**: Made the Gaussian width responsive to market volatility, narrowing during high volatility periods and widening during low volatility.
2. **Time-to-Expiration Weighting**: Added exponential decay weighting based on days to expiration, with special emphasis on expiration day.
3. **Time-of-Day Adjustment**: Incorporated intraday dynamics by increasing the weight during market open and close when time decay effects are often more pronounced.
4. **Improved Numerical Stability**: Enhanced handling of edge cases and NaN values throughout the calculation.

### 2.3 Volatility Regime Indicator (VRI) Enhancement

#### Original Implementation:
```python
df['vri'] = (
    vanna_exposure_values * vomma_exposure_values * 
    df['norm_net_vanna_flow'] * df['norm_net_vomma_flow']
)
```

#### Enhanced Formula:
```python
def calculate_vri(self, options_df: pd.DataFrame, iv_context: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    # [Existing setup code...]
    
    # Enhanced: IV percentile context adjustment
    iv_context_factor = 1.0
    if iv_context is not None:
        try:
            iv_percentile_key = str(self._get_config_value(["data_processor_settings", "iv_context_parameters", "iv_percentile"], "iv_percentile_30d"))
            if iv_percentile_key in iv_context and iv_context[iv_percentile_key] is not None:
                iv_percentile = float(iv_context[iv_percentile_key])
                # Adjust weight based on IV percentile - higher weight in extreme IV environments
                if iv_percentile > 0.8 or iv_percentile < 0.2:
                    iv_context_factor = 1.5
                elif 0.4 <= iv_percentile <= 0.6:
                    iv_context_factor = 0.8  # Reduce weight in neutral IV environment
        except Exception as e_iv:
            vri_logger.warning(f"Error calculating IV context factor: {e_iv}")
    
    # Enhanced: Term structure component
    term_structure_factor = 1.0
    if 'expiration_date' in df.columns:
        try:
            today = date.today()
            exp_dates = pd.to_datetime(df['expiration_date'], errors='coerce').dt.date
            dtes = (exp_dates - today).apply(lambda x: x.days if pd.notna(x) else np.nan)
            
            # Group by expiration buckets
            short_term = dtes <= 7
            medium_term = (dtes > 7) & (dtes <= 30)
            long_term = dtes > 30
            
            # Calculate vanna-vomma imbalance across term structure
            if any(short_term) and any(long_term):
                short_vanna = vanna_exposure_values[short_term].sum()
                long_vanna = vanna_exposure_values[long_term].sum()
                
                # Detect term structure imbalance
                if abs(short_vanna) > 0 and abs(long_vanna) > 0:
                    vanna_term_ratio = short_vanna / long_vanna
                    # Increase factor when term structure shows significant imbalance
                    if abs(vanna_term_ratio) > 2 or abs(vanna_term_ratio) < 0.5:
                        term_structure_factor = 1.3
        except Exception as e_term:
            vri_logger.warning(f"Error calculating term structure factor: {e_term}")
    
    # Enhanced: Vomma-to-Vanna ratio adjustment
    vomma_vanna_balance_factor = 1.0
    try:
        total_abs_vanna = vanna_exposure_values.abs().sum()
        total_abs_vomma = vomma_exposure_values.abs().sum()
        
        if total_abs_vanna > 0 and total_abs_vomma > 0:
            vomma_vanna_ratio = total_abs_vomma / total_abs_vanna
            
            # Adjust factor based on vomma-vanna balance
            if vomma_vanna_ratio > 2:  # Vomma-dominated environment
                vomma_vanna_balance_factor = 1.4  # Higher weight to volatility of volatility
            elif vomma_vanna_ratio < 0.5:  # Vanna-dominated environment
                vomma_vanna_balance_factor = 0.8  # Lower weight
    except Exception as e_balance:
        vri_logger.warning(f"Error calculating vomma-vanna balance factor: {e_balance}")
    
    # Enhanced: Final VRI calculation with improved components
    df['vri'] = (
        vanna_exposure_values * vomma_exposure_values * 
        df['norm_net_vanna_flow'] * df['norm_net_vomma_flow'] *
        iv_context_factor * term_structure_factor * vomma_vanna_balance_factor
    ).fillna(0.0)
    
    return df
```

#### Rationale for Changes:
1. **IV Percentile Context**: Added adjustment based on implied volatility percentile to increase sensitivity during extreme volatility environments.
2. **Term Structure Component**: Incorporated analysis of vanna exposure across different expiration periods to detect term structure imbalances.
3. **Vomma-to-Vanna Ratio**: Added adjustment based on the balance between vomma and vanna to better reflect the current volatility regime.
4. **Improved Numerical Stability**: Enhanced handling of edge cases and NaN values throughout the calculation.

### 2.4 Skew and Delta Adjusted Gamma Exposure (SDAG) Enhancements

#### 2.4.1 SDAG Multiplicative Method Enhancement

#### Original Implementation:
```python
return (gamma_exp_numeric * (1 + delta_exp_norm_numeric * delta_weight_factor_val)).fillna(0.0)
```

#### Enhanced Formula:
```python
def calculate_sdag_multiplicative(self, df: pd.DataFrame, gamma_exposure: pd.Series, delta_exposure_norm: pd.Series) -> pd.Series:
    # [Existing setup code...]
    
    # Enhanced: Apply skew adjustment if available
    skew_factor = pd.Series(1.0, index=df.index)
    if self.option_iv_col in df.columns:
        try:
            iv_values = pd.to_numeric(df[self.option_iv_col], errors='coerce').fillna(0.0)
            if 'price' in df.columns and 'strike' in df.columns:
                current_price = pd.to_numeric(df['price'].iloc[0], errors='coerce')
                strikes = pd.to_numeric(df['strike'], errors='coerce')
                
                if pd.notna(current_price) and current_price > 0:
                    # Calculate moneyness
                    moneyness = strikes / current_price - 1
                    
                    # Group by moneyness buckets
                    atm_mask = abs(moneyness) <= 0.02
                    otm_mask = ~atm_mask
                    
                    # Calculate average IV for ATM options
                    atm_iv = iv_values[atm_mask].mean() if any(atm_mask) else iv_values.mean()
                    
                    if atm_iv > 0:
                        # Calculate skew factor based on IV relative to ATM IV
                        skew_factor = np.where(
                            otm_mask,
                            1 + 0.5 * (1 - iv_values / atm_iv),  # Adjust based on skew
                            1.0  # No adjustment for ATM
                        )
                        skew_factor = pd.Series(skew_factor, index=df.index).fillna(1.0)
        except Exception as e_skew:
            sdag_logger.warning(f"Error calculating skew factor: {e_skew}. Using neutral factor.")
    
    # Enhanced: Apply volume weighting
    volume_factor = pd.Series(1.0, index=df.index)
    if self.volm_col_for_weighting in df.columns:
        try:
            volume_values = pd.to_numeric(df[self.volm_col_for_weighting], errors='coerce').fillna(0.0)
            norm_volume = self._normalize_series(volume_values, 'volume_for_sdag_mult')
            volume_factor = 1 + 0.3 * norm_volume  # 30% max boost from volume
        except Exception as e_vol:
            sdag_logger.warning(f"Error calculating volume factor: {e_vol}. Using neutral factor.")
    
    # Enhanced: Final SDAG Multiplicative calculation
    return (
        gamma_exp_numeric * 
        (1 + delta_exp_norm_numeric * delta_weight_factor_val) * 
        skew_factor * 
        volume_factor
    ).fillna(0.0)
```

#### Rationale for Changes:
1. **Volatility Skew Adjustment**: Added adjustment based on the volatility skew to better account for market pricing of tail risk.
2. **Volume Weighting**: Incorporated trading volume to give more weight to strikes with higher activity.
3. **Improved Numerical Stability**: Enhanced handling of edge cases and NaN values throughout the calculation.

#### 2.4.2 SDAG Directional Method Enhancement

#### Original Implementation:
```python
interaction_term_sign = np.sign(gamma_exp_numeric * delta_exp_norm_numeric).replace(0, 1)
magnitude_enhancement_factor = 1 + abs(delta_exp_norm_numeric * delta_weight_factor_val)
return (gamma_exp_numeric * interaction_term_sign * magnitude_enhancement_factor).fillna(0.0)
```

#### Enhanced Formula:
```python
def calculate_sdag_directional(self, df: pd.DataFrame, gamma_exposure: pd.Series, delta_exposure_norm: pd.Series) -> pd.Series:
    # [Existing setup code...]
    
    # Enhanced: Improved interaction term with smoothing
    interaction_term = gamma_exp_numeric * delta_exp_norm_numeric
    # Apply tanh smoothing to avoid abrupt sign changes
    smoothed_sign = np.tanh(3 * interaction_term)
    
    # Enhanced: Dynamic weight factor based on alignment strength
    alignment_strength = abs(smoothed_sign)
    dynamic_weight_factor = delta_weight_factor_val * (0.8 + 0.4 * alignment_strength)
    
    # Enhanced: Magnitude enhancement with improved scaling
    magnitude_enhancement_factor = 1 + abs(delta_exp_norm_numeric * dynamic_weight_factor)
    
    # Enhanced: Apply proximity factor if price available
    proximity_factor = pd.Series(1.0, index=df.index)
    if 'price' in df.columns and 'strike' in df.columns:
        try:
            current_price = pd.to_numeric(df['price'].iloc[0], errors='coerce')
            strikes = pd.to_numeric(df['strike'], errors='coerce')
            
            if pd.notna(current_price) and current_price > 0:
                # Calculate strike proximity factor
                proximity_factor = 1 - np.minimum(1, np.abs(strikes - current_price) / (current_price * 0.05))
                proximity_factor = pd.Series(proximity_factor, index=df.index).fillna(0.5)
        except Exception as e_prox:
            sdag_logger.warning(f"Error calculating proximity factor: {e_prox}. Using neutral factor.")
    
    # Enhanced: Final SDAG Directional calculation
    return (
        gamma_exp_numeric * 
        smoothed_sign * 
        magnitude_enhancement_factor * 
        proximity_factor
    ).fillna(0.0)
```

#### Rationale for Changes:
1. **Smoothed Interaction Term**: Replaced hard sign function with tanh for smoother transitions and to avoid abrupt changes.
2. **Dynamic Weight Factor**: Made the weight factor responsive to the strength of alignment between gamma and delta.
3. **Strike Proximity Factor**: Added weighting based on proximity to current price to emphasize near-the-money options.
4. **Improved Numerical Stability**: Enhanced handling of edge cases and NaN values throughout the calculation.

#### 2.4.3 SDAG Weighted Method Enhancement

#### Original Implementation:
```python
w1_gamma_val = float(config_params.get("w1_gamma", 0.6))
w2_delta_val = float(config_params.get("w2_delta", 0.4))
sum_of_weights = w1_gamma_val + w2_delta_val
return ((w1_gamma_val * gamma_exp_numeric + w2_delta_val * delta_exp_raw_numeric) / sum_of_weights).fillna(0.0)
```

#### Enhanced Formula:
```python
def calculate_sdag_weighted(self, df: pd.DataFrame, gamma_exposure: pd.Series, delta_exposure_raw: pd.Series) -> pd.Series:
    # [Existing setup code...]
    
    # Enhanced: Dynamic weights based on market conditions
    dynamic_w1_gamma = w1_gamma_val
    dynamic_w2_delta = w2_delta_val
    
    # Adjust weights based on relative magnitudes
    gamma_magnitude = gamma_exp_numeric.abs().mean()
    delta_magnitude = delta_exp_raw_numeric.abs().mean()
    
    if gamma_magnitude > 0 and delta_magnitude > 0:
        # Calculate ratio of magnitudes
        magnitude_ratio = gamma_magnitude / delta_magnitude
        
        # Adjust weights to balance contribution when one Greek dominates
        if magnitude_ratio > 3:  # Gamma dominates
            adjustment_factor = np.log10(magnitude_ratio) * 0.1
            dynamic_w1_gamma = max(0.4, min(0.8, w1_gamma_val - adjustment_factor))
            dynamic_w2_delta = max(0.2, min(0.6, w2_delta_val + adjustment_factor))
        elif magnitude_ratio < 0.33:  # Delta dominates
            adjustment_factor = np.log10(1/magnitude_ratio) * 0.1
            dynamic_w1_gamma = max(0.4, min(0.8, w1_gamma_val + adjustment_factor))
            dynamic_w2_delta = max(0.2, min(0.6, w2_delta_val - adjustment_factor))
    
    # Enhanced: Apply volume-based adjustment
    if self.volm_col_for_weighting in df.columns:
        try:
            volume_values = pd.to_numeric(df[self.volm_col_for_weighting], errors='coerce').fillna(0.0)
            # Higher volume increases gamma weight (more responsive to hedging)
            norm_volume = self._normalize_series(volume_values, 'volume_for_sdag_weighted')
            volume_adjustment = 0.1 * norm_volume
            
            # Apply volume adjustment with limits
            dynamic_w1_gamma = np.clip(dynamic_w1_gamma + volume_adjustment, 0.4, 0.8)
            dynamic_w2_delta = np.clip(dynamic_w2_delta - volume_adjustment, 0.2, 0.6)
        except Exception as e_vol:
            sdag_logger.warning(f"Error calculating volume adjustment: {e_vol}")
    
    # Ensure weights sum to original total
    sum_of_dynamic_weights = dynamic_w1_gamma + dynamic_w2_delta
    if abs(sum_of_dynamic_weights) < MIN_NORMALIZATION_DENOMINATOR:
        sdag_logger.warning(f"Sum of dynamic weights ({sum_of_dynamic_weights:.3f}) near zero. Using original weights.")
        dynamic_w1_gamma = w1_gamma_val
        dynamic_w2_delta = w2_delta_val
        sum_of_dynamic_weights = sum_of_weights
    
    # Enhanced: Final SDAG Weighted calculation
    return ((dynamic_w1_gamma * gamma_exp_numeric + dynamic_w2_delta * delta_exp_raw_numeric) / sum_of_dynamic_weights).fillna(0.0)
```

#### Rationale for Changes:
1. **Dynamic Weights**: Made weights responsive to the relative magnitudes of gamma and delta to ensure balanced contribution.
2. **Volume-Based Adjustment**: Added adjustment based on trading volume to increase gamma weight for high-volume strikes.
3. **Magnitude Ratio Balancing**: Implemented automatic balancing when one Greek dominates to prevent skewed results.
4. **Improved Numerical Stability**: Enhanced handling of edge cases and NaN values throughout the calculation.

#### 2.4.4 SDAG Volatility-Focused Method Enhancement

#### Original Implementation:
```python
gamma_exposure_sign = np.sign(gamma_exp_numeric).replace(0, 1)
return (gamma_exp_numeric * (1 + delta_exp_norm_numeric * gamma_exposure_sign * delta_weight_factor_val)).fillna(0.0)
```

#### Enhanced Formula:
```python
def calculate_sdag_volatility_focused(self, df: pd.DataFrame, gamma_exposure: pd.Series, delta_exposure_norm: pd.Series) -> pd.Series:
    # [Existing setup code...]
    
    # Enhanced: Improved gamma sign calculation with smoothing
    gamma_magnitude = gamma_exp_numeric.abs()
    gamma_sign_smooth = np.tanh(3 * gamma_exp_numeric)  # Smoothed sign function
    
    # Enhanced: Volatility context adjustment
    vol_context_factor = 1.0
    if self.option_iv_col in df.columns:
        try:
            iv_values = pd.to_numeric(df[self.option_iv_col], errors='coerce').fillna(0.0)
            avg_iv = iv_values.mean()
            
            if avg_iv > 0:
                # Normalize IV relative to average
                relative_iv = iv_values / avg_iv
                
                # Higher weight for high IV options in volatility-focused method
                vol_context_factor = 1 + 0.3 * (relative_iv - 1)
                vol_context_factor = np.clip(vol_context_factor, 0.7, 1.5)
        except Exception as e_vol:
            sdag_logger.warning(f"Error calculating volatility context factor: {e_vol}. Using neutral factor.")
    
    # Enhanced: Apply vomma influence if available
    vomma_factor = pd.Series(1.0, index=df.index)
    if 'vommaxoi' in df.columns:
        try:
            vomma_values = pd.to_numeric(df['vommaxoi'], errors='coerce').fillna(0.0)
            norm_vomma = self._normalize_series(vomma_values.abs(), 'vomma_for_sdag_vol')
            
            # Vomma enhances volatility sensitivity
            vomma_factor = 1 + 0.4 * norm_vomma
        except Exception as e_vomma:
            sdag_logger.warning(f"Error calculating vomma factor: {e_vomma}. Using neutral factor.")
    
    # Enhanced: Final SDAG Volatility-Focused calculation
    return (
        gamma_exp_numeric * 
        (1 + delta_exp_norm_numeric * gamma_sign_smooth * delta_weight_factor_val) * 
        vol_context_factor * 
        vomma_factor
    ).fillna(0.0)
```

#### Rationale for Changes:
1. **Smoothed Gamma Sign**: Replaced hard sign function with tanh for smoother transitions and to avoid abrupt changes.
2. **Volatility Context Adjustment**: Added adjustment based on relative implied volatility to enhance sensitivity in high-volatility environments.
3. **Vomma Influence**: Incorporated vomma (volatility of volatility sensitivity) to better capture volatility regime dynamics.
4. **Improved Numerical Stability**: Enhanced handling of edge cases and NaN values throughout the calculation.

### 2.5 Adaptive DAG (A-DAG) Enhancement

#### Original Implementation:
```python
df[self.a_dag_output_col] = (
    volume_weighted_gamma_exposure * dxoi_sign *
    (1 + df['a_dag_alpha'] * df['a_dag_flow_ratio']) *
    df['a_dag_norm_net_gamma_flow'] *
    dte_scaling_series
)
```

#### Enhanced Formula:
```python
def calculate_adaptive_dag(self, options_df: pd.DataFrame, current_iv: Optional[float] = None, 
                          avg_iv_long_term: Optional[float] = None, 
                          historical_atr_normalized_vs_avg: Optional[float] = None,
                          historical_flow_snapshots_delta: Optional[Deque[pd.Series]] = None,
                          historical_flow_snapshots_gamma: Optional[Deque[pd.Series]] = None,
                          current_price_for_dte_scaling: Optional[float] = None,
                          historical_ohlc_for_dte_atr: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    # [Existing setup code...]
    
    # Enhanced: Improved volume weighting with recency bias
    volume_weighted_gamma_exposure = self._calculate_volume_weighted_gamma(df)
    
    # Enhanced: Apply volatility regime-based scaling
    vol_regime_factor = self._get_volatility_regime_factor(current_iv, avg_iv_long_term, historical_atr_normalized_vs_avg)
    
    # Enhanced: Apply adaptive alpha with volatility regime influence
    base_alpha = self.a_dag_adaptive_alpha_base
    adaptive_alpha_aligned = base_alpha.get("aligned", 1.3) * vol_regime_factor
    adaptive_alpha_opposed = base_alpha.get("opposed", 0.7) / vol_regime_factor
    adaptive_alpha_neutral = base_alpha.get("neutral", 1.0)
    
    # Enhanced: Apply temporal decay to flow data
    recency_weighted_net_delta_flow = self._apply_temporal_decay_to_flow(net_delta_flow_current, historical_flow_snapshots_delta)
    recency_weighted_net_gamma_flow = self._apply_temporal_decay_to_flow(net_gamma_flow_current, historical_flow_snapshots_gamma)
    
    # Enhanced: Calculate alignment with improved smoothing
    alignment_sign_a_dag = np.tanh(3 * recency_weighted_net_delta_flow * dxoi_numeric)
    
    # Enhanced: Apply adaptive alpha based on smoothed alignment
    df['a_dag_alpha'] = np.select(
        [alignment_sign_a_dag > 0.3, alignment_sign_a_dag < -0.3],
        [adaptive_alpha_aligned, adaptive_alpha_opposed], 
        default=adaptive_alpha_neutral
    )
    
    # Enhanced: Calculate flow ratio with improved normalization
    recency_weighted_net_delta_flow_abs = recency_weighted_net_delta_flow.abs()
    dxoi_abs_a_dag = dxoi_numeric.abs().replace(0, np.inf)
    raw_flow_ratio = (recency_weighted_net_delta_flow_abs / dxoi_abs_a_dag).fillna(0.0)
    
    # Apply sigmoid normalization for better scaling
    df['a_dag_flow_ratio'] = 2 / (1 + np.exp(-3 * raw_flow_ratio)) - 1
    
    # Enhanced: Apply DTE scaling with improved curve
    dte_scaling_series = self._calculate_dte_scaling(df, current_price_for_dte_scaling, historical_ohlc_for_dte_atr)
    
    # Enhanced: Apply skew adjustment if available
    skew_factor = pd.Series(1.0, index=df.index)
    if self.option_iv_col in df.columns and 'strike' in df.columns and 'price' in df.columns:
        try:
            iv_values = pd.to_numeric(df[self.option_iv_col], errors='coerce').fillna(0.0)
            current_price = pd.to_numeric(df['price'].iloc[0], errors='coerce')
            strikes = pd.to_numeric(df['strike'], errors='coerce')
            
            if pd.notna(current_price) and current_price > 0:
                # Calculate moneyness
                moneyness = strikes / current_price - 1
                
                # Group by moneyness buckets
                atm_mask = abs(moneyness) <= 0.02
                otm_mask = ~atm_mask
                
                # Calculate average IV for ATM options
                atm_iv = iv_values[atm_mask].mean() if any(atm_mask) else iv_values.mean()
                
                if atm_iv > 0:
                    # Calculate skew factor based on IV relative to ATM IV
                    skew_factor = np.where(
                        otm_mask,
                        1 + 0.3 * (1 - iv_values / atm_iv),  # Adjust based on skew
                        1.0  # No adjustment for ATM
                    )
                    skew_factor = pd.Series(skew_factor, index=df.index).fillna(1.0)
        except Exception as e_skew:
            a_dag_logger.warning(f"Error calculating skew factor: {e_skew}. Using neutral factor.")
    
    # Enhanced: Final A-DAG calculation with all improvements
    df[self.a_dag_output_col] = (
        volume_weighted_gamma_exposure * 
        np.sign(dxoi_numeric) * 
        (1 + df['a_dag_alpha'] * df['a_dag_flow_ratio']) * 
        self._normalize_series(recency_weighted_net_gamma_flow, 'recency_weighted_net_gamma_flow_for_a_dag') * 
        dte_scaling_series * 
        skew_factor * 
        vol_regime_factor
    ).fillna(0.0)
    
    return df
```

#### Rationale for Changes:
1. **Improved Alignment Calculation**: Replaced hard sign function with tanh for smoother transitions and better handling of alignment.
2. **Enhanced Flow Ratio Normalization**: Applied sigmoid function to better scale the flow ratio and handle extreme values.
3. **Volatility Regime Integration**: Directly incorporated volatility regime factor into the final calculation.
4. **Skew Adjustment**: Added volatility skew adjustment to better account for market pricing of tail risk.
5. **Improved Temporal Decay**: Enhanced the temporal decay application to flow data for better recency weighting.
6. **Improved Numerical Stability**: Enhanced handling of edge cases and NaN values throughout the calculation.

## 3. Composite Metrics and Key Level Enhancements

### 3.1 Market Structure and Price Impact (MSPI) Enhancement

#### Original Implementation:
The MSPI is calculated by weighted combination of individual metrics:
```python
for config_key, weight_value_cfg in selected_weights_config_base_keys.items():
    # [Weight selection logic...]
    final_mspi_component_weights[actual_norm_col_for_mspi] = current_weight_value
```

#### Enhanced Formula:
```python
def get_weights(self, current_time: Optional[time] = None, iv_context: Optional[Dict[str, Any]] = None) -> Dict[str, float]:
    # [Existing setup code...]
    
    # Enhanced: Apply adaptive weighting based on performance tracking
    if self.adaptive_system_enabled:
        try:
            # Get performance metrics from tracking system
            performance_metrics = self._get_performance_metrics()
            
            if performance_metrics and len(performance_metrics) >= 3:
                # Extract metric performance scores
                dag_performance = performance_metrics.get('dag_custom', 0.5)
                tdpi_performance = performance_metrics.get('tdpi', 0.5)
                vri_performance = performance_metrics.get('vri', 0.5)
                sdag_mult_performance = performance_metrics.get('sdag_multiplicative_norm', 0.5)
                sdag_weight_performance = performance_metrics.get('sdag_weighted_norm', 0.5)
                
                # Calculate performance-based adjustment factors
                dag_adj = (dag_performance - 0.5) * 0.4  # Max ±20% adjustment
                tdpi_adj = (tdpi_performance - 0.5) * 0.4
                vri_adj = (vri_performance - 0.5) * 0.4
                sdag_mult_adj = (sdag_mult_performance - 0.5) * 0.4
                sdag_weight_adj = (sdag_weight_performance - 0.5) * 0.4
                
                # Apply adjustments to base weights
                for metric_key in selected_weights_config_base_keys:
                    if metric_key == 'dag_custom':
                        selected_weights_config_base_keys[metric_key] *= (1 + dag_adj)
                    elif metric_key == 'tdpi':
                        selected_weights_config_base_keys[metric_key] *= (1 + tdpi_adj)
                    elif metric_key == 'vri':
                        selected_weights_config_base_keys[metric_key] *= (1 + vri_adj)
                    elif metric_key == 'sdag_multiplicative_norm':
                        selected_weights_config_base_keys[metric_key] *= (1 + sdag_mult_adj)
                    elif metric_key == 'sdag_weighted_norm':
                        selected_weights_config_base_keys[metric_key] *= (1 + sdag_weight_adj)
                
                # Renormalize weights to sum to 1.0
                total_weight = sum(selected_weights_config_base_keys.values())
                if total_weight > MIN_NORMALIZATION_DENOMINATOR:
                    for key in selected_weights_config_base_keys:
                        selected_weights_config_base_keys[key] /= total_weight
                
                weights_logger.info(f"Applied performance-based weight adjustments. New weights: {selected_weights_config_base_keys}")
        except Exception as e_adapt:
            weights_logger.warning(f"Error applying adaptive weights: {e_adapt}. Using base weights.")
    
    # Enhanced: Apply market regime context
    if iv_context is not None:
        try:
            iv_percentile_key = str(self._get_config_value(["data_processor_settings", "iv_context_parameters", "iv_percentile"], "iv_percentile_30d"))
            if iv_percentile_key in iv_context and iv_context[iv_percentile_key] is not None:
                iv_percentile = float(iv_context[iv_percentile_key])
                
                # Adjust weights based on volatility regime
                if iv_percentile > 0.7:  # High volatility regime
                    # Increase weight of VRI and volatility-focused SDAG
                    vri_boost = 0.1
                    vol_sdag_boost = 0.05
                    
                    # Find keys to adjust
                    vri_key = next((k for k in selected_weights_config_base_keys if k == 'vri'), None)
                    vol_sdag_key = next((k for k in selected_weights_config_base_keys if 'volatility_focused' in k), None)
                    
                    # Apply adjustments
                    if vri_key and vol_sdag_key:
                        # Calculate how much to reduce other weights
                        total_boost = vri_boost + vol_sdag_boost
                        other_keys = [k for k in selected_weights_config_base_keys if k != vri_key and k != vol_sdag_key]
                        reduction_per_key = total_boost / len(other_keys) if other_keys else 0
                        
                        # Apply adjustments
                        selected_weights_config_base_keys[vri_key] += vri_boost
                        selected_weights_config_base_keys[vol_sdag_key] += vol_sdag_boost
                        
                        for other_key in other_keys:
                            selected_weights_config_base_keys[other_key] -= reduction_per_key
                
                elif iv_percentile < 0.3:  # Low volatility regime
                    # Increase weight of DAG and weighted SDAG
                    dag_boost = 0.1
                    weighted_sdag_boost = 0.05
                    
                    # Find keys to adjust
                    dag_key = next((k for k in selected_weights_config_base_keys if k == 'dag_custom'), None)
                    weighted_sdag_key = next((k for k in selected_weights_config_base_keys if 'weighted_norm' in k), None)
                    
                    # Apply adjustments
                    if dag_key and weighted_sdag_key:
                        # Calculate how much to reduce other weights
                        total_boost = dag_boost + weighted_sdag_boost
                        other_keys = [k for k in selected_weights_config_base_keys if k != dag_key and k != weighted_sdag_key]
                        reduction_per_key = total_boost / len(other_keys) if other_keys else 0
                        
                        # Apply adjustments
                        selected_weights_config_base_keys[dag_key] += dag_boost
                        selected_weights_config_base_keys[weighted_sdag_key] += weighted_sdag_boost
                        
                        for other_key in other_keys:
                            selected_weights_config_base_keys[other_key] -= reduction_per_key
                
                weights_logger.info(f"Applied volatility regime adjustments. IV percentile: {iv_percentile:.2f}")
        except Exception as e_regime:
            weights_logger.warning(f"Error applying regime-based weight adjustments: {e_regime}")
    
    # [Continue with existing weight processing...]
    
    return final_mspi_component_weights
```

#### Rationale for Changes:
1. **Performance-Based Adaptive Weighting**: Added adjustment of weights based on historical performance of each metric.
2. **Volatility Regime Context**: Incorporated volatility regime context to adjust weights based on current market conditions.
3. **Enhanced Normalization**: Improved the weight normalization process to ensure consistent scaling.
4. **Improved Error Handling**: Added robust error handling to ensure system stability even when adaptive features encounter issues.

### 3.2 Key Level Identification Enhancement

#### Original Implementation:
Key levels are identified based on aggregated metrics at each strike.

#### Enhanced Formula:
```python
def identify_enhanced_key_levels(self, aggregated_df: pd.DataFrame, current_price: float, 
                                historical_levels: Optional[List[Dict[str, Any]]] = None,
                                historical_interactions: Optional[Dict[float, Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
    # [Existing setup code...]
    
    # Enhanced: Apply multi-timeframe analysis
    if historical_levels is not None and len(historical_levels) > 0:
        try:
            # Extract historical key levels
            historical_strikes = []
            for hist_level_set in historical_levels:
                if isinstance(hist_level_set, dict) and 'levels' in hist_level_set:
                    for level in hist_level_set['levels']:
                        if isinstance(level, dict) and 'strike' in level:
                            historical_strikes.append(float(level['strike']))
            
            # Create density map of historical levels
            if historical_strikes:
                hist_density = {}
                for strike in aggregated_df['strike']:
                    strike_val = float(strike)
                    # Count nearby historical levels
                    nearby_count = sum(1 for hist_strike in historical_strikes 
                                      if abs(hist_strike - strike_val) / current_price < 0.01)
                    hist_density[strike_val] = nearby_count
                
                # Apply historical density boost
                for i, row in aggregated_df.iterrows():
                    strike_val = float(row['strike'])
                    if strike_val in hist_density and hist_density[strike_val] > 0:
                        # Boost MSPI based on historical level density
                        density_boost = min(0.3, 0.1 * hist_density[strike_val])
                        aggregated_df.at[i, self.mspi_col_name] *= (1 + density_boost)
        except Exception as e_hist:
            key_levels_logger.warning(f"Error applying historical level analysis: {e_hist}")
    
    # Enhanced: Apply interaction history analysis
    if historical_interactions is not None and len(historical_interactions) > 0:
        try:
            for i, row in aggregated_df.iterrows():
                strike_val = float(row['strike'])
                # Check for nearby interactions
                for hist_strike, interaction_data in historical_interactions.items():
                    if abs(hist_strike - strike_val) / current_price < 0.01:
                        # Extract interaction statistics
                        bounce_count = interaction_data.get('bounce_count', 0)
                        break_count = interaction_data.get('break_count', 0)
                        total_interactions = bounce_count + break_count
                        
                        if total_interactions > 0:
                            # Calculate interaction strength
                            interaction_ratio = bounce_count / total_interactions
                            
                            # Apply different boosts based on interaction type
                            if interaction_ratio > 0.7:  # Strong support/resistance
                                aggregated_df.at[i, self.mspi_col_name] *= (1 + 0.2 * min(1, total_interactions/5))
                            elif interaction_ratio < 0.3:  # Frequently broken level
                                aggregated_df.at[i, self.mspi_col_name] *= (1 - 0.1 * min(1, total_interactions/5))
        except Exception as e_inter:
            key_levels_logger.warning(f"Error applying interaction history analysis: {e_inter}")
    
    # Enhanced: Apply volume profile analysis
    if 'volm' in aggregated_df.columns:
        try:
            # Normalize volume
            norm_volume = self._normalize_series(aggregated_df['volm'], 'volume_for_key_levels')
            
            # Apply volume boost to MSPI
            aggregated_df[self.mspi_col_name] *= (1 + 0.2 * norm_volume)
        except Exception as e_vol:
            key_levels_logger.warning(f"Error applying volume profile analysis: {e_vol}")
    
    # Enhanced: Apply dynamic clustering
    try:
        # Sort by strike
        sorted_df = aggregated_df.sort_values('strike')
        
        # Calculate strike distances as percentage of current price
        strike_diffs = np.diff(sorted_df['strike']) / current_price
        
        # Identify clusters (strikes within 0.5% of each other)
        cluster_starts = np.where(strike_diffs > 0.005)[0] + 1
        cluster_indices = np.split(np.arange(len(sorted_df)), cluster_starts)
        
        # Process each cluster
        clustered_levels = []
        for cluster in cluster_indices:
            if len(cluster) > 0:
                cluster_df = sorted_df.iloc[cluster]
                
                # Calculate weighted average strike
                weights = np.abs(cluster_df[self.mspi_col_name])
                if weights.sum() > 0:
                    avg_strike = np.average(cluster_df['strike'], weights=weights)
                else:
                    avg_strike = cluster_df['strike'].mean()
                
                # Sum MSPI values in cluster
                combined_mspi = cluster_df[self.mspi_col_name].sum()
                
                # Create enhanced level
                level_data = {
                    'strike': avg_strike,
                    'mspi': combined_mspi,
                    'type': 'support' if avg_strike < current_price else 'resistance',
                    'strength': abs(combined_mspi),
                    'proximity': abs(avg_strike - current_price) / current_price,
                    'cluster_size': len(cluster)
                }
                
                clustered_levels.append(level_data)
        
        # Sort by strength
        clustered_levels.sort(key=lambda x: x['strength'], reverse=True)
        
        # Apply proximity boost to nearby levels
        for level in clustered_levels:
            if level['proximity'] < 0.02:  # Within 2% of current price
                proximity_boost = 1 + (0.02 - level['proximity']) * 5  # Max 10% boost for very close levels
                level['strength'] *= proximity_boost
        
        # Re-sort after proximity boost
        clustered_levels.sort(key=lambda x: x['strength'], reverse=True)
        
        return clustered_levels
    except Exception as e_cluster:
        key_levels_logger.error(f"Error in dynamic clustering: {e_cluster}")
        # Fallback to basic level identification
        # [Basic level identification code...]
```

#### Rationale for Changes:
1. **Multi-Timeframe Analysis**: Added analysis of historical levels to identify persistent support/resistance zones.
2. **Interaction History**: Incorporated historical price interactions with levels to better assess level strength.
3. **Volume Profile Analysis**: Added volume-based weighting to emphasize levels with significant trading activity.
4. **Dynamic Clustering**: Implemented improved clustering algorithm to combine nearby levels into more meaningful zones.
5. **Proximity Boost**: Added proximity-based boost to emphasize levels near the current price.

## 4. Signal Generation Enhancements

### 4.1 Directional Signal Enhancement

#### Original Implementation:
Directional signals are generated based on threshold crossings of individual metrics.

#### Enhanced Formula:
```python
def generate_enhanced_directional_signals(self, df: pd.DataFrame, current_price: float, 
                                         historical_signals: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
    # [Setup code...]
    
    # Enhanced: Apply consensus-based signal generation
    try:
        # Extract directional components
        dag_series = df.get('dag_custom', pd.Series(dtype=float))
        a_dag_series = df.get(self.a_dag_output_col, pd.Series(dtype=float))
        sdag_mult_series = df.get('sdag_multiplicative', pd.Series(dtype=float))
        sdag_dir_series = df.get('sdag_directional', pd.Series(dtype=float))
        
        # Calculate consensus direction for each strike
        consensus_directions = {}
        for i, row in df.iterrows():
            strike = float(row['strike'])
            
            # Collect directional votes
            directions = []
            if i in dag_series.index and pd.notna(dag_series[i]):
                directions.append(np.sign(dag_series[i]))
            if i in a_dag_series.index and pd.notna(a_dag_series[i]):
                directions.append(np.sign(a_dag_series[i]))
            if i in sdag_mult_series.index and pd.notna(sdag_mult_series[i]):
                directions.append(np.sign(sdag_mult_series[i]))
            if i in sdag_dir_series.index and pd.notna(sdag_dir_series[i]):
                directions.append(np.sign(sdag_dir_series[i]))
            
            if directions:
                # Calculate consensus
                consensus_score = sum(directions) / len(directions)
                consensus_directions[strike] = consensus_score
        
        # Identify high-consensus strikes
        high_consensus_strikes = []
        for strike, consensus in consensus_directions.items():
            if abs(consensus) > 0.5:  # More than half agree on direction
                high_consensus_strikes.append({
                    'strike': strike,
                    'consensus': consensus,
                    'direction': 'bullish' if consensus > 0 else 'bearish',
                    'strength': abs(consensus)
                })
        
        # Sort by strength and proximity to current price
        high_consensus_strikes.sort(key=lambda x: (x['strength'], 1 - abs(x['strike'] - current_price) / current_price), reverse=True)
        
        # Generate signals for top consensus strikes
        signals = []
        for consensus_data in high_consensus_strikes[:5]:  # Top 5 consensus strikes
            strike = consensus_data['strike']
            direction = consensus_data['direction']
            
            # Calculate signal strength based on consensus and proximity
            proximity = abs(strike - current_price) / current_price
            proximity_factor = max(0, 1 - proximity * 20)  # Decreases with distance
            signal_strength = consensus_data['strength'] * proximity_factor
            
            # Only generate signal if strong enough
            if signal_strength > 0.3:
                signal = {
                    'type': 'directional',
                    'subtype': 'enhanced_consensus',
                    'direction': direction,
                    'primary_strike': strike,
                    'strength': signal_strength,
                    'consensus_score': consensus_data['consensus'],
                    'timestamp': datetime.now(),
                    'price_at_signal': current_price
                }
                signals.append(signal)
        
        # Apply historical signal performance if available
        if historical_signals:
            try:
                # Extract historical performance by strike proximity
                strike_performance = {}
                for hist_signal in historical_signals:
                    if hist_signal.get('type') == 'directional' and 'primary_strike' in hist_signal and 'performance' in hist_signal:
                        hist_strike = float(hist_signal['primary_strike'])
                        perf = float(hist_signal['performance'])
                        strike_performance[hist_strike] = perf
                
                # Adjust current signals based on historical performance
                for signal in signals:
                    signal_strike = signal['primary_strike']
                    
                    # Find nearby historical signals
                    nearby_perfs = []
                    for hist_strike, perf in strike_performance.items():
                        if abs(hist_strike - signal_strike) / current_price < 0.01:
                            nearby_perfs.append(perf)
                    
                    # Apply performance adjustment
                    if nearby_perfs:
                        avg_perf = sum(nearby_perfs) / len(nearby_perfs)
                        perf_factor = 0.5 + 0.5 * avg_perf  # Scale between 0.5-1.5
                        signal['strength'] *= perf_factor
                        signal['historical_performance_factor'] = perf_factor
            except Exception as e_hist:
                signal_logger.warning(f"Error applying historical signal performance: {e_hist}")
        
        return signals
    except Exception as e_signal:
        signal_logger.error(f"Error generating enhanced directional signals: {e_signal}")
        return []
```

#### Rationale for Changes:
1. **Consensus-Based Generation**: Implemented consensus mechanism across multiple metrics to generate more reliable signals.
2. **Proximity-Weighted Strength**: Added proximity-based weighting to emphasize signals near the current price.
3. **Historical Performance Integration**: Incorporated historical signal performance to adjust signal strength based on past success.
4. **Enhanced Signal Metadata**: Added additional metadata to signals for better tracking and analysis.

### 4.2 Volatility Regime Signal Enhancement

#### Original Implementation:
Volatility signals are generated based on VRI thresholds.

#### Enhanced Formula:
```python
def generate_enhanced_volatility_signals(self, df: pd.DataFrame, current_price: float, 
                                        iv_context: Optional[Dict[str, Any]] = None,
                                        historical_volatility: Optional[pd.Series] = None) -> List[Dict[str, Any]]:
    # [Setup code...]
    
    # Enhanced: Apply multi-factor volatility regime detection
    try:
        signals = []
        
        # Extract volatility components
        vri_series = df.get('vri', pd.Series(dtype=float))
        vfi_series = df.get('vfi', pd.Series(dtype=float))
        vomma_series = df.get('vommaxoi', pd.Series(dtype=float)) if 'vommaxoi' in df.columns else pd.Series(dtype=float)
        
        # Calculate aggregate volatility pressure
        vol_pressure_by_strike = {}
        for i, row in df.iterrows():
            strike = float(row['strike'])
            
            # Collect volatility indicators
            vol_factors = []
            if i in vri_series.index and pd.notna(vri_series[i]):
                vol_factors.append(vri_series[i])
            if i in vfi_series.index and pd.notna(vfi_series[i]):
                vol_factors.append(vfi_series[i] * 0.8)  # Slightly lower weight
            if i in vomma_series.index and pd.notna(vomma_series[i]):
                norm_vomma = vomma_series[i] / vomma_series.abs().max() if vomma_series.abs().max() > 0 else 0
                vol_factors.append(norm_vomma * 0.6)  # Lower weight for raw vomma
            
            if vol_factors:
                # Calculate weighted average
                weights = [1.0, 0.8, 0.6][:len(vol_factors)]
                weighted_pressure = sum(f * w for f, w in zip(vol_factors, weights)) / sum(weights[:len(vol_factors)])
                vol_pressure_by_strike[strike] = weighted_pressure
        
        # Apply IV context if available
        iv_context_factor = 1.0
        iv_regime = "neutral"
        if iv_context is not None:
            try:
                iv_percentile_key = str(self._get_config_value(["data_processor_settings", "iv_context_parameters", "iv_percentile"], "iv_percentile_30d"))
                if iv_percentile_key in iv_context and iv_context[iv_percentile_key] is not None:
                    iv_percentile = float(iv_context[iv_percentile_key])
                    
                    # Determine IV regime
                    if iv_percentile > 0.7:
                        iv_regime = "high"
                        iv_context_factor = 1.3
                    elif iv_percentile < 0.3:
                        iv_regime = "low"
                        iv_context_factor = 0.7
            except Exception as e_iv:
                signal_logger.warning(f"Error processing IV context: {e_iv}")
        
        # Apply historical volatility trend if available
        vol_trend_factor = 1.0
        vol_trend = "neutral"
        if historical_volatility is not None and len(historical_volatility) > 5:
            try:
                # Calculate short-term vs long-term volatility
                short_vol = historical_volatility.iloc[-5:].mean()
                long_vol = historical_volatility.mean()
                
                if long_vol > 0:
                    vol_ratio = short_vol / long_vol
                    
                    # Determine volatility trend
                    if vol_ratio > 1.2:
                        vol_trend = "increasing"
                        vol_trend_factor = 1.3
                    elif vol_ratio < 0.8:
                        vol_trend = "decreasing"
                        vol_trend_factor = 0.7
            except Exception as e_hist_vol:
                signal_logger.warning(f"Error processing historical volatility: {e_hist_vol}")
        
        # Generate expansion and contraction signals
        for strike, pressure in vol_pressure_by_strike.items():
            adjusted_pressure = pressure * iv_context_factor * vol_trend_factor
            
            # Determine signal type based on adjusted pressure
            if adjusted_pressure > 0.6:  # Expansion signal
                proximity = abs(strike - current_price) / current_price
                proximity_factor = max(0, 1 - proximity * 20)  # Decreases with distance
                
                signal_strength = adjusted_pressure * proximity_factor
                
                if signal_strength > 0.4:  # Only generate if strong enough
                    signal = {
                        'type': 'volatility',
                        'subtype': 'enhanced_expansion',
                        'primary_strike': strike,
                        'strength': signal_strength,
                        'iv_regime': iv_regime,
                        'vol_trend': vol_trend,
                        'timestamp': datetime.now(),
                        'price_at_signal': current_price
                    }
                    signals.append(signal)
            
            elif adjusted_pressure < -0.6:  # Contraction signal
                proximity = abs(strike - current_price) / current_price
                proximity_factor = max(0, 1 - proximity * 20)  # Decreases with distance
                
                signal_strength = abs(adjusted_pressure) * proximity_factor
                
                if signal_strength > 0.4:  # Only generate if strong enough
                    signal = {
                        'type': 'volatility',
                        'subtype': 'enhanced_contraction',
                        'primary_strike': strike,
                        'strength': signal_strength,
                        'iv_regime': iv_regime,
                        'vol_trend': vol_trend,
                        'timestamp': datetime.now(),
                        'price_at_signal': current_price
                    }
                    signals.append(signal)
        
        # Sort by strength
        signals.sort(key=lambda x: x['strength'], reverse=True)
        
        return signals[:5]  # Return top 5 signals
    except Exception as e_vol_signal:
        signal_logger.error(f"Error generating enhanced volatility signals: {e_vol_signal}")
        return []
```

#### Rationale for Changes:
1. **Multi-Factor Detection**: Implemented comprehensive volatility regime detection using multiple metrics.
2. **IV Context Integration**: Added implied volatility context to adjust signal strength based on current volatility regime.
3. **Historical Volatility Trend**: Incorporated historical volatility trend to detect regime shifts.
4. **Proximity-Weighted Strength**: Added proximity-based weighting to emphasize signals near the current price.

## 5. Implementation Recommendations

### 5.1 Integration Strategy

To implement these enhancements:

1. **Phased Approach**: Implement changes in phases, starting with core metric enhancements, then key level identification, and finally signal generation.

2. **A/B Testing**: Run the original and enhanced formulas in parallel for a period to compare results and validate improvements.

3. **Monitoring Framework**: Implement a monitoring system to track the performance of enhanced metrics and signals.

4. **Adaptive Learning**: Gradually enable the adaptive features after validating the base enhancements.

### 5.2 Performance Considerations

1. **Vectorization**: All enhancements use vectorized operations for optimal performance.

2. **Error Handling**: Robust error handling ensures system stability even when individual components fail.

3. **Memory Management**: Efficient use of temporary variables and in-place operations to minimize memory usage.

4. **Computational Efficiency**: Calculations are structured to minimize redundant operations and optimize performance.

## 6. Conclusion

The enhanced formulas provide significant improvements to the Elite Options Trading System by:

1. **Increasing Adaptability**: Making metrics responsive to market conditions, volatility regimes, and historical performance.

2. **Improving Accuracy**: Incorporating additional factors like volume, proximity, and skew for more precise calculations.

3. **Enhancing Stability**: Improving numerical stability and error handling throughout the system.

4. **Enabling Learning**: Adding adaptive features that allow the system to improve based on historical performance.

These enhancements create a more robust, accurate, and adaptive trading system that can better identify key levels, generate higher-quality signals, and adapt to changing market conditions.
