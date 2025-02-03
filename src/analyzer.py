import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from typing import Dict

class DataAnalyzer:
    def calculate_spending_metrics(self, df: pd.DataFrame) -> Dict:
        total_spend = df['amount'].sum()
        monthly_spend = df.groupby(df['date'].dt.to_period('M'))['amount'].sum().mean()
        
        return {
            'total_spend': total_spend,
            'average_monthly_spend': monthly_spend,
            'trend': {'slope': 0, 'trend_direction': 'stable'}
        }
    
    def predict_future_spending(self, df: pd.DataFrame, periods: int = 3) -> pd.Series:
        monthly = df.groupby(df['date'].dt.to_period('M'))['amount'].sum()
        return pd.Series([monthly.mean()] * periods, index=range(periods))