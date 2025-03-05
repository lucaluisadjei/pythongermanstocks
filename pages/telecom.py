import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Telecom Stocks", layout="wide")

# Custom Styling
st.markdown("""
    <style>
        .big-title {
            font-size:56px;
            font-weight:bold;
            color: #0073e6;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-title">📡 Telecom Sector - Live Trading</p>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("Select a Company")
    telecom_stocks = {"1&1": "1U", "Telekom": "DTE"}
    selected_stock = st.selectbox("Choose a stock:", list(telecom_stocks.keys()))

with col2:
    st.subheader(f"📊 {selected_stock} Stock Price Chart")

    df = pd.DataFrame({
        "Date": pd.date_range(start="2024-01-01", periods=30),
        "Price": (pd.Series(range(30)) * 1.8 + 50).tolist()
    })

    fig = px.line(df, x="Date", y="Price", title=f"{selected_stock} Stock Price History")
    st.plotly_chart(fig, use_container_width=True)

st.button("🔍 Get Prediction")

""""""