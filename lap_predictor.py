"""
F1 Lap Time Prediction Model
Machine Learning for race strategy optimization
Created by Luna for Arturo's portfolio
"""

import numpy as np
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import cross_val_score
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
import json


@dataclass
class LapPrediction:
    """Prediction results for lap times"""
    predicted_time: float
    confidence: float
    factors: Dict[str, float]
    model_used: str


class LapTimePredictor:
    """
    ML model for predicting lap times based on multiple factors:
    - Tire age
    - Fuel load
    - Track position
    - Tire compound
    - Weather conditions
    """
    
    def __init__(self):
        self.model = None
        self.poly_features = None
        self.is_fitted = False
        self.feature_names = [
            'tire_age', 'fuel_load', 'track_position', 
            'compound_soft', 'compound_medium', 'compound_hard',
            'lap_number'
        ]
        self.base_lap_time = 80.0  # Default base time
        
    def prepare_features(self, 
                         tire_age: int,
                         fuel_load: float,
                         track_position: int,
                         compound: str,
                         lap_number: int) -> np.ndarray:
        """Convert raw inputs to feature array"""
        features = [
            tire_age,
            fuel_load,
            track_position,
            1 if compound == 'SOFT' else 0,
            1 if compound == 'MEDIUM' else 0,
            1 if compound == 'HARD' else 0,
            lap_number
        ]
        return np.array(features).reshape(1, -1)
    
    def fit(self, X: np.ndarray, y: np.ndarray, use_polynomial: bool = True):
        """
        Train the prediction model
        
        Args:
            X: Feature matrix (n_samples, n_features)
            y: Target lap times
            use_polynomial: Whether to use polynomial features
        """
        if use_polynomial:
            self.poly_features = PolynomialFeatures(degree=2, include_bias=False)
            X_poly = self.poly_features.fit_transform(X)
            self.model = Ridge(alpha=1.0)
            self.model.fit(X_poly, y)
        else:
            self.model = LinearRegression()
            self.model.fit(X, y)
        
        self.base_lap_time = np.mean(y)
        self.is_fitted = True
        
        # Calculate cross-validation score
        if len(y) >= 5:
            scores = cross_val_score(self.model, 
                                     X_poly if use_polynomial else X, 
                                     y, cv=min(5, len(y)))
            return np.mean(scores)
        return 0.0
    
    def predict(self, 
                tire_age: int,
                fuel_load: float = 100.0,
                track_position: int = 10,
                compound: str = 'MEDIUM',
                lap_number: int = 1) -> LapPrediction:
        """
        Predict lap time for given conditions
        
        Returns:
            LapPrediction with predicted time and confidence
        """
        if not self.is_fitted:
            # Use analytical model if not trained
            return self._analytical_prediction(
                tire_age, fuel_load, track_position, compound, lap_number
            )
        
        X = self.prepare_features(tire_age, fuel_load, track_position, 
                                  compound, lap_number)
        
        if self.poly_features:
            X = self.poly_features.transform(X)
        
        predicted = self.model.predict(X)[0]
        
        # Calculate feature contributions
        factors = {
            'tire_degradation': tire_age * 0.05,
            'fuel_effect': -fuel_load * 0.03,
            'traffic_effect': max(0, (track_position - 5) * 0.1),
            'compound_modifier': self._compound_modifier(compound)
        }
        
        return LapPrediction(
            predicted_time=round(predicted, 3),
            confidence=0.85,
            factors=factors,
            model_used='polynomial_regression'
        )
    
    def _analytical_prediction(self,
                               tire_age: int,
                               fuel_load: float,
                               track_position: int,
                               compound: str,
                               lap_number: int) -> LapPrediction:
        """Fallback analytical model when ML model not trained"""
        
        # Base time adjustments
        tire_deg = tire_age * 0.05  # 0.05s per lap on tires
        fuel_effect = (100 - fuel_load) * 0.03 / 100  # Lighter = faster
        traffic = max(0, (track_position - 5) * 0.1)  # Dirty air effect
        compound_mod = self._compound_modifier(compound)
        
        predicted = (self.base_lap_time + 
                     tire_deg - 
                     fuel_effect + 
                     traffic + 
                     compound_mod)
        
        factors = {
            'tire_degradation': tire_deg,
            'fuel_effect': -fuel_effect,
            'traffic_effect': traffic,
            'compound_modifier': compound_mod
        }
        
        return LapPrediction(
            predicted_time=round(predicted, 3),
            confidence=0.6,  # Lower confidence for analytical
            factors=factors,
            model_used='analytical'
        )
    
    def _compound_modifier(self, compound: str) -> float:
        """Get lap time modifier for tire compound"""
        modifiers = {
            'SOFT': -0.8,    # Faster but degrades quickly
            'MEDIUM': 0.0,   # Baseline
            'HARD': 0.5,     # Slower but more durable
            'INTERMEDIATE': 1.5,
            'WET': 3.0
        }
        return modifiers.get(compound.upper(), 0.0)


