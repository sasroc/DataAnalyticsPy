# src/sample_data.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sqlite3

def generate_sample_data():
    # Generate dates
    start_date = datetime.now() - timedelta(days=365)
    dates = [start_date + timedelta(days=x) for x in range(365)]
    
    # Categories
    categories = ['Personnel', 'Equipment', 'Services', 'Infrastructure', 'Operations']
    
    # Generate data
    data = []
    departments = ['Treasury', 'Defense', 'Education', 'Health']
    
    for dept in departments:
        base_amount = np.random.randint(10000, 100000)
        for date in dates:
            for category in categories:
                amount = base_amount + np.random.normal(0, base_amount * 0.1)
                data.append({
                    'department_id': dept,
                    'date': date,
                    'category': category,
                    'amount': max(0, amount),
                    'transaction_id': np.random.randint(10000, 99999)
                })
    
    df = pd.DataFrame(data)
    
    # Create SQLite database
    conn = sqlite3.connect('government_spending.db')
    df.to_sql('department_expenses', conn, if_exists='replace', index=False)
    conn.close()
    
    return "Sample data generated successfully!"

if __name__ == "__main__":
    generate_sample_data()