import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.lstm_predictor import StockPredictor
from datetime import timedelta

# ─── Styling ───────────────────────────────────────────────
st.set_page_config(page_title="Automotive Sector Analysis", layout="wide")

st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: 'Source Sans Pro', sans-serif !important;
    }
    .arrow-up {
        animation: wiggle-up 1s infinite;
    }
    .arrow-down {
        animation: wiggle-down 1s infinite;
    }
    @keyframes wiggle-up {
        0% { transform: translateY(0); }
        50% { transform: translateY(-3px); }
        100% { transform: translateY(0); }
    }
    @keyframes wiggle-down {
        0% { transform: translateY(0); }
        50% { transform: translateY(3px); }
        100% { transform: translateY(0); }
    }
    </style>
""", unsafe_allow_html=True)

# ─── Title ──────────────────────────────────────────────────
st.markdown("""
    <h1 style='
        font-size: 48px;
        color: #e0e0e0;
        font-family: "Source Sans Pro", sans-serif;
        margin-bottom: 10px;
    '>Pharmaceutical Sector Analysis ⚕️</h1>
""", unsafe_allow_html=True)

# ─── Load Data ──────────────────────────────────────────────
df = pd.read_csv("utils/data/processed/de_share_prices_processed.csv")
df['Date'] = pd.to_datetime(df['Date'])

tickers = ['BAYN.DE', 'FRE.DE']
filtered_df = df[df['Ticker'].isin(tickers)]

# ─── Time Filter ────────────────────────────────────────────
time_filter = st.selectbox("Select Time Range", ["Daily (default)", "Last 5 Days", "Last Month", "Last Year", "All Time"])

if time_filter == "Daily (default)":
    sector_df = filtered_df.groupby('Ticker').apply(lambda x: x.tail(2)).reset_index(drop=True)
elif time_filter == "Last 5 Days":
    sector_df = filtered_df.groupby('Ticker').apply(lambda x: x.tail(5)).reset_index(drop=True)
elif time_filter == "Last Month":
    cutoff = df['Date'].max() - pd.Timedelta(days=30)
    sector_df = filtered_df[filtered_df['Date'] >= cutoff]
elif time_filter == "Last Year":
    cutoff = df['Date'].max() - pd.Timedelta(days=365)
    sector_df = filtered_df[filtered_df['Date'] >= cutoff]
else:  # All Time
    sector_df = filtered_df.copy()

# ─── Sector Metric Card ─────────────────────────────────────
latest_dates = sector_df.groupby('Ticker')['Date'].max().reset_index()
latest_vals = pd.merge(sector_df, latest_dates, on=['Ticker', 'Date'], how='inner')
latest_sum = latest_vals['Close'].sum()

if time_filter == "Daily (default)" and len(sector_df) >= 2 * len(tickers):
    prev_vals = sector_df.groupby('Ticker').apply(lambda x: x.iloc[-2]).reset_index(drop=True)
else:
    prev_vals = sector_df.groupby('Ticker').first().reset_index()

prev_sum = prev_vals['Close'].sum()
sector_pct = ((latest_sum - prev_sum) / prev_sum) * 100
arrow = "🡅" if sector_pct >= 0 else "🡇"
color = "#00FF00" if sector_pct >= 0 else "#FF4C4C"
arrow_class = "arrow-up" if sector_pct >= 0 else "arrow-down"

start_date = sector_df['Date'].min().date()
end_date = sector_df['Date'].max().date()

st.markdown(f"""
    <div style="
        background-color: #1c1c1c;
        border: 1px solid #444;
        border-radius: 10px;
        padding: 20px;
        font-size: 22px;
        color: #e0e0e0;
        text-align: center;
        margin-bottom: 20px;
        font-family: 'Source Sans Pro', sans-serif;
    ">
        <b>{start_date} → {end_date}</b><br>
        Total Market Movement: <span style='color:{color}; font-weight:bold;' class='{arrow_class}'>{arrow} {sector_pct:.2f}%</span>
    </div>