def predict_race_strategy(
    total_laps: int,
    base_lap_time: float,
    compounds_available: List[str] = ['SOFT', 'MEDIUM', 'HARD'],
    pit_stop_time: float = 22.0
) -> Dict:
    """
    Predict optimal race strategy
    
    Returns:
        Strategy recommendation with pit stops and compound choices
    """
    strategies = []
    
    # 1-stop strategy
    if total_laps <= 50:
        stint1_laps = total_laps // 2
        stint2_laps = total_laps - stint1_laps
        strategies.append({
            'name': '1-Stop',
            'stops': [stint1_laps],
            'compounds': ['MEDIUM', 'HARD'],
            'estimated_time': _calculate_race_time(
                [stint1_laps, stint2_laps],
                ['MEDIUM', 'HARD'],
                base_lap_time,
                pit_stop_time
            )
        })
    
    # 2-stop strategy
    stint1 = total_laps // 3
    stint2 = total_laps // 3
    stint3 = total_laps - stint1 - stint2
    strategies.append({
        'name': '2-Stop',
        'stops': [stint1, stint1 + stint2],
        'compounds': ['SOFT', 'MEDIUM', 'HARD'],
        'estimated_time': _calculate_race_time(
            [stint1, stint2, stint3],
            ['SOFT', 'MEDIUM', 'HARD'],
            base_lap_time,
            pit_stop_time
        )
    })
    
    # Aggressive strategy
    strategies.append({
        'name': 'Aggressive',
        'stops': [total_laps // 4, total_laps // 2, 3 * total_laps // 4],
        'compounds': ['SOFT', 'SOFT', 'SOFT', 'MEDIUM'],
        'estimated_time': _calculate_race_time(
            [total_laps // 4, total_laps // 4, total_laps // 4, total_laps - 3 * (total_laps // 4)],
            ['SOFT', 'SOFT', 'SOFT', 'MEDIUM'],
            base_lap_time,
            pit_stop_time
        )
    })
    
    # Find optimal
    optimal = min(strategies, key=lambda x: x['estimated_time'])
    
    return {
        'total_laps': total_laps,
        'strategies': strategies,
        'recommended': optimal['name'],
        'estimated_advantage': round(
            max(s['estimated_time'] for s in strategies) - optimal['estimated_time'], 
            2
        )
    }


def _calculate_race_time(stints: List[int], 
                         compounds: List[str],
                         base_time: float,
                         pit_time: float) -> float:
    """Calculate total race time for a strategy"""
    predictor = LapTimePredictor()
    predictor.base_lap_time = base_time
    
    total_time = 0.0
    fuel = 100.0
    fuel_per_lap = 100.0 / sum(stints)
    
    for stint_idx, (stint_laps, compound) in enumerate(zip(stints, compounds)):
        for lap in range(stint_laps):
            pred = predictor._analytical_prediction(
                tire_age=lap,
                fuel_load=fuel,
                track_position=5,
                compound=compound,
                lap_number=lap
            )
            total_time += pred.predicted_time
            fuel -= fuel_per_lap
    
    # Add pit stop times
    total_time += pit_time * (len(stints) - 1)
    
    return round(total_time, 2)


def prediction_to_json(prediction: LapPrediction) -> dict:
    """Convert LapPrediction to JSON-serializable dict"""
    return {
        'predicted_time': prediction.predicted_time,
        'confidence': prediction.confidence,
        'factors': prediction.factors,
        'model_used': prediction.model_used
    }


if __name__ == "__main__":
    # Test the predictor
    print("🏎️ Lap Time Prediction Test")
    print("=" * 40)
    
    predictor = LapTimePredictor()
    predictor.base_lap_time = 82.0
    
    for tire_age in [1, 10, 20, 30]:
        pred = predictor.predict(
            tire_age=tire_age,
            fuel_load=100 - (tire_age * 2),
            track_position=5,
            compound='MEDIUM',
            lap_number=tire_age
        )
        print(f"Lap {tire_age}: {pred.predicted_time}s (confidence: {pred.confidence})")
    
    print("\n🏁 Race Strategy Prediction")
    print("=" * 40)
    
    strategy = predict_race_strategy(57, 82.0)  # Monaco
    print(f"Recommended: {strategy['recommended']}")
    print(f"Advantage: {strategy['estimated_advantage']}s")
