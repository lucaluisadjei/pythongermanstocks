import streamlit as st

# ─── Page Config ─────────────────────────────────────────────
st.set_page_config(page_title="Home - FinPulse", layout="wide")

# ─── Custom Styling ──────────────────────────────────────────
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: 'Source Sans Pro', sans-serif !important;
    }
    h1 {
        font-size: 60px !important;
        font-weight: 900 !important;
        color: #e0e0e0 !important;
        margin-bottom: 5px !important;
    }
    h2, h3 {
        color: #00B4D8 !important;
        font-weight: 700 !important;
    }
    .stMarkdown {
        font-size: 20px;
        color: #e0e0e0;
    }
    .stButton>button {
        font-size: 18px;
        border-radius: 12px;
        padding: 10px 20px;
        background-color: #00B4D8;
        color: white;
        border: none;
    }
    .stButton>button:hover {
        background-color: #0077b6;
    }
    .key-feature {
        background-color: #1c1c1c;
        border: 1px solid #444;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        font-size: 18px;
        text-align: center;
        color: #e0e0e0;
    }
    </style>
""", unsafe_allow_html=True)

# ─── Header ─────────────────────────────────────────────────
st.markdown("<h1>📊 FinPulse</h1>", unsafe_allow_html=True)
st.markdown("""
    <h3 style='margin-top: 0px; color: #bbb;'>AI-powered insights for your daily trading decisions.</h3>
""", unsafe_allow_html=True)

st.markdown("""
Welcome to **FinPulse**, your AI-driven trading assistant.  
This platform provides **daily trading signals** for selected German stocks using machine learning models trained on historical data.  
Built with financial data from **SimFin**, updated daily for smarter decisions.
""")

st.divider()

# ─── Key Features ───────────────────────────────────────────
st.markdown("## 🔍 Key Features")
col1, col2 = st.columns(2)
with col1:
    st.markdown("<div class='key-feature'>📈 Daily trading signals</div>", unsafe_allow_html=True)
    st.markdown("<div class='key-feature'>🤖 Predictions powered by ML</div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div class='key-feature'>🧠 Simple strategy suggestions</div>", unsafe_allow_html=True)
    st.markdown("<div class='key-feature'>🏭 Sector-specific market insights</div>", unsafe_allow_html=True)

# ─── Expander: How to Use ───────────────────────────────────
with st.expander("📘 How to use this app"):
    st.markdown("""
- Navigate to **German Stocks** to view daily insights by ticker.
- Visit **sector pages** to explore trends across industries.
- Use our **risk-based recommendations** to guide your trades.
    """)

st.divider()

# ─── About Section ──────────────────────────────────────────
st.markdown("## 👨‍💻 About Us")
st.markdown("""
FinPulse is developed by **Group 10** as part of an AI-driven financial project.  
Our mission is to make **smart trading** accessible to everyone.
""")
