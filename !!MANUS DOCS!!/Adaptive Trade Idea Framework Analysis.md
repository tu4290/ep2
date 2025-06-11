# Adaptive Trade Idea Framework Analysis

## Overview

This document provides a comprehensive analysis of the Adaptive Trade Idea Framework designed to enhance the Elite Options Trading System. This framework transforms signal generation and trade recommendation into a dynamic, performance-based system optimized for day trading SPY/SPX options.

## Current Trade Idea Framework Limitations

The current Elite Options Trading System trade idea framework has several limitations:

1. **Static Conviction Mapping**: Fixed thresholds for mapping signals to conviction levels
2. **Generic Strategy Recommendations**: Limited specificity in option strategy selection
3. **Independent Signal Processing**: Signals are processed independently without integration
4. **Fixed Exit Parameters**: Static profit targets and stop losses regardless of market conditions
5. **Limited Performance Tracking**: Minimal learning from historical recommendation performance

## Enhanced Adaptive Trade Idea Framework

The enhanced framework addresses these limitations through four key components:

### 1. Performance-Based Conviction Mapping

**Core Enhancement Concept:**
Implement performance-based conviction mapping that adjusts based on historical signal success rates.

**Detailed Implementation:**
```python
def calculate_performance_based_conviction(self, signals, historical_performance):
    """
    Calculate performance-based conviction scores for signals.
    """
    # 1. Calculate signal success rates
    success_rates = self._calculate_signal_success_rates(historical_performance)
    
    # Track historical performance of each signal type
    signal_types = ['directional', 'volatility', 'time_decay', 'complex']
    success_rates = {}
    
    for signal_type in signal_types:
        # Get historical signals of this type
        historical_signals = historical_performance.get(signal_type, [])
        
        # Count successful signals
        successful_signals = sum(1 for signal in historical_signals if signal['successful'])
        total_signals = len(historical_signals) if historical_signals else 1  # Avoid division by zero
        
        # Calculate success rate
        success_rate = successful_signals / total_signals
        
        # Apply minimum success rate to avoid zeroing out signals
        success_rate = max(0.3, success_rate)
        
        success_rates[signal_type] = success_rate
    
    # 2. Apply performance-based weights
    weighted_signals = self._apply_performance_weights(signals, success_rates)
    
    # Weight each signal by its type's success rate
    weighted_signals = {}
    
    for signal_name, signal_value in signals.items():
        # Determine signal type
        signal_type = self._determine_signal_type(signal_name)
        
        # Apply weight based on success rate
        weight = success_rates.get(signal_type, 0.5)  # Default to 0.5 if type unknown
        weighted_signals[signal_name] = signal_value * weight
    
    # 3. Calculate adaptive conviction thresholds
    adaptive_thresholds = self._calculate_adaptive_conviction_thresholds(historical_performance)
    
    # Adjust thresholds based on historical performance
    base_thresholds = {
        'low': 1.0,
        'medium': 2.0,
        'high': 3.0
    }
    
    # Calculate performance adjustment factor
    overall_success_rate = sum(success_rates.values()) / len(success_rates)
    performance_adjustment_factor = 1 / (0.5 + overall_success_rate)  # Higher success rate = lower thresholds
    
    adaptive_thresholds = {
        level: threshold * performance_adjustment_factor 
        for level, threshold in base_thresholds.items()
    }
    
    # 4. Generate conviction-mapped signals
    conviction_mapped_signals = self._generate_conviction_mapped_signals(
        weighted_signals,
        adaptive_thresholds
    )
    
    # Map signals to conviction levels based on adaptive thresholds
    conviction_mapped_signals = {}
    
    for signal_name, weighted_value in weighted_signals.items():
        abs_value = abs(weighted_value)
        direction = 1 if weighted_value > 0 else -1
        
        # Determine conviction level
        if abs_value >= adaptive_thresholds['high']:
            conviction = 'high'
        elif abs_value >= adaptive_thresholds['medium']:
            conviction = 'medium'
        elif abs_value >= adaptive_thresholds['low']:
            conviction = 'low'
        else:
            conviction = 'none'
        
        conviction_mapped_signals[signal_name] = {
            'value': weighted_value,
            'direction': direction,
            'conviction': conviction
        }
    
    return {
        "conviction_mapped_signals": conviction_mapped_signals,
        "success_rates": success_rates,
        "weighted_signals": weighted_signals,
        "adaptive_thresholds": adaptive_thresholds
    }
```

