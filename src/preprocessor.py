import pandas as pd
import numpy as np
from typing import Dict

class DataPreprocessor:
    def clean_financial_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and prepare financial data for analysis."""
        cleaned = df.copy()
        
        # Handle missing values
        cleaned['amount'] = cleaned['amount'].fillna(0)
        
        # Remove duplicates
        cleaned = cleaned.drop_duplicates()
        
        # Convert date columns
        cleaned['date'] = pd.to_datetime(cleaned['date'])
        
        # Standardize categories
        cleaned['category'] = cleaned['category'].str.lower()
        
        return cleaned
    
    def aggregate_by_period(self, df: pd.DataFrame, period: str = 'M') -> pd.DataFrame:
        """Aggregate financial data by specified period."""
        return df.groupby([
            pd.Grouper(key='date', freq=period),
            'category'
        ])['amount'].sum().reset_index()