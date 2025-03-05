import streamlit as st
import pandas as pd

st.set_page_config(page_title="Portfolio Summary", layout="wide")
# This is Chatgpt html code for testing : 
st.markdown("""
    <style>
        .big-title {
            font-size:56px;
            font-weight:bold;
            color: #28a745;
        }
        .profit {color: #28a745; font-weight: bold;}
        .loss {color: #FF4B4B; font-weight: bold;}
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-title">💼 Portfolio Summary</p>', unsafe_allow_html=True)

#This is mine :
# Mock Portfolio Data (Replace with API Data)
portfolio = {
    "Volkswagen": {"Initial Price": 150, "Current Price": 165},
    "BMW": {"Initial Price": 80, "Current Price": 75},
    "Mercedes Group": {"Initial Price": 90, "Current Price": 95},
    "1&1": {"Initial Price": 20, "Current Price": 18},
    "Telekom": {"Initial Price": 25, "Current Price": 30},
}

# Convert to DataFrame
df = pd.DataFrame(portfolio).T
df["Change"] = df["Current Price"] - df["Initial Price"]
df["% Change"] = (df["Change"] / df["Initial Price"]) * 100

# Portfolio Gain/Loss Calculation
total_investment = df["Initial Price"].sum()
total_value = df["Current Price"].sum()
portfolio_change = total_value - total_investment
portfolio_pct_change = (portfolio_change / total_investment) * 100

#Chatgpt here cause i got confused with the code above
# Display Results
st.subheader("📈 Portfolio Performance")
st.dataframe(df.style.format({"Initial Price": "€{:.2f}", "Current Price": "€{:.2f}", "Change": "€{:.2f}", "% Change": "{:.2f}%"}))

#here also for html stuff cause the fonts were weird
# Show Portfolio Status
if portfolio_change >= 0:
    st.markdown(f"<h2 class='profit'>📈 You are UP by €{portfolio_change:.2f} ({portfolio_pct_change:.2f}%)</h2>", unsafe_allow_html=True)
else:
    st.markdown(f"<h2 class='loss'>📉 You are DOWN by €{portfolio_change:.2f} ({portfolio_pct_change:.2f}%)</h2>", unsafe_allow_html=True)

