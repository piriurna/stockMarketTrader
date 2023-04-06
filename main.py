from apis import AlphaVantageApi
from analysis import analyze_stock_data


def main():
    # Replace with your Alpha Vantage API key
    api_key = "YOUR_API_KEY"

    # Create an AlphaVantageApi instance
    api = AlphaVantageApi(api_key)

    # Fetch stock data for a given symbol
    symbol = "MSFT"
    stock_data = api.fetch_stock_data(symbol)

    # Perform stock analysis
    analyzed_data = analyze_stock_data(stock_data)

    # Print the analyzed stock data
    print(analyzed_data)


if __name__ == "__main__":
    main()
