import pandas as pd
from typing import Dict

class DataPreprocessor:
    def clean_financial_data(self, df: pd.DataFrame) -> pd.DataFrame:
        cleaned = df.copy()
        cleaned['amount'] = cleaned['amount'].fillna(0)
        cleaned = cleaned.drop_duplicates()
        cleaned['date'] = pd.to_datetime(cleaned['date'])
        return cleaned