import warnings
warnings.filterwarnings("ignore")

import json

import numpy as np
import pandas as pd

import plotly.express as px

import simfin as sf

from simfin.names import *

import os
from time import sleep
from dotenv import load_dotenv
import datetime
import requests
import json
from functools import reduce

class SimFinAPI:
    def __init__(self):
        self.__load_dotenv()
        self.__token = os.getenv("API_KEY")
        sf.set_api_key(self.__token)
        sf.set_data_dir('~/simfin_data/')

    def __load_dotenv(self):
        load_dotenv()

    def get_companies(self, market='de'):
        try:
            # Load company data for the specified market
            df_companies = sf.load_companies(market=market)
            df_companies = df_companies.reset_index()  # Reset index to access 'Ticker'
            return df_companies[['SimFinId', 'Ticker']]
        except Exception as e:
            print(f"Error fetching company data: {e}")
            return None

    def get_share_prices(self, market='de', variant='daily', tickers=None, start_date=None, end_date=None):
        try:
            # Load share prices for the specified market and variant
            df_prices = sf.load_shareprices(market=market, variant=variant)
            
           # Filter for the specified tickers
            if tickers:
                df_prices = df_prices.loc[df_prices.index.get_level_values('Ticker').isin(tickers)]
            
            # Convert index to datetime if not already in datetime format
            df_prices.index = pd.to_datetime(df_prices.index.get_level_values('Date'))
            
            # Filter by date range if provided
            if start_date:
                start_date = pd.to_datetime(start_date)
                df_prices = df_prices[df_prices.index >= start_date]
            if end_date:
                end_date = pd.to_datetime(end_date)
                df_prices = df_prices[df_prices.index <= end_date]


            # Load company data to map SimFinId to Ticker
            df_companies = self.get_companies(market)
            df_prices = df_prices.reset_index() 
            if df_companies is not None:
                df_prices = df_prices.merge(df_companies, on='SimFinId', how='left')
            
            return df_prices
        except Exception as e:
            print(f"Error fetching share prices: {e}")
            return None

# Create an instance of the SimFinAPI class
simfin_api = SimFinAPI()

# Define the start date, end date and tickers
start_date = '2023-01-01'
end_date = '2023-12-31'
tickers = ['MBG.DE', 'BMW.DE', 'VOW.DE']

# Get share prices for the tickers
ticker_prices = simfin_api.get_share_prices(tickers=tickers, start_date=start_date, end_date=end_date)