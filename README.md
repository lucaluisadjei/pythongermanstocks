# FinPulse: Automated Daily Trading System

## Project Overview
FinPulse is an automated trading system designed to assist with short-term investment decisions in the German equity market. By integrating machine learning with real-time market data, the system generates daily trading signals—**Buy**, **Sell**, or **Hold**—based on short-term stock price forecasts and the investor’s risk profile. The system focuses on high-volume stocks in the automotive and pharmaceutical sectors, tailoring recommendations to suit low-risk or high-risk investors.

## Data Sources
The analysis uses historical daily share prices for publicly listed companies in Germany from 2019 to 2024. The selected companies represent two key sectors: **automotive** (**BMW.DE**, **MBG.DE**, **VOW.DE**) and **pharmaceuticals** (**FRE.DE**, **BAYNE.DE**), providing a balanced mix of growth and stability.

## ETL Process
The **ETL** process begins by extracting raw stock data from the **SimFin API**, focusing on historical stock prices and financial data for the selected companies. This data is cleaned by handling missing values, converting date columns to **datetime** format, and engineering features such as stock price changes. The transformed data is saved and loaded into a structured format, ready for analysis and machine learning model training.

## Modeling Methodology
Stock price forecasts are generated using the **LSTM (Long Short-Term Memory)** model, which excels at capturing long-term dependencies in time series data. While **XGBoost** was also tested, it did not perform as well as LSTM and was excluded from the final model. The models are evaluated using metrics like **MAE**, **RMSE**, and **R²**, with the **LSTM** model selected for its accuracy in predicting stock price movements.

## Trading Strategy Design
The trading strategy is based on **two-day predictions**, with recommendations to **Buy**, **Sell**, or **Hold** depending on the predicted price changes and trends. For example, a **Buy** signal is issued when both **Day 1** and **Day 2** predictions indicate an upward trend. If **Day 1** shows a rise but **Day 2** predicts a decline, the strategy checks if the predicted **Day 2** price is higher or lower than the current price (**Day 0**). **High-risk** investors may act on smaller price movements, while **low-risk** investors are advised to **Hold** in uncertain conditions.

## Application Interface - User Experience
The **Streamlit** dashboard allows users to select a stock, define their risk profile, and view two-day price forecasts. The app provides actionable trade recommendations and visualizes both historical and predicted stock prices over time. It also includes detailed information on industry behavior and stock performance.

## Important Considerations
This system is designed for **short-term forecasting** and assumes that users already hold stocks in the selected companies. External factors like macroeconomic events, news, and earnings reports are not considered in the model; only historical price data is used.

---

## 🛠 Tech Stack

- **Python 3.10+**
- **Pandas, NumPy**
- **TensorFlow / Keras**
- **XGBoost**
- **Streamlit**
- **SimFin API**
- **Matplotlib / Seaborn**

---
