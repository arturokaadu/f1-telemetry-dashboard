"""
F1 Tire Degradation Analysis Module
Machine Learning for tire wear prediction and strategy optimization
Created by Luna for Arturo's portfolio
"""

import numpy as np
from scipy.optimize import curve_fit
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import json


@dataclass
class TireDegradation:
    """Represents tire degradation analysis results"""
    compound: str
    degradation_rate: float  # seconds per lap
    optimal_stint_length: int
    cliff_lap: Optional[int]
    performance_loss_percent: float
    strategy_recommendation: str


def degradation_model(lap: np.ndarray, base_time: float, deg_rate: float, 
                      cliff_factor: float = 0.0, cliff_start: float = 30.0) -> np.ndarray:
    """
    Non-linear tire degradation model
    
    Args:
        lap: Lap number array
        base_time: Initial lap time on fresh tires
        deg_rate: Linear degradation rate (seconds/lap)
        cliff_factor: Exponential cliff factor (0 = no cliff)
        cliff_start: Lap where cliff begins
        
    Returns:
        Predicted lap times
    """
    linear_deg = base_time + (deg_rate * lap)
    cliff_effect = cliff_factor * np.maximum(0, lap - cliff_start) ** 2
    return linear_deg + cliff_effect


def analyze_tire_degradation(lap_times: List[float], 
                              compound: str = "MEDIUM") -> TireDegradation:
    """
    Analyze tire degradation from lap time data
    
    Args:
        lap_times: List of lap times in seconds
        compound: Tire compound (SOFT, MEDIUM, HARD)
        
    Returns:
        TireDegradation analysis object
    """
    if len(lap_times) < 5:
        return TireDegradation(
            compound=compound,
            degradation_rate=0.0,
            optimal_stint_length=len(lap_times),
            cliff_lap=None,
            performance_loss_percent=0.0,
            strategy_recommendation="Insufficient data"
        )
    
    laps = np.arange(len(lap_times))
    times = np.array(lap_times)
    
    # Remove outliers (pit laps, safety cars, etc.)
    median_time = np.median(times)
    valid_mask = times < (median_time * 1.1)  # Within 10% of median
    clean_laps = laps[valid_mask]
    clean_times = times[valid_mask]
    
    if len(clean_times) < 5:
        clean_laps = laps
        clean_times = times
    
    # Fit linear degradation model first
    try:
        popt_linear, _ = curve_fit(
            lambda x, a, b: a + b * x,
            clean_laps,
            clean_times,
            p0=[clean_times[0], 0.05],
            bounds=([clean_times.min() - 5, 0], [clean_times.max() + 5, 1.0])
        )
        base_time, deg_rate = popt_linear
    except Exception:
        base_time = clean_times[0]
        deg_rate = (clean_times[-1] - clean_times[0]) / len(clean_times)
    
    # Try to fit cliff model
    cliff_lap = None
    try:
        popt_cliff, _ = curve_fit(
            degradation_model,
            clean_laps,
            clean_times,
            p0=[base_time, deg_rate, 0.001, len(clean_laps) * 0.7],
            bounds=(
                [clean_times.min() - 5, 0, 0, 5],
                [clean_times.max() + 5, 1.0, 0.1, len(clean_laps)]
            ),
            maxfev=2000
        )
        cliff_factor, cliff_start = popt_cliff[2], popt_cliff[3]
        if cliff_factor > 0.0005:  # Significant cliff detected
            cliff_lap = int(cliff_start)
    except Exception:
        pass
    
    # Calculate optimal stint length
    if cliff_lap:
        optimal_stint = cliff_lap - 2  # Stop 2 laps before cliff
    else:
        # Based on degradation rate and typical F1 strategies
        if compound == "SOFT":
            optimal_stint = min(15, max(10, int(0.5 / max(deg_rate, 0.01))))
        elif compound == "HARD":
            optimal_stint = min(35, max(20, int(1.0 / max(deg_rate, 0.01))))
        else:  # MEDIUM
            optimal_stint = min(25, max(15, int(0.7 / max(deg_rate, 0.01))))
    
    # Performance loss calculation
    performance_loss = (clean_times[-1] - clean_times[0]) / clean_times[0] * 100
    
    # Strategy recommendation
    if deg_rate < 0.03:
        recommendation = "Low degradation - extend stint for track position"
    elif deg_rate < 0.08:
        recommendation = "Normal degradation - follow planned strategy"
    elif deg_rate < 0.15:
        recommendation = "High degradation - consider early pit stop"
    else:
        recommendation = "Severe degradation - pit ASAP for fresh tires"
    
    if cliff_lap and cliff_lap < len(lap_times) + 5:
        recommendation += f" | WARNING: Tire cliff predicted at lap {cliff_lap}"
    
    return TireDegradation(
        compound=compound,
        degradation_rate=round(deg_rate, 4),
        optimal_stint_length=optimal_stint,
        cliff_lap=cliff_lap,
        performance_loss_percent=round(performance_loss, 2),
        strategy_recommendation=recommendation
    )