**Key Improvements:**
- **Signal Success Rate Tracking**: Tracks historical performance of each signal type
- **Performance-Based Weighting**: Adjusts signal weights based on historical success
- **Adaptive Conviction Thresholds**: Dynamically adjusts thresholds based on performance
- **Enhanced Conviction Mapping**: Maps signals to conviction levels based on performance

**Market Impact:**
This component significantly improves signal quality by emphasizing signals with proven predictive power and adjusting conviction thresholds based on overall system performance. This leads to higher-quality trade recommendations with more appropriate sizing based on actual historical performance.

### 2. Enhanced Strategy Specificity

**Core Enhancement Concept:**
Provide more specific option strategy recommendations based on signals, market conditions, and SPY/SPX characteristics.

**Detailed Implementation:**
```python
def generate_enhanced_strategy_recommendations(self, signals, market_conditions, current_price, volatility_data):
    """
    Generate enhanced strategy recommendations with specific option parameters.
    """
    # 1. Determine optimal strategy types
    strategy_types = self._determine_optimal_strategy_types(signals, market_conditions)
    
    # Map signals to strategy types
    directional_strength = self._calculate_directional_strength(signals)
    volatility_expectation = self._calculate_volatility_expectation(signals)
    time_decay_opportunity = self._calculate_time_decay_opportunity(signals)
    
    # Determine primary strategy type based on strongest signal
    if abs(directional_strength) > max(volatility_expectation, time_decay_opportunity):
        primary_type = 'directional'
        primary_direction = 'bullish' if directional_strength > 0 else 'bearish'
    elif volatility_expectation > time_decay_opportunity:
        primary_type = 'volatility'
        primary_direction = 'expansion' if volatility_expectation > 0 else 'contraction'
    else:
        primary_type = 'time_decay'
        primary_direction = 'neutral'
    
    strategy_types = {
        'primary_type': primary_type,
        'primary_direction': primary_direction,
        'directional_strength': directional_strength,
        'volatility_expectation': volatility_expectation,
        'time_decay_opportunity': time_decay_opportunity
    }
    
    # 2. Select specific option strategies
    specific_strategies = self._select_specific_option_strategies(strategy_types, volatility_data)
    
    # Select strategies based on type and market conditions
    iv_percentile = volatility_data['iv_percentile']
    dte_preference = self._calculate_dte_preference(signals)
    
    specific_strategies = []
    
    if strategy_types['primary_type'] == 'directional':
        if strategy_types['primary_direction'] == 'bullish':
            if iv_percentile > 70:  # High IV environment
                specific_strategies.append({
                    'name': 'Bull Call Spread',
                    'description': 'Buy ATM call, sell OTM call',
                    'risk_profile': 'Defined risk, defined reward',
                    'iv_sensitivity': 'Negative (benefits from IV contraction)'
                })
            else:  # Low/moderate IV environment
                specific_strategies.append({
                    'name': 'Long Call',
                    'description': 'Buy ATM/slightly OTM call',
                    'risk_profile': 'Defined risk, unlimited reward',
                    'iv_sensitivity': 'Positive (benefits from IV expansion)'
                })
        else:  # Bearish
            if iv_percentile > 70:  # High IV environment
                specific_strategies.append({
                    'name': 'Bear Put Spread',
                    'description': 'Buy ATM put, sell OTM put',
                    'risk_profile': 'Defined risk, defined reward',
                    'iv_sensitivity': 'Negative (benefits from IV contraction)'
                })
            else:  # Low/moderate IV environment
                specific_strategies.append({
                    'name': 'Long Put',
                    'description': 'Buy ATM/slightly OTM put',
                    'risk_profile': 'Defined risk, unlimited reward',
                    'iv_sensitivity': 'Positive (benefits from IV expansion)'
                })
    
    elif strategy_types['primary_type'] == 'volatility':
        if strategy_types['primary_direction'] == 'expansion':
            specific_strategies.append({
                'name': 'Long Straddle',
                'description': 'Buy ATM call and put',
                'risk_profile': 'Defined risk, unlimited reward',
                'iv_sensitivity': 'Positive (benefits from IV expansion)'
            })
        else:  # Contraction
            if iv_percentile > 60:  # Only sell volatility when IV is elevated
                specific_strategies.append({
                    'name': 'Iron Condor',
                    'description': 'Sell OTM put spread and call spread',
                    'risk_profile': 'Defined risk, defined reward',
                    'iv_sensitivity': 'Negative (benefits from IV contraction)'
                })
    
    elif strategy_types['primary_type'] == 'time_decay':
        if iv_percentile > 60:  # Only sell premium when IV is elevated
            specific_strategies.append({
                'name': 'Short Put Spread',
                'description': 'Sell OTM put, buy further OTM put',
                'risk_profile': 'Defined risk, defined reward',
                'iv_sensitivity': 'Negative (benefits from IV contraction)'
            })
        else:
            specific_strategies.append({
                'name': 'Butterfly Spread',
                'description': 'Buy ATM call, sell 2 OTM calls, buy further OTM call',
                'risk_profile': 'Defined risk, defined reward',
                'iv_sensitivity': 'Neutral'
            })
    
    # 3. Determine optimal strikes and expirations
    strike_expiration_recommendations = self._determine_optimal_strikes_expirations(
        specific_strategies,
        current_price,
        volatility_data,
        signals
    )
    
    # Calculate optimal parameters for each strategy
    strike_expiration_recommendations = []
    
    for strategy in specific_strategies:
        if strategy['name'] == 'Long Call':
            # Determine optimal delta based on conviction
            if directional_strength > 2:
                target_delta = 0.60  # Higher conviction = higher delta
            else:
                target_delta = 0.45  # Lower conviction = lower delta
            
            # Determine optimal DTE based on signals
            if time_decay_opportunity < -1:  # Strong negative time decay signal
                target_dte = 2  # Very short-term
            elif volatility_expectation > 1:  # Strong volatility expansion expected
                target_dte = 7  # Give more time for volatility expansion
            else:
                target_dte = 4  # Default for day trading
            
            strike_expiration_recommendations.append({
                'strategy': strategy['name'],
                'target_delta': target_delta,
                'target_dte': target_dte,
                'strike_calculation': f"Find strike with ~{target_delta} delta",
                'expiration_calculation': f"Find expiration ~{target_dte} days out"
            })
        
        # Similar calculations for other strategy types...
    
    # 4. Calculate risk-reward parameters
    risk_reward_parameters = self._calculate_risk_reward_parameters(
        specific_strategies,
        strike_expiration_recommendations,
        volatility_data
    )
    
    # Calculate risk parameters for each strategy
    risk_reward_parameters = []
    
    for strategy, params in zip(specific_strategies, strike_expiration_recommendations):
        # Calculate based on strategy type
        if strategy['name'] == 'Long Call':
            max_risk = 100  # Example: $100 per contract
            target_reward = max_risk * 2  # 2:1 reward-to-risk ratio
            stop_loss_pct = 40  # Exit at 40% loss
            profit_target_pct = 80  # Exit at 80% gain
            
            # Adjust based on signals
            if directional_strength > 2:
                stop_loss_pct = 50  # Allow more room with higher conviction
                profit_target_pct = 100  # Aim for higher profit with higher conviction
            
            risk_reward_parameters.append({
                'strategy': strategy['name'],
                'max_risk_per_contract': max_risk,
                'target_reward_per_contract': target_reward,
                'stop_loss_percentage': stop_loss_pct,
                'profit_target_percentage': profit_target_pct,
                'reward_to_risk_ratio': target_reward / max_risk
            })
        
        # Similar calculations for other strategy types...
    
    # 5. Generate enhanced strategy recommendations
    enhanced_recommendations = self._generate_enhanced_recommendations(
        specific_strategies,
        strike_expiration_recommendations,
        risk_reward_parameters,
        signals
    )
    
    # Combine all information into final recommendations
    enhanced_recommendations = []
    
    for strategy, strike_exp, risk_reward in zip(specific_strategies, strike_expiration_recommendations, risk_reward_parameters):
        recommendation = {
            'strategy_name': strategy['name'],
            'strategy_description': strategy['description'],
            'direction': strategy_types['primary_direction'],
            'conviction': self._map_strength_to_conviction(directional_strength if strategy_types['primary_type'] == 'directional' else volatility_expectation),
            'target_delta': strike_exp.get('target_delta'),
            'target_dte': strike_exp.get('target_dte'),
            'max_risk_per_contract': risk_reward.get('max_risk_per_contract'),
            'target_reward_per_contract': risk_reward.get('target_reward_per_contract'),
            'stop_loss_percentage': risk_reward.get('stop_loss_percentage'),
            'profit_target_percentage': risk_reward.get('profit_target_percentage'),
            'reward_to_risk_ratio': risk_reward.get('reward_to_risk_ratio'),
            'key_levels': self._identify_relevant_key_levels(signals, current_price, strategy_types['primary_direction']),
            'time_window': self._determine_optimal_time_window(signals, market_conditions),
            'implementation_notes': self._generate_implementation_notes(strategy, signals, market_conditions)
        }
        
        enhanced_recommendations.append(recommendation)
    
    return {
        "enhanced_recommendations": enhanced_recommendations,
        "strategy_types": strategy_types,
        "specific_strategies": specific_strategies,
        "strike_expiration_recommendations": strike_expiration_recommendations,
        "risk_reward_parameters": risk_reward_parameters
    }
```

