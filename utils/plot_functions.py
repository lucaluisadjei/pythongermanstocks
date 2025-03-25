import plotly.express as px
import pandas as pd
from utils.apiclass import SimFinAPI  # Correct import

def get_stock_price_chart(start_date, end_date, tickers):
    """
    Fetches stock prices using SimFinAPI and generates a Plotly chart.

    Parameters:
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.
        tickers (list): List of stock ticker symbols.

    Returns:
        fig: A Plotly figure object.
    """
    # Create an instance of SimFinAPI
    simfin_api = SimFinAPI()
    
    # Fetch stock prices
    df_prices = simfin_api.get_share_prices(tickers=tickers, start_date=start_date, end_date=end_date)

    # Check if data is available
    if df_prices is not None and not df_prices.empty:
        # Generate Plotly line chart
        fig = px.line(df_prices, x='Date', y='Close', color='Ticker',
                      title="Stock Prices Over Time",
                      labels={"Close": "Stock Price (EUR)", "Date": "Date", "Ticker": "Company"})
        return fig
    else:
        return None

def plot_time_series(df, ticker):
    fig = px.line(
        df,
        x='Date',
        y='Close',
        title=f"{ticker} Share Price Over Time",
        labels={'Close': 'Closing Price (EUR)', 'Date': 'Date'}
    )
    fig.update_traces(mode="lines+markers")
    fig.update_layout(margin=dict(t=50, b=40))
    return fig