""", unsafe_allow_html=True)

# ─── Line Chart ─────────────────────────────────────────────
fig = go.Figure()
for ticker in tickers:
    ticker_df = sector_df[sector_df['Ticker'] == ticker]
    fig.add_trace(go.Scatter(x=ticker_df['Date'], y=ticker_df['Close'], mode='lines', name=ticker))

fig.update_layout(title="Sector Time Series", xaxis_title="Date", yaxis_title="Close ($)")
st.plotly_chart(fig, use_container_width=True)

# ─── Sidebar Risk Preference ────────────────────────────────
st.sidebar.header("Risk Preference")
risk_profile = st.sidebar.selectbox("Choose your risk profile", ["High", "Low"])

# ─── Predict & Recommend ────────────────────────────────────
if st.button("🚀 Run Daytrading Predictions"):
    st.subheader("2-Day Forecast & Recommendation")
    for ticker in tickers:
        ticker_df = filtered_df[filtered_df['Ticker'] == ticker].sort_values('Date')
        model_path = f"utils/models/lstm_model_{ticker}.h5"
        predictor = StockPredictor(model_path, ticker_df)

        last_actual, predicted_closes = predictor.get_last_actual_and_predictions()
        recommendation = predictor.recommend(risk_profile)

        future_dates = [ticker_df['Date'].iloc[-1] + timedelta(days=i+1) for i in range(2)]
        change = ((predicted_closes[1] - predicted_closes[0]) / predicted_closes[0]) * 100
        arrow = "🡅" if change >= 0 else "🡇"
        color = "#00FF00" if change >= 0 else "#FF4C4C"
        arrow_class = "arrow-up" if change >= 0 else "arrow-down"

        # Company name for display
        company_name = ticker_df['Company Name'].iloc[0]
        st.markdown(f"""
            <h3 style='
                font-size: 28px;
                color: #e0e0e0;
                font-family: "Source Sans Pro", sans-serif;
                margin-top: 40px;
            '>{company_name}</h3>
        """, unsafe_allow_html=True)

        # ── Prediction Cards ──
        col1, col2, col3 = st.columns(3)

        col1.markdown(f"""
            <div style="
                background-color: #1c1c1c;
                border: 1px solid #444;
                border-radius: 10px;
                padding: 16px;
                font-size: 18px;
                color: #e0e0e0;
                text-align: center;
            ">
                <b>{future_dates[0].date()}</b><br>{predicted_closes[0]:.2f} $
            </div>
        """, unsafe_allow_html=True)

        col2.markdown(f"""
            <div style="
                background-color: #1c1c1c;
                border: 1px solid #444;
                border-radius: 10px;
                padding: 16px;
                font-size: 18px;
                color: #e0e0e0;
                text-align: center;
            ">
                <b>{future_dates[1].date()}</b><br>{predicted_closes[1]:.2f} $
            </div>
        """, unsafe_allow_html=True)

        col3.markdown(f"""
            <div style="
                background-color: #1c1c1c;
                border: 1px solid #444;
                border-radius: 10px;
                padding: 16px;
                font-size: 18px;
                text-align: center;
                color: {color};
            ">
                <b>Change</b><br><span class='{arrow_class}'>{arrow} {change:.2f}%</span>
            </div>
        """, unsafe_allow_html=True)

        # ── Recommendation ──
        st.markdown(f"""
            <div style="
                background-color: #1c1c1c;
                border: 2px solid #00ffcc;
                border-radius: 10px;
                padding: 20px;
                margin-top: 10px;
                font-size: 20px;
                color: #e0e0e0;
                font-weight: bold;
                text-align: center;
            ">
                 <b>Recommendation:</b> <span style="color:#00ffcc;">{recommendation}</span>
            </div>
        """, unsafe_allow_html=True)

        # ── Prediction Plot ──
        last_5 = ticker_df[['Date', 'Close']].iloc[-5:].copy()
        pred_df_plot = pd.DataFrame({'Date': future_dates, 'Close': predicted_closes})
        combined = pd.concat([last_5, pred_df_plot], ignore_index=True)

        fig_pred = go.Figure()
        fig_pred.add_trace(go.Scatter(x=combined['Date'], y=combined['Close'], mode='lines+markers', name='Close'))
        fig_pred.add_trace(go.Scatter(x=pred_df_plot['Date'], y=pred_df_plot['Close'],
                                      mode='lines+markers', marker=dict(color='red'), name='Predicted'))

        fig_pred.update_layout(title=f"{company_name}: Last 5 Days + 2-Day Forecast", xaxis_title="Date", yaxis_title="Close ($)")
        st.plotly_chart(fig_pred, use_container_width=True)
