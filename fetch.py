import sys

import pandas as pd
from PyQt5.QtWidgets import QApplication

from analysis import Indicators
from main_window import MainWindow
from analysis.stock_analysis import analyze_stock_data, analyze_combined_stock_data
from apis import AlphaVantageApi
import os

API_KEY = os.environ.get("ALPHA_VANTAGE_API_KEY")
RAW_PATH = "data/raw"
ANALYZED_PATH = "data/analyzed"


def main():
    api = AlphaVantageApi(API_KEY)
    stock_symbols = ["MSFT", "NVDA", "ZM", "TSLA", "NKE", "NFLX", "MCD", "KO", "JPM", "INTC", "HD", "GS", "FB", "CSCO", "AMZN", "AAPL", "WMT", "VZ", "UNH", "TGT", "SBUX", "PYPL", "PEP", "NEM", "MA", "LOW", "IBM", "GE", "EBAY", "DIS","CVS","COST","CLX","CAT","BAC","ABT","XOM","WFC","TWTR","SQ","SNAP","SHOP","ROKU","QCOM","PFE","ORCL","MRNA","MMM","LUV","JNJ", "INTC"]
    all_stock_datas = {}
    for stock_symbol in sorted(stock_symbols):
        stock_data = None
        try:
            stock_data = pd.read_json(os.path.join(RAW_PATH, f"{stock_symbol.upper()}_raw.json"))
        except FileNotFoundError:
            try:
                stock_data = api.fetch_stock_data(stock_symbol)
                stock_data.to_json(os.path.join(RAW_PATH, f"{stock_symbol.upper()}_raw.json"))
            except KeyError:
                print(f"Could not find stock data for {stock_symbol}")
                continue
        finally:
            if stock_data is not None:
                all_stock_datas[stock_symbol] = stock_data

    all_stock_datas = dict(sorted(all_stock_datas.items(), key=lambda x: max(x[1]["4. close"]), reverse=True))

    analyzed_data, figures = analyze_combined_stock_data(all_stock_datas)
    for stock_symbol in all_stock_datas.keys():
        analyzed_data[stock_symbol].to_json(os.path.join(f"{ANALYZED_PATH}/json", f"{stock_symbol.upper()}_analyzed.json"))
        analyzed_data[stock_symbol].to_csv(os.path.join(f"{ANALYZED_PATH}/csv", f"{stock_symbol.upper()}_analyzed.csv"))

    def refresh_callback(symbols):
        print("Refreshing because checkbox pressed")
        new_stock_datas = {}
        for symbol in all_stock_datas.keys():
            if symbol in symbols:
                new_stock_datas[symbol] = all_stock_datas[symbol]

        _, new_figures = analyze_combined_stock_data(new_stock_datas)
        return new_figures

    main_window = MainWindow(figures, refresh_callback, all_stock_datas.keys(), False)

    app = QApplication(sys.argv)
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
