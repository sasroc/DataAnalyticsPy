import pandas as pd
from sqlalchemy import create_engine
from typing import Dict, List

class DataLoader:
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)
    
    def load_department_data(self, department_id: str) -> pd.DataFrame:
        """Load department specific data from database."""
        query = """
            SELECT date, expense_type, amount, transaction_id, category
            FROM department_expenses
            WHERE department_id = %s
            ORDER BY date
        """
        return pd.read_sql(query, self.engine, params=[department_id])
    
    def load_budget_data(self, fiscal_year: str) -> pd.DataFrame:
        """Load budget allocation and spending data."""
        query = """
            SELECT department_id, allocated_budget, spent_amount,
                   remaining_budget, quarter
            FROM budget_tracking
            WHERE fiscal_year = %s
        """
        return pd.read_sql(query, self.engine, params=[fiscal_year])