**Key Improvements:**
- **Optimal Strategy Type Selection**: Determines best strategy category based on signals
- **Specific Option Strategy Selection**: Recommends specific option strategies
- **Strike and Expiration Optimization**: Determines optimal strikes and expirations
- **Risk-Reward Parameter Calculation**: Calculates detailed risk-reward parameters

**Market Impact:**
This component provides significantly more actionable trade recommendations with specific option parameters tailored to current market conditions. Traders receive clear guidance on strategy selection, strike and expiration choice, and risk management parameters, leading to more effective trade execution.

### 3. Dynamic Signal Integration

**Core Enhancement Concept:**
Implement dynamic signal integration with performance-based weighting, enhanced time-based profiles, and market regime adaptation.

**Detailed Implementation:**
```python
def integrate_signals_dynamically(self, all_signals, historical_performance, current_time, market_regime):
    """
    Integrate signals dynamically with performance-based weighting and regime adaptation.
    """
    # 1. Calculate performance-based signal weights
    performance_weights = self._calculate_performance_weights(all_signals, historical_performance)
    
    # Calculate weights based on historical success rates
    signal_types = ['directional', 'volatility', 'time_decay', 'complex']
    performance_weights = {}
    
    for signal_type in signal_types:
        # Get historical signals of this type
        historical_signals = historical_performance.get(signal_type, [])
        
        # Count successful signals
        successful_signals = sum(1 for signal in historical_signals if signal['successful'])
        total_signals = len(historical_signals) if historical_signals else 1  # Avoid division by zero
        
        # Calculate success rate
        success_rate = successful_signals / total_signals
        
        # Apply minimum weight to avoid zeroing out signals
        weight = max(0.3, success_rate)
        
        # Apply recency bias (more weight to recent performance)
        recent_signals = [s for s in historical_signals if s['age_days'] < 5]
        if recent_signals:
            recent_success_rate = sum(1 for s in recent_signals if s['successful']) / len(recent_signals)
            weight = 0.7 * weight + 0.3 * recent_success_rate
        
        performance_weights[signal_type] = weight
    
    # 2. Apply enhanced time-based profiles
    time_adjusted_signals = self._apply_enhanced_time_profiles(all_signals, current_time)
    
    # Adjust signals based on time of day
    hour = current_time.hour + current_time.minute / 60
    
    # Define time profiles
    if 9.5 <= hour < 10.5:  # Opening hour
        time_profile = {
            'directional': 1.2,  # Emphasize directional signals during volatile open
            'volatility': 1.3,   # Emphasize volatility signals during volatile open
            'time_decay': 0.7,   # De-emphasize time decay during volatile open
            'complex': 0.9       # Slightly de-emphasize complex signals during open
        }
    elif 11.5 <= hour < 13.5:  # Midday
        time_profile = {
            'directional': 0.8,  # De-emphasize directional during midday lull
            'volatility': 0.7,   # De-emphasize volatility during midday lull
            'time_decay': 1.3,   # Emphasize time decay during midday lull
            'complex': 1.0       # Neutral on complex signals during midday
        }
    elif 15 <= hour < 16:  # Closing hour
        time_profile = {
            'directional': 1.1,  # Emphasize directional during close
            'volatility': 0.9,   # Slightly de-emphasize volatility during close
            'time_decay': 1.2,   # Emphasize time decay during close (for next-day positioning)
            'complex': 1.1       # Emphasize complex signals during close
        }
    else:  # Default
        time_profile = {
            'directional': 1.0,
            'volatility': 1.0,
            'time_decay': 1.0,
            'complex': 1.0
        }
    
    # Apply time profile to signals
    time_adjusted_signals = {}
    for signal_name, signal_value in all_signals.items():
        signal_type = self._determine_signal_type(signal_name)
        time_factor = time_profile.get(signal_type, 1.0)
        time_adjusted_signals[signal_name] = signal_value * time_factor
    
    # 3. Adapt signals to market regime
    regime_adapted_signals = self._adapt_signals_to_regime(time_adjusted_signals, market_regime)
    
    # Define regime adaptation factors
    regime_adaptation = {
        'bullish_trend': {
            'directional_bullish': 1.2,
            'directional_bearish': 0.7,
            'volatility_expansion': 0.9,
            'volatility_contraction': 1.1,
            'time_decay_positive': 1.1,
            'time_decay_negative': 0.9
        },
        'bearish_trend': {
            'directional_bullish': 0.7,
            'directional_bearish': 1.2,
            'volatility_expansion': 1.1,
            'volatility_contraction': 0.9,
            'time_decay_positive': 0.9,
            'time_decay_negative': 1.1
        },
        'high_volatility': {
            'directional_bullish': 0.9,
            'directional_bearish': 0.9,
            'volatility_expansion': 1.3,
            'volatility_contraction': 0.7,
            'time_decay_positive': 0.8,
            'time_decay_negative': 1.2
        },
        'low_volatility': {
            'directional_bullish': 1.1,
            'directional_bearish': 1.1,
            'volatility_expansion': 0.8,
            'volatility_contraction': 1.2,
            'time_decay_positive': 1.2,
            'time_decay_negative': 0.8
        },
        'neutral': {
            'directional_bullish': 1.0,
            'directional_bearish': 1.0,
            'volatility_expansion': 1.0,
            'volatility_contraction': 1.0,
            'time_decay_positive': 1.0,
            'time_decay_negative': 1.0
        }
    }
    
    # Get adaptation factors for current regime
    current_adaptation = regime_adaptation.get(market_regime, regime_adaptation['neutral'])
    
    # Apply regime adaptation to signals
    regime_adapted_signals = {}
    for signal_name, signal_value in time_adjusted_signals.items():
        signal_type = self._determine_signal_type(signal_name)
        signal_direction = 'positive' if signal_value > 0 else 'negative'
        
        # Determine adaptation key
        if signal_type == 'directional':
            adaptation_key = f"{signal_type}_bullish" if signal_value > 0 else f"{signal_type}_bearish"
        else:
            adaptation_key = f"{signal_type}_{signal_direction}"
        
        # Apply adaptation factor
        adaptation_factor = current_adaptation.get(adaptation_key, 1.0)
        regime_adapted_signals[signal_name] = signal_value * adaptation_factor
    
    # 4. Resolve signal conflicts
    resolved_signals = self._resolve_signal_conflicts(regime_adapted_signals, performance_weights)
    
    # Identify conflicting signals
    directional_signals = {k: v for k, v in regime_adapted_signals.items() if self._determine_signal_type(k) == 'directional'}
    volatility_signals = {k: v for k, v in regime_adapted_signals.items() if self._determine_signal_type(k) == 'volatility'}
    time_decay_signals = {k: v for k, v in regime_adapted_signals.items() if self._determine_signal_type(k) == 'time_decay'}
    
    # Resolve conflicts within each category using weighted voting
    resolved_signals = {}
    
    # Resolve directional conflicts
    if directional_signals:
        weighted_sum = sum(v * performance_weights.get(self._determine_signal_type(k), 1.0) for k, v in directional_signals.items())
        weight_sum = sum(performance_weights.get(self._determine_signal_type(k), 1.0) for k in directional_signals)
        resolved_directional = weighted_sum / weight_sum if weight_sum > 0 else 0
        resolved_signals['resolved_directional'] = resolved_directional
    
    # Similar resolution for volatility and time decay signals...
    
    # 5. Generate integrated signal set
    integrated_signals = self._generate_integrated_signals(resolved_signals, performance_weights)
    
    # Combine resolved signals into final integrated set
    integrated_signals = {
        'directional': resolved_signals.get('resolved_directional', 0),
        'volatility': resolved_signals.get('resolved_volatility', 0),
        'time_decay': resolved_signals.get('resolved_time_decay', 0),
        'complex': resolved_signals.get('resolved_complex', 0),
        'overall_bias': self._calculate_overall_bias(resolved_signals, performance_weights)
    }
    
    return {
        "integrated_signals": integrated_signals,
        "performance_weights": performance_weights,
        "time_adjusted_signals": time_adjusted_signals,
        "regime_adapted_signals": regime_adapted_signals,
        "resolved_signals": resolved_signals
    }
```

