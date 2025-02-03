from typing import Dict, List
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

class DataAnalyzer:
    def calculate_spending_metrics(self, df: pd.DataFrame) -> Dict:
        """Calculate key spending metrics."""
        metrics = {
            'total_spend': df['amount'].sum(),
            'average_monthly_spend': df.groupby(
                df['date'].dt.to_period('M')
            )['amount'].sum().mean(),
            'spending_by_category': df.groupby('category')['amount'].sum().to_dict(),
            'trend': self._calculate_trend(df)
        }
        return metrics
    
    def _calculate_trend(self, df: pd.DataFrame) -> Dict:
        """Calculate spending trends over time."""
        monthly_data = df.groupby(df['date'].dt.to_period('M'))['amount'].sum()
        X = np.arange(len(monthly_data)).reshape(-1, 1)
        y = monthly_data.values
        
        model = LinearRegression()
        model.fit(X, y)
        
        trend = {
            'slope': model.coef_[0],
            'intercept': model.intercept_,
            'trend_direction': 'increasing' if model.coef_[0] > 0 else 'decreasing'
        }
        return trend

    def predict_future_spending(self, df: pd.DataFrame, periods: int = 3) -> pd.Series:
        """Predict future spending based on historical data."""
        monthly_data = df.groupby(df['date'].dt.to_period('M'))['amount'].sum()
        X = np.arange(len(monthly_data)).reshape(-1, 1)
        
        model = LinearRegression()
        model.fit(X, monthly_data.values)
        
        future_X = np.arange(len(monthly_data), len(monthly_data) + periods).reshape(-1, 1)
        predictions = model.predict(future_X)
        
        return pd.Series(predictions, index=pd.period_range(
            monthly_data.index[-1] + 1,
            periods=periods,
            freq='M'
        ))
