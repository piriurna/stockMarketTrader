import sys
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow
from analysis.stock_analysis import analyze_stock_data
from apis import AlphaVantageApi
import os

API_KEY = os.environ.get("ALPHA_VANTAGE_API_KEY")


def main():
    api = AlphaVantageApi(API_KEY)
    stock_symbol = "MSFT"
    stock_data = api.fetch_stock_data(stock_symbol)

    # Save the raw stock data to a CSV file
    raw_data_csv_file = os.path.join("data", f"{stock_symbol}_raw.csv")
    stock_data.to_csv(raw_data_csv_file)

    analyzed_data, figures = analyze_stock_data(stock_data)

    def refresh_callback(symbol):
        new_stock_data = api.fetch_stock_data(symbol)
        _, new_figures = analyze_stock_data(new_stock_data)

        # Save the raw stock data to a CSV file
        new_stock_data.to_csv(os.path.join("data", f"{symbol.upper()}_raw.csv"))

        return new_figures

    main_window = MainWindow(figures, refresh_callback)
    app = QApplication(sys.argv)
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
