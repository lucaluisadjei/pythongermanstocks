import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="Portfolio Snapshot - FinPulse", layout="wide")

# Global font and style
st.markdown("""
    <style>
    html, body, [class*="css"]  {
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

# Title
st.markdown("""
    <h1 style='
        font-size: 48px;
        color: #e0e0e0;
        font-family: "Source Sans Pro", sans-serif;
        margin-bottom: 10px;
    '>German Stocks</h1>
""", unsafe_allow_html=True)

# Load data
df = pd.read_csv("utils/data/processed/de_share_prices_processed.csv")
df_info = pd.read_csv("utils/data/raw/de_companies_data_RAW.csv")
df['Date'] = pd.to_datetime(df['Date'])

# Company dropdown
company_names = df['Company Name'].dropna().unique()
selected_company = st.selectbox("Select a Company", sorted(company_names))

# Filter data by selected company
company_df = df[df['Company Name'] == selected_company].sort_values("Date")

# Time filter selection
filter_option = st.selectbox("Select Time Range", ["Daily (default)", "Last 5 Days", "Last Month", "Last Year", "All Time"])

# Filter logic
if filter_option == "Daily (default)":
    filtered_df = company_df.tail(2)
elif filter_option == "Last 5 Days":
    filtered_df = company_df.tail(5)
elif filter_option == "Last Month":
    one_month_ago = company_df['Date'].max() - pd.Timedelta(days=30)
    filtered_df = company_df[company_df['Date'] >= one_month_ago]
elif filter_option == "Last Year":
    one_year_ago = company_df['Date'].max() - pd.Timedelta(days=365)
    filtered_df = company_df[company_df['Date'] >= one_year_ago]
else:  # All Time
    filtered_df = company_df.copy()

# Get latest and reference for % change
latest_row = filtered_df.iloc[-1]
reference_row = filtered_df.iloc[-2] if len(filtered_df) > 1 else filtered_df.iloc[0]

# Key stats
ticker = latest_row['Ticker']
latest_date = latest_row['Date'].date()
latest_open = latest_row['Open']
latest_close = latest_row['Close']
ref_close = reference_row['Close']
pct_change = ((latest_close - ref_close) / ref_close) * 100
arrow = "🡅" if pct_change >= 0 else "🡇"
color = "#00FF00" if pct_change >= 0 else "#FF4C4C"
arrow_class = "arrow-up" if pct_change >= 0 else "arrow-down"

# Snapshot
st.subheader(f"📊 Snapshot for {selected_company}")

# Stat cards
col1, col2, col3, col4, col5 = st.columns(5)

def stat_card(title, value, color_override=None):
    color_style = f"color:{color_override}; font-weight:bold;" if color_override else "color: #e0e0e0;"
    return f"""
        <div style="
            background-color: #1c1c1c;
            border: 1px solid #444;
            border-radius: 10px;
            padding: 16px;
            font-size: 20px;
            text-align: center;
            font-family: 'Source Sans Pro', sans-serif;
            {color_style}
        ">
            <b>{title}</b><br>{value}
        </div>
    """

col1.markdown(stat_card("Ticker", ticker), unsafe_allow_html=True)
col2.markdown(stat_card("Date", latest_date), unsafe_allow_html=True)
col3.markdown(stat_card("Open ($)", f"{latest_open:.2f}"), unsafe_allow_html=True)
col4.markdown(stat_card("Close ($)", f"{latest_close:.2f}"), unsafe_allow_html=True)

start_date = filtered_df['Date'].min().date()
end_date = filtered_df['Date'].max().date()

col5.markdown(f"""
    <div style="
        background-color: #1c1c1c;
        border: 1px solid #444;
        border-radius: 10px;
        padding: 16px;
        font-size: 20px;
        text-align: center;
        color: #e0e0e0;
        font-family: 'Source Sans Pro', sans-serif;
    ">
        <b>Change</b><br>
        <span style='color:{color}; font-weight:bold;' class='{arrow_class}'>{arrow} {pct_change:.2f}%</span><br>
        <span style="font-size: 14px; color: #aaa;">{start_date} → {end_date}</span>
    </div>
""", unsafe_allow_html=True)

# Chart
fig = px.line(filtered_df, x='Date', y='Close',
              labels={'value': 'Price ($)', 'Date': 'Date'},
              title=f"{selected_company} - Close Prices Over Time")
st.plotly_chart(fig, use_container_width=True)

# Company description
summary = df_info[df_info['Company Name'] == selected_company]['Business Summary']
summary_text = summary.values[0] if not summary.empty else "No description available."

st.markdown("### 🏢 Company Description")

st.markdown(f"""
    <div style="
        background-color: #1c1c1c;
        border: 1px solid #444;
        border-radius: 10px;
        padding: 20px;
        color: #e0e0e0;
        margin-top: 10px;
        font-size: 20px;
        font-family: 'Source Sans Pro', sans-serif;
    ">
        {summary_text}
    </div>
""", unsafe_allow_html=True)

