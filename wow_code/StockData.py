import pandas as pd
import FinanceDataReader as fdr
from GlobalFunction import get_config_data

def get_stock_diff_data():
    config = get_config_data()

    start_day = config['StockData']['start_day']
    end_day = config['StockData']['end_day']
    number_of_stock = config['StockData']['number_of_stock']
    save_path = config['StockData']['save_path']

    stocks = fdr.StockListing('NASDAQ')
    stock_code_list = stocks['Symbol'][0:number_of_stock].tolist()

    for stock_code in stock_code_list:
        raw_stock_data = fdr.DataReader(stock_code, start_day, end_day)
        stock_diff = raw_stock_data.diff()
        stock_diff = stock_diff.dropna()
        stock_diff.to_csv(f'{save_path}/{stock_code}_{start_day}_{end_day}_diff.csv', index=True)
        print(f"'{stock_code}({start_day} ~ {end_day})' diff data is downloaded successfully!")
if __name__ == "__main__":
    get_stock_diff_data()