**Key Improvements:**
- **Performance-Based Signal Weighting**: Weights signals based on historical success
- **Enhanced Time-Based Profiles**: Applies sophisticated time-of-day adjustments
- **Market Regime Adaptation**: Adapts signal interpretation to current market regime
- **Signal Conflict Resolution**: Implements weighted voting for conflict resolution

**Market Impact:**
This component significantly improves signal quality by integrating multiple signals into a coherent whole, accounting for time of day, market regime, and historical performance. This leads to more consistent and reliable trade recommendations that adapt to changing market conditions.

### 4. Intelligent Recommendation Management

**Core Enhancement Concept:**
Develop intelligent recommendation management with adaptive exit thresholds, enhanced performance tracking, and partial position management.

**Detailed Implementation:**
```python
def manage_recommendations_intelligently(self, active_recommendations, current_price, market_conditions, new_signals):
    """
    Manage recommendations intelligently with adaptive exits and performance tracking.
    """
    # 1. Calculate adaptive exit thresholds
    adaptive_exits = self._calculate_adaptive_exit_thresholds(active_recommendations, market_conditions)
    
    # Adjust exit thresholds based on volatility and other factors
    adaptive_exits = {}
    
    for rec_id, recommendation in active_recommendations.items():
        # Get base exit parameters
        base_stop = recommendation['stop_loss_percentage']
        base_target = recommendation['profit_target_percentage']
        
        # Calculate volatility adjustment factor
        current_volatility = market_conditions['current_volatility']
        historical_volatility = market_conditions['historical_volatility']
        volatility_ratio = current_volatility / historical_volatility if historical_volatility > 0 else 1
        
        # More volatile = wider stops, higher targets
        volatility_adjustment_factor = math.sqrt(volatility_ratio)
        
        # Calculate time-based adjustment
        entry_time = recommendation['entry_time']
        current_time = market_conditions['current_time']
        time_elapsed = (current_time - entry_time).total_seconds() / 3600  # Hours
        
        # Tighten stops as time passes (for day trades)
        time_factor = max(0.7, 1 - (time_elapsed / 8) * 0.3)  # Reduce by up to 30% over 8 hours
        
        # Calculate signal-based adjustment
        signal_strength = abs(new_signals.get('directional', 0))
        signal_direction = 1 if new_signals.get('directional', 0) > 0 else -1
        recommendation_direction = 1 if recommendation['direction'] == 'bullish' else -1
        
        # If signals are strengthening in our direction, allow more room
        # If signals are strengthening against our direction, tighten stops
        signal_agreement = signal_direction == recommendation_direction
        signal_factor = 1 + (0.2 * signal_strength) if signal_agreement else 1 - (0.2 * signal_strength)
        
        # Calculate final adaptive exits
        adaptive_stop = base_stop * volatility_adjustment_factor * time_factor * signal_factor
        adaptive_target = base_target * volatility_adjustment_factor * signal_factor
        
        adaptive_exits[rec_id] = {
            'adaptive_stop_loss_percentage': adaptive_stop,
            'adaptive_profit_target_percentage': adaptive_target,
            'volatility_adjustment_factor': volatility_adjustment_factor,
            'time_factor': time_factor,
            'signal_factor': signal_factor
        }
    
    # 2. Track recommendation performance
    performance_metrics = self._track_recommendation_performance(active_recommendations, current_price)
    
    # Calculate performance metrics for each recommendation
    performance_metrics = {}
    
    for rec_id, recommendation in active_recommendations.items():
        entry_price = recommendation['entry_price']
        current_pnl_pct = ((current_price - entry_price) / entry_price) * 100 if recommendation['direction'] == 'bullish' else ((entry_price - current_price) / entry_price) * 100
        
        # Calculate metrics
        performance_metrics[rec_id] = {
            'current_pnl_percentage': current_pnl_pct,
            'max_pnl_percentage': max(current_pnl_pct, recommendation.get('max_pnl_percentage', 0)),
            'min_pnl_percentage': min(current_pnl_pct, recommendation.get('min_pnl_percentage', float('inf'))),
            'time_in_trade': (market_conditions['current_time'] - recommendation['entry_time']).total_seconds() / 60,  # Minutes
            'price_path_efficiency': self._calculate_price_path_efficiency(recommendation, current_price),
            'signal_alignment': self._calculate_signal_alignment(recommendation, new_signals)
        }
    
    # 3. Apply learning from past recommendations
    adjusted_recommendations = self._apply_recommendation_learning(active_recommendations, performance_metrics)
    
    # Adjust recommendations based on historical performance
    adjusted_recommendations = {}
    
    for rec_id, recommendation in active_recommendations.items():
        strategy_type = recommendation['strategy_type']
        
        # Get historical performance for this strategy type
        historical_performance = self._get_historical_strategy_performance(strategy_type)
        
        # Calculate adjustment factors based on historical performance
        avg_hold_time = historical_performance.get('average_hold_time', 120)  # Minutes
        avg_max_profit = historical_performance.get('average_max_profit_percentage', 50)
        optimal_exit_time = historical_performance.get('optimal_exit_time_percentage', 70)  # % of avg hold time
        
        # Calculate optimal exit parameters
        current_hold_time = performance_metrics[rec_id]['time_in_trade']
        hold_time_percentage = (current_hold_time / avg_hold_time) * 100 if avg_hold_time > 0 else 0
        
        # Adjust recommendation based on learned patterns
        adjusted_recommendations[rec_id] = recommendation.copy()
        
        # If we're approaching optimal exit time, start tightening stops
        if hold_time_percentage > optimal_exit_time:
            tightening_factor = min(1, (hold_time_percentage - optimal_exit_time) / (100 - optimal_exit_time))
            adjusted_recommendations[rec_id]['stop_loss_percentage'] *= (1 - 0.3 * tightening_factor)  # Tighten by up to 30%
        
        # If we've captured a significant portion of average max profit, start taking profits
        current_profit = performance_metrics[rec_id]['current_pnl_percentage']
        if current_profit > 0 and avg_max_profit > 0:
            profit_percentage = (current_profit / avg_max_profit) * 100
            if profit_percentage > 70:  # Captured 70% of average max profit
                adjusted_recommendations[rec_id]['profit_taking_suggested'] = True
                adjusted_recommendations[rec_id]['profit_taking_reason'] = f"Captured {profit_percentage:.1f}% of average maximum profit"
    
    # 4. Manage partial positions
    position_management = self._manage_partial_positions(adjusted_recommendations, current_price, new_signals)
    
    # Calculate position management recommendations
    position_management = {}
    
    for rec_id, recommendation in adjusted_recommendations.items():
        current_pnl = performance_metrics[rec_id]['current_pnl_percentage']
        max_pnl = performance_metrics[rec_id]['max_pnl_percentage']
        
        # Initialize with no action
        position_management[rec_id] = {
            'action': 'hold',
            'percentage': 100,
            'reason': 'Maintaining position'
        }
        
        # Check for partial profit taking
        if current_pnl > 0:
            # If we've reached 50% of target, take partial profits
            if current_pnl >= recommendation['profit_target_percentage'] * 0.5:
                position_management[rec_id] = {
                    'action': 'reduce',
                    'percentage': 50,
                    'reason': f"Taking partial profits at {current_pnl:.1f}% gain"
                }
            
            # If we've pulled back significantly from max profit, take partial profits
            elif max_pnl > current_pnl and (max_pnl - current_pnl) > (max_pnl * 0.3):
                position_management[rec_id] = {
                    'action': 'reduce',
                    'percentage': 50,
                    'reason': f"Protecting gains after {((max_pnl - current_pnl) / max_pnl * 100):.1f}% pullback from max profit"
                }
        
        # Check for scaling into position
        elif current_pnl < 0 and recommendation.get('conviction') == 'high':
            # If we're down but signals remain strong, consider adding
            signal_alignment = performance_metrics[rec_id]['signal_alignment']
            if signal_alignment > 0.8:  # Strong signal alignment
                position_management[rec_id] = {
                    'action': 'increase',
                    'percentage': 50,
                    'reason': f"Adding to high-conviction position with strong signal alignment"
                }
    
    # 5. Generate updated recommendation statuses
    updated_recommendations = self._generate_updated_recommendations(
        adjusted_recommendations,
        adaptive_exits,
        position_management,
        new_signals
    )
    
    # Combine all information into updated recommendations
    updated_recommendations = {}
    
    for rec_id, recommendation in adjusted_recommendations.items():
        # Get relevant data
        exits = adaptive_exits.get(rec_id, {})
        performance = performance_metrics.get(rec_id, {})
        position = position_management.get(rec_id, {})
        
        # Determine status
        current_pnl = performance.get('current_pnl_percentage', 0)
        
        if current_pnl <= -exits.get('adaptive_stop_loss_percentage', recommendation['stop_loss_percentage']):
            status = 'stopped_out'
            action = 'exit'
            reason = f"Stopped out at {current_pnl:.1f}% loss"
        elif current_pnl >= exits.get('adaptive_profit_target_percentage', recommendation['profit_target_percentage']):
            status = 'target_reached'
            action = 'exit'
            reason = f"Profit target reached at {current_pnl:.1f}% gain"
        else:
            status = 'active'
            action = position.get('action', 'hold')
            reason = position.get('reason', 'Maintaining position')
        
        # Create updated recommendation
        updated_recommendations[rec_id] = {
            'original_recommendation': recommendation,
            'current_status': status,
            'current_pnl_percentage': current_pnl,
            'recommended_action': action,
            'action_reason': reason,
            'adaptive_exits': exits,
            'performance_metrics': performance,
            'position_management': position,
            'signal_alignment': performance.get('signal_alignment', 0)
        }
    
    return {
        "updated_recommendations": updated_recommendations,
        "adaptive_exits": adaptive_exits,
        "performance_metrics": performance_metrics,
        "adjusted_recommendations": adjusted_recommendations,
        "position_management": position_management
    }
```

