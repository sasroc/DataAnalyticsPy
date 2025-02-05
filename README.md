# Government Spending Analytics Dashboard

A Python-based analytics platform for visualizing and analyzing government department spending patterns. Built to enhance transparency and efficiency in public sector financial management.

## Features
- Interactive Streamlit dashboard for real-time spending analysis
- Multi-department spending comparisons
- Trend analysis and forecasting
- Category-wise spending breakdown
- Automated data preprocessing pipeline
- Interactive data visualization using Plotly
- SQL database integration for robust data storage

## Installation

1. Clone repository:
```bash
git clone https://github.com/your-username/DataAnalyticsPy.git
cd DataAnalyticsPy
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure
```
src/
├── dashboard.py     # Main Streamlit dashboard
├── data_loader.py   # Database connectivity and data retrieval
├── preprocessor.py  # Data cleaning and preprocessing
├── analyzer.py      # Statistical analysis and forecasting
├── visualizer.py    # Data visualization components
└── sample_data.py   # Sample data generation for testing
```

## Usage

1. Generate sample data:
```bash
python src/sample_data.py
```

2. Run the dashboard:
```bash
streamlit run src/dashboard.py
```

## Key Components

### Data Loader
Handles database connections and data retrieval:
```python
from src.data_loader import DataLoader
loader = DataLoader("sqlite:///government_spending.db")
data = loader.load_department_data("Treasury")
```

### Analytics Dashboard
Features:
- Department-wise spending analysis
- Dynamic date range filtering
- Spending trends and forecasts
- Category breakdown visualizations
- Detailed transaction view

## Contributing
Pull requests welcome. For major changes, please open an issue first.

## License
MIT
