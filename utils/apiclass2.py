import os
import pandas as pd
from dotenv import load_dotenv
import simfin as sf

class SimFinAPI:
    """
    A class to interact with the SimFin API and download financial data for processing.
    """

    def __init__(self):  # ✅ Fixed constructor name
        self.__load_dotenv()
        self.__token = os.getenv("API_KEY")
        sf.set_api_key(self.__token)
        sf.set_data_dir(r'C:\Users\Paulm\Desktop\My Files\IE\Courses\Python For data Analysis 2\PyGroupProject\utils\data')
        
        # ✅ Fixed different file paths
        self.companies_path = r'C:\Users\Paulm\Desktop\My Files\IE\Courses\Python For data Analysis 2\PyGroupProject\utils\data\raw\de_companies_data_RAW.csv'
        self.share_prices_path = r'C:\Users\Paulm\Desktop\My Files\IE\Courses\Python For data Analysis 2\PyGroupProject\utils\data\raw\de_share_prices_RAW.csv'

    def __load_dotenv(self):
        load_dotenv() 

    def get_companies(self, market='de'):
        try:
            df_companies = sf.load_companies(market=market)
            df_companies = df_companies.reset_index()
            return df_companies
        except Exception as e:
            print(f"Error fetching company data: {e}")
            return None

    def get_share_prices(self, market='de', variant='daily'):
        try:
            df_prices = sf.load_shareprices(market=market, variant=variant)
            df_prices = df_prices.reset_index()
            return df_prices
        except Exception as e:
            print(f"Error fetching share prices: {e}")
            return None

    def process_and_save_data(self, companies, prices):
        if companies is None or prices is None:
            print("Data is missing. Skipping processing.")
            return

        updated_prices = prices.merge(companies[['Ticker','Company Name']], on="Ticker", how="left")
        updated_prices.to_csv(self.share_prices_path, index=False) 
        companies.to_csv(self.companies_path, index=False)
        print(f"Updated files saved: {self.companies_path} and {self.share_prices_path}")

# ✅ Run the code
if __name__ == "__main__":
    simfin_api = SimFinAPI()
    companies = simfin_api.get_companies()
    prices = simfin_api.get_share_prices() 
    simfin_api.process_and_save_data(companies, prices)