**Key Improvements:**
- **Adaptive Exit Thresholds**: Dynamically adjusts exit thresholds based on market conditions
- **Enhanced Performance Tracking**: Implements comprehensive tracking of recommendation performance
- **Learning from Past Recommendations**: Adjusts recommendations based on historical performance
- **Partial Position Management**: Adds support for scaling in/out of positions

**Market Impact:**
This component significantly improves trade management by dynamically adjusting exit parameters based on market conditions and trade performance. It also enables more sophisticated position management with partial profit-taking and position scaling, leading to better risk management and higher overall returns.

## Integration with Enhanced Metrics and Key Levels

The Adaptive Trade Idea Framework integrates seamlessly with the enhanced metrics and key levels:

### Metric Integration

1. **Enhanced Rolling Flow Metrics**
   - VAPI-FA provides early indication of institutional positioning for trade idea generation
   - DWFD identifies potential reversal points for counter-trend trade ideas
   - TW-LAF confirms sustainable flow for continuation trade ideas

2. **Enhanced Heatmap Combinations**
   - SGDHP identifies key support/resistance levels for entry and exit points
   - IVSDH guides volatility strategy selection and timing
   - UGCH provides comprehensive structural view for trade idea context

### Key Level Integration

1. **Multi-Timeframe Support and Resistance**
   - Intraday levels guide day trading entries and exits
   - Daily levels provide context for trade idea generation
   - Weekly levels establish the broader framework for risk management

