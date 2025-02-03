import plotly.express as px
import plotly.graph_objects as go
from typing import Dict

class DataVisualizer:
    def create_spending_dashboard(self, df: pd.DataFrame, metrics: Dict) -> Dict:
        """Create a comprehensive spending dashboard."""
        figures = {
            'spending_over_time': self._create_time_series(df),
            'category_breakdown': self._create_category_breakdown(df),
            'spending_forecast': self._create_forecast_plot(
                df, metrics.get('predictions', [])
            )
        }
        return figures
    
    def _create_time_series(self, df: pd.DataFrame) -> go.Figure:
        """Create time series plot of spending."""
        fig = px.line(
            df,
            x='date',
            y='amount',
            title='Spending Over Time',
            labels={'amount': 'Amount ($)', 'date': 'Date'}
        )
        return fig
    
    def _create_category_breakdown(self, df: pd.DataFrame) -> go.Figure:
        """Create category breakdown visualization."""
        category_totals = df.groupby('category')['amount'].sum()
        fig = px.pie(
            values=category_totals.values,
            names=category_totals.index,
            title='Spending by Category'
        )
        return fig
    
    def _create_forecast_plot(
        self,
        df: pd.DataFrame,
        predictions: pd.Series
    ) -> go.Figure:
        """Create forecast visualization."""
        fig = go.Figure()
        
        # Historical data
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['amount'],
            name='Historical'
        ))
        
        # Predictions
        if len(predictions) > 0:
            fig.add_trace(go.Scatter(
                x=predictions.index.astype(str),
                y=predictions.values,
                name='Forecast',
                line=dict(dash='dash')
            ))
        
        fig.update_layout(title='Spending Forecast')
        return fig