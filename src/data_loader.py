import pandas as pd
from sqlalchemy import create_engine
from typing import Dict, List

class DataLoader:
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)
    
    def load_department_data(self, department_id: str) -> pd.DataFrame:
        query = """
            SELECT date, category, amount, transaction_id
            FROM department_expenses
            WHERE department_id = :dept_id
            ORDER BY date
        """
        return pd.read_sql(query, self.engine, params={"dept_id": department_id})