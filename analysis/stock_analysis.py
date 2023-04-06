import pandas as pd
import matplotlib.pyplot as plt


def calculate_moving_average(data, window_size):
    return data.rolling(window=window_size).mean()


def calculate_return(data):
    return data.pct_change()


def plot_stock_data(data, title, ylabel):
    plt.figure(figsize=(10, 5))
    plt.plot(data)
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel(ylabel)
    plt.grid()
    plt.show()


def analyze_stock_data(stock_data):
    # Calculate the moving averages
    stock_data['SMA20'] = calculate_moving_average(stock_data['4. close'], 20)
    stock_data['SMA50'] = calculate_moving_average(stock_data['4. close'], 50)

    # Calculate the daily returns
    stock_data['Return'] = calculate_return(stock_data['4. close'])

    # Plot the stock data
    plot_stock_data(stock_data['4. close'], 'Stock Price', 'Price')
    plot_stock_data(stock_data[['SMA20', 'SMA50']], 'Moving Averages', 'Price')
    plot_stock_data(stock_data['Return'], 'Daily Returns', 'Return')

    return stock_data
