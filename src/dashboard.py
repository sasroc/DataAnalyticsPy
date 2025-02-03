# src/dashboard.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
from data_loader import DataLoader
from preprocessor import DataPreprocessor
from analyzer import DataAnalyzer
from visualizer import DataVisualizer

class Dashboard:
    def __init__(self):
        self.loader = DataLoader("sqlite:///government_spending.db")  # We'll use SQLite for demo
        self.preprocessor = DataPreprocessor()
        self.analyzer = DataAnalyzer()
        self.visualizer = DataVisualizer()

    def run(self):
        st.set_page_config(page_title="Government Spending Analytics", layout="wide")
        
        st.title("📊 Government Spending Analytics Dashboard")
        
        # Sidebar filters
        st.sidebar.header("Filters")
        
        # Demo data for department selection
        departments = ["Treasury", "Defense", "Education", "Health"]
        selected_dept = st.sidebar.selectbox("Select Department", departments)
        
        # Date range selection
        date_range = st.sidebar.date_input(
            "Select Date Range",
            value=(datetime.now() - timedelta(days=365), datetime.now())
        )
        
        # Load and process data
        try:
            data = self.loader.load_department_data(selected_dept)
            processed_data = self.preprocessor.clean_financial_data(data)
            
            # Main dashboard area
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("💰 Spending Overview")
                metrics = self.analyzer.calculate_spending_metrics(processed_data)
                
                # Display key metrics
                st.metric(
                    "Total Spending", 
                    f"${metrics['total_spend']:,.2f}",
                    f"{metrics['trend']['slope']:,.2f}"
                )
                
                st.metric(
                    "Monthly Average", 
                    f"${metrics['average_monthly_spend']:,.2f}"
                )
            
            with col2:
                st.subheader("📈 Trend Analysis")
                trend_direction = metrics['trend']['trend_direction']
                st.write(f"Spending trend is currently **{trend_direction}**")
                
                # Prediction
                predictions = self.analyzer.predict_future_spending(processed_data)
                st.write("3-Month Spending Forecast:")
                st.line_chart(predictions)
            
            # Detailed visualizations
            st.subheader("📊 Detailed Analysis")
            tabs = st.tabs(["Time Series", "Categories", "Forecast"])
            
            with tabs[0]:
                figures = self.visualizer.create_spending_dashboard(
                    processed_data, 
                    {"predictions": predictions}
                )
                st.plotly_chart(figures['spending_over_time'], use_container_width=True)
            
            with tabs[1]:
                st.plotly_chart(figures['category_breakdown'], use_container_width=True)
            
            with tabs[2]:
                st.plotly_chart(figures['spending_forecast'], use_container_width=True)
            
            # Data table
            st.subheader("🗃️ Detailed Data")
            st.dataframe(
                processed_data.sort_values('date', ascending=False),
                use_container_width=True
            )
            
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")

if __name__ == "__main__":
    dashboard = Dashboard()
    dashboard.run()