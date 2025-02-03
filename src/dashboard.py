# src/dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from data_loader import DataLoader
from preprocessor import DataPreprocessor
from analyzer import DataAnalyzer
from visualizer import DataVisualizer

class Dashboard:
    def __init__(self):
        self.loader = DataLoader("sqlite:///government_spending.db")
        self.preprocessor = DataPreprocessor()
        self.analyzer = DataAnalyzer()
        self.visualizer = DataVisualizer()

    def run(self):
        st.set_page_config(page_title="Government Spending Analytics", layout="wide")
        st.title("📊 Government Spending Analytics Dashboard")
        
        # Sidebar filters
        st.sidebar.header("Filters")
        departments = ["Treasury", "Defense", "Education", "Health"]
        selected_dept = st.sidebar.selectbox("Select Department", departments)
        
        # Date range selection with default values
        default_start = datetime.now() - timedelta(days=365)
        default_end = datetime.now()
        start_date = st.sidebar.date_input("Start Date", default_start)
        end_date = st.sidebar.date_input("End Date", default_end)
        
        try:
            # Load data
            data = self.loader.load_department_data(selected_dept)
            processed_data = self.preprocessor.clean_financial_data(data)
            
            # Filter by date range
            mask = (processed_data['date'].dt.date >= start_date) & (processed_data['date'].dt.date <= end_date)
            filtered_data = processed_data.loc[mask]
            
            if filtered_data.empty:
                st.warning("No data available for selected date range")
                return
            
            # Display visualizations with filtered data
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("💰 Spending Overview")
                metrics = self.analyzer.calculate_spending_metrics(filtered_data)
                st.metric("Total Spending", f"${metrics['total_spend']:,.2f}")
                st.metric("Monthly Average", f"${metrics['average_monthly_spend']:,.2f}")
            
            with col2:
                st.subheader("📈 Trend Analysis")
                predictions = self.analyzer.predict_future_spending(filtered_data)
                st.line_chart(predictions)
            
            # Detailed visualizations
            st.subheader("📊 Detailed Analysis")
            tabs = st.tabs(["Time Series", "Categories", "Forecast"])
            
            figures = self.visualizer.create_spending_dashboard(filtered_data, {"predictions": predictions})
            
            with tabs[0]:
                st.plotly_chart(figures['spending_over_time'], use_container_width=True)
            with tabs[1]:
                st.plotly_chart(figures['category_breakdown'], use_container_width=True)
            with tabs[2]:
                st.plotly_chart(figures['spending_forecast'], use_container_width=True)
            
            # Data table
            st.subheader("🗃️ Detailed Data")
            st.dataframe(filtered_data.sort_values('date', ascending=False), use_container_width=True)
            
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")

if __name__ == "__main__":
    dashboard = Dashboard()
    dashboard.run()