def compare_tire_compounds(stints: Dict[str, List[float]]) -> Dict[str, any]:
    """
    Compare degradation across different tire compounds
    
    Args:
        stints: Dictionary of compound -> lap_times
        
    Returns:
        Comparison analysis
    """
    results = {}
    
    for compound, lap_times in stints.items():
        analysis = analyze_tire_degradation(lap_times, compound)
        results[compound] = {
            'degradation_rate': analysis.degradation_rate,
            'optimal_stint': analysis.optimal_stint_length,
            'cliff_lap': analysis.cliff_lap,
            'performance_loss': analysis.performance_loss_percent
        }
    
    # Determine best strategy
    if results:
        sorted_compounds = sorted(
            results.items(),
            key=lambda x: (x[1]['degradation_rate'], -x[1]['optimal_stint'])
        )
        best_compound = sorted_compounds[0][0]
    else:
        best_compound = None
    
    return {
        'compounds': results,
        'recommendation': f"Best compound for race pace: {best_compound}" if best_compound else "No data"
    }


def predict_lap_time(lap_number: int, base_time: float, 
                     deg_rate: float, fuel_effect: float = 0.03) -> float:
    """
    Predict lap time considering tire degradation and fuel load
    
    Args:
        lap_number: Current lap number in stint
        base_time: Base lap time on fresh tires
        deg_rate: Tire degradation rate (seconds/lap)
        fuel_effect: Fuel saving per lap (seconds/lap, typical ~0.03s)
        
    Returns:
        Predicted lap time
    """
    tire_deg = deg_rate * lap_number
    fuel_gain = fuel_effect * lap_number  # Lighter car = faster
    return base_time + tire_deg - fuel_gain


def calculate_optimal_pit_window(
    current_lap: int,
    total_laps: int,
    current_tire_age: int,
    deg_rate: float,
    pit_stop_loss: float = 22.0,  # Typical pit stop time loss
    new_tire_advantage: float = 1.0  # Typical advantage on new tires
) -> Tuple[int, int, str]:
    """
    Calculate optimal pit window
    
    Returns:
        (earliest_lap, latest_lap, recommendation)
    """
    remaining_laps = total_laps - current_lap
    
    # Calculate when pit stop break-even happens
    laps_to_recover = pit_stop_loss / max(new_tire_advantage, 0.1)
    
    # Earliest optimal: when you can recover pit loss before finish
    earliest = current_lap + max(0, int(current_tire_age * 0.1))
    
    # Latest optimal: leave enough laps to use new tires
    latest = total_laps - int(laps_to_recover) - 5
    
    # Current recommendation
    if deg_rate > 0.1 and current_tire_age > 15:
        recommendation = "PIT NOW - High degradation"
    elif latest - current_lap < 5:
        recommendation = "FINAL WINDOW - Pit within 5 laps"
    elif current_lap < earliest:
        recommendation = f"WAIT - Optimal window starts lap {earliest}"
    else:
        recommendation = f"OPTIMAL WINDOW - Pit laps {earliest}-{latest}"
    
    return (max(1, earliest), max(earliest + 1, latest), recommendation)


# API endpoint helpers for Flask

def tire_analysis_to_json(analysis: TireDegradation) -> dict:
    """Convert TireDegradation to JSON-serializable dict"""
    return {
        'compound': analysis.compound,
        'degradation_rate_per_lap': analysis.degradation_rate,
        'optimal_stint_length': analysis.optimal_stint_length,
        'cliff_lap': analysis.cliff_lap,
        'performance_loss_percent': analysis.performance_loss_percent,
        'strategy_recommendation': analysis.strategy_recommendation
    }


if __name__ == "__main__":
    # Test with sample data
    sample_laps = [
        82.5, 82.6, 82.8, 82.9, 83.0, 83.2, 83.4, 83.5, 83.7, 83.9,
        84.1, 84.3, 84.6, 84.9, 85.2, 85.6, 86.0, 86.5, 87.1, 87.8
    ]
    
    analysis = analyze_tire_degradation(sample_laps, "SOFT")
    print("🏎️ Tire Degradation Analysis")
    print("=" * 40)
    print(f"Compound: {analysis.compound}")
    print(f"Degradation Rate: {analysis.degradation_rate:.4f} s/lap")
    print(f"Optimal Stint: {analysis.optimal_stint_length} laps")
    print(f"Cliff Lap: {analysis.cliff_lap or 'Not detected'}")
    print(f"Performance Loss: {analysis.performance_loss_percent:.1f}%")
    print(f"Strategy: {analysis.strategy_recommendation}")
