import streamlit as st
import plotly.express as px
import pandas as pd

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
    st.subheader("Select a Company")
    automotive_stocks = {"Volkswagen": "VW", "BMW": "BMW", "Mercedes Group": "MBG"}
    selected_stock = st.selectbox("Choose a stock:", list(automotive_stocks.keys()))

with col2:
    st.subheader(f"📊 {selected_stock} Stock Price Chart")

    # Mock Data (Replace with API Data)
    df = pd.DataFrame({
        "Date": pd.date_range(start="2024-01-01", periods=30),
        "Price": (pd.Series(range(30)) * 2.5 + 100).tolist()
    })

    fig = px.line(df, x="Date", y="Price", title=f"{selected_stock} Stock Price History")
    st.plotly_chart(fig, use_container_width=True)

st.button("🔍 Get Prediction")

