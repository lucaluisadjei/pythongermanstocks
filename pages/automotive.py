import streamlit as st
import plotly.express as px
import pandas as pd
from utils.plot_functions import get_stock_price_chart
st.set_page_config(page_title="Automotive Stocks", layout="wide")

# Custom Styling
st.markdown("""
    <style>
        .big-title {
            font-size:56px;
            font-weight:bold;
            color: #FF4B4B;
        }
        .stButton>button {
            background-color: #FF4B4B !important;
            color: white !important;
            font-size: 16px !important;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-title">🚗 Automotive Sector - Live Trading</p>', unsafe_allow_html=True)

# Columns for structured layout
col1, col2 = st.columns([1, 3])

with col1:
    start_date = st.date_input("Start Date", pd.to_datetime("2023-01-01"))
    end_date = st.date_input("End Date", pd.to_datetime("2023-12-31"))
    tickers = st.multiselect("Select Tickers", ['MBG.DE', 'BMW.DE', 'VOW.DE'], default=['MBG.DE', 'BMW.DE'])

# Fetch and plot stock prices
if tickers:
    fig = get_stock_price_chart(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), tickers)

    if fig:
        st.plotly_chart(fig)
    else:
        st.warning("No data available for the selected tickers and date range.")
else:
    st.info("Please select at least one ticker.")

st.button("🔍 Get Prediction")

