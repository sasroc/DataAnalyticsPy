import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from typing import Dict

class DataAnalyzer:
    def _get_appropriate_freq(self, days: int) -> tuple:
        """Determine appropriate frequency and periods based on date range."""
        if days <= 7:
            return 'H', 168  # Hourly for a week
        elif days <= 30:
            return '6H', 120  # 6-hourly for a month
        elif days <= 90:
            return 'D', 90   # Daily for 3 months
        else:
            return 'W', 52   # Weekly for a year

    def calculate_spending_metrics(self, df: pd.DataFrame) -> Dict:
        total_spend = float(df['amount'].sum())
        
        # Calculate true daily average instead of monthly
        daily_avg = float(df.groupby(pd.Grouper(key='date', freq='D'))['amount'].sum().mean())
        monthly_avg = daily_avg * 30.44  # Average days in a month
        
        # Get time-appropriate aggregation
        date_range = (df['date'].max() - df['date'].min()).days
        freq, _ = self._get_appropriate_freq(date_range)
        
        # Create time series with appropriate frequency
        time_series = df.resample(freq, on='date')['amount'].sum().fillna(0)
        
        # Calculate trend
        if len(time_series) > 1:
            X = np.arange(len(time_series)).reshape(-1, 1)
            y = time_series.values.astype(float)
            model = LinearRegression()
            model.fit(X, y)
            slope = float(model.coef_[0])
            r2_score = model.score(X, y)
        else:
            slope = 0.0
            r2_score = 0.0

        return {
            'total_spend': total_spend,
            'average_monthly_spend': monthly_avg,
            'trend': {
                'slope': slope,
                'r2_score': r2_score,
                'trend_direction': 'increasing' if slope > 0 else 'decreasing'
            }
        }
    
    def predict_future_spending(self, df: pd.DataFrame) -> pd.Series:
        date_range = (df['date'].max() - df['date'].min()).days
        freq, periods = self._get_appropriate_freq(date_range)
        
        # Create evenly spaced time series
        time_series = df.resample(freq, on='date')['amount'].sum().fillna(method='ffill')
        
        if len(time_series) > 1:
            # Prepare data for modeling
            X = np.arange(len(time_series)).reshape(-1, 1)
            y = time_series.values.astype(float)
            
            # Fit model with regularization
            model = LinearRegression()
            model.fit(X, y)
            
            # Generate future predictions
            future_X = np.arange(len(time_series), len(time_series) + periods).reshape(-1, 1)
            base_predictions = model.predict(future_X)
            
            # Add historical volatility
            volatility = np.std(y)
            predictions = base_predictions + np.random.normal(0, volatility * 0.1, size=len(base_predictions))
            predictions = np.maximum(predictions, 0)  # Ensure non-negative values
        else:
            predictions = np.repeat(time_series.mean(), periods)
        
        # Generate future dates
        future_dates = pd.date_range(
            start=time_series.index[-1] + pd.Timedelta(hours=1),
            periods=periods,
            freq=freq
        )
        
        return pd.Series(predictions, index=future_dates)