2. **Conviction-Based Levels**
   - High-conviction levels serve as primary targets for trade ideas
   - Level strength scores inform position sizing decisions
   - Historical level performance guides exit parameter adjustment

## Implementation Recommendations

### Data Requirements
- Historical signal performance data
- Trade recommendation performance history
- Real-time market condition data
- Current signal values from enhanced metrics

### Calculation Frequency
- Performance-based conviction mapping: Daily recalibration
- Strategy recommendations: Generated on signal triggers
- Dynamic signal integration: Updated every 5-15 minutes
- Recommendation management: Continuous monitoring with 1-minute updates

### User Interface Considerations
- Clear visualization of conviction levels
- Detailed strategy explanations with risk parameters
- Position management dashboard with adaptive exits
- Historical performance tracking for continuous improvement

## Conclusion

The Adaptive Trade Idea Framework represents a significant advancement in options trading strategy generation and management. By implementing performance-based conviction mapping, enhanced strategy specificity, dynamic signal integration, and intelligent recommendation management, the framework transforms the Elite Options Trading System into a highly adaptive, self-improving trading system.

This framework addresses the limitations of the current system by making trade recommendations more specific, adaptive, and performance-driven. The integration with enhanced metrics and key levels creates a cohesive ecosystem that provides traders with a comprehensive solution for day trading SPY/SPX options with higher probability of success and better risk management.
