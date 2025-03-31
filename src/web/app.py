import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import os
from pathlib import Path

# Import our savings calculator
from src.analysis.savings_calculator import SavingsCalculator

# Set page config
st.set_page_config(
    page_title="Electricity Savings Calculator",
    page_icon="⚡",
    layout="wide"
)

# Title and description
st.title("⚡ Electricity Savings Calculator")
st.markdown("""
This application helps you calculate potential electricity bill savings from battery storage
by analyzing historical battery performance and electricity rates.
""")

# Sidebar for file uploads and parameters
with st.sidebar:
    st.header("Input Files")
    
    # File uploaders
    tariff_file = st.file_uploader("Upload Tariff PDF", type=['pdf'])
    battery_file = st.file_uploader("Upload Battery Data CSV", type=['csv'])
    market_file = st.file_uploader("Upload Market Data CSV", type=['csv'])
    
    # Date range selection
    st.header("Analysis Period")
    start_date = st.date_input(
        "Start Date",
        value=datetime.now() - timedelta(days=30),
        max_value=datetime.now()
    )
    end_date = st.date_input(
        "End Date",
        value=datetime.now(),
        max_value=datetime.now()
    )
    
    # Calculate button
    calculate_button = st.button("Calculate Savings", type="primary")

# Main content area
if calculate_button and tariff_file and battery_file and market_file:
    try:
        # Create temporary files for uploaded data
        temp_dir = Path("temp")
        temp_dir.mkdir(exist_ok=True)
        
        # Save uploaded files
        tariff_path = temp_dir / "tariff.pdf"
        battery_path = temp_dir / "battery_data.csv"
        market_path = temp_dir / "market_data.csv"
        
        with open(tariff_path, "wb") as f:
            f.write(tariff_file.getvalue())
        with open(battery_path, "wb") as f:
            f.write(battery_file.getvalue())
        with open(market_path, "wb") as f:
            f.write(market_file.getvalue())
        
        # Initialize calculator with correct parameter names
        calculator = SavingsCalculator(
            tariff_path=str(tariff_path),
            battery_data_path=str(battery_path),
            market_data_path=str(market_path)
        )
        
        # Calculate savings for the selected month
        selected_month = datetime.combine(start_date, datetime.min.time())
        savings = calculator.calculate_monthly_savings(selected_month)
        
        # Display results
        st.header("Results")
        
        # Monthly savings display
        st.subheader(f"Savings Analysis for {savings['month']}")
        
        # Summary statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Savings", f"${savings['total_savings']:,.2f}")
        with col2:
            st.metric("Battery Operations", f"{savings['battery_operations']['total_charge']:.2f} kWh charged, {savings['battery_operations']['total_discharge']:.2f} kWh discharged")
        with col3:
            st.metric("Average Market Price", f"${savings['market_conditions']['avg_price']:.2f}/kWh")
        
        # Battery operations chart
        st.subheader("Battery Operations")
        battery_data = pd.DataFrame({
            'Charge': [savings['battery_operations']['total_charge']],
            'Discharge': [savings['battery_operations']['total_discharge']]
        })
        fig = px.bar(
            battery_data,
            title="Battery Charge/Discharge",
            labels={'value': 'Energy (kWh)', 'index': 'Operation'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Market price statistics
        st.subheader("Market Price Statistics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Maximum Price", f"${savings['market_conditions']['max_price']:.2f}/kWh")
        with col2:
            st.metric("Minimum Price", f"${savings['market_conditions']['min_price']:.2f}/kWh")
        with col3:
            st.metric("Price Standard Deviation", f"${savings['market_conditions']['price_std']:.2f}/kWh")
        
        # Clean up temporary files
        for file in [tariff_path, battery_path, market_path]:
            file.unlink()
        temp_dir.rmdir()
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.error("Please check your input files and try again.")
else:
    st.info("Please upload all required files and click 'Calculate Savings' to begin analysis.") 