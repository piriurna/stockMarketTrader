import os

import pandas as pd
import matplotlib.pyplot as plt
from .indicators import (
    simple_moving_average,
    exponential_moving_average,
    bollinger_bands,
    relative_strength_index,
    calculate_standard_deviation,
    value_at_risk, moving_average_convergence_divergence, moving_average_convergence_divergence_new,
)
from .enums import MovingAverageType, Indicators


def calculate_moving_average(data, window_size):
    return data.rolling(window=window_size).mean()


def calculate_return(data):
    return data.pct_change()


def plot_stock_data(data, title, ylabel):
    fig = plt.figure(figsize=(10, 5))

    if isinstance(data, pd.DataFrame):
        for column in data.columns:
            plt.plot(data[column], label=column)
    else:
        plt.plot(data)

    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid()

    return fig


def analyze_stock_data(stock_data, ma_type=MovingAverageType.SMA, window_size_1=20, window_size_2=50, rsi_period=14,
                       bb_period=20, var_confidence_level=0.95, symbol=""):
    # Calculate the moving averages based on the specified type and window sizes
    ma_one_name = f'MA{window_size_1}'
    ma_two_name = f'MA{window_size_2}'
    stock_data["Price"] = stock_data["4. close"]
    stock_data["4. close"] = None
    if ma_type == MovingAverageType.SMA:
        stock_data[ma_one_name] = simple_moving_average(stock_data["Price"], window_size_1)
        stock_data[ma_two_name] = simple_moving_average(stock_data["Price"], window_size_2)
    elif ma_type == MovingAverageType.EMA:
        stock_data[ma_one_name] = exponential_moving_average(stock_data["Price"], window_size_1)
        stock_data[ma_two_name] = exponential_moving_average(stock_data["Price"], window_size_2)

    # Calculate the daily returns
    stock_data['Return'] = calculate_return(stock_data["Price"])

    # Calculate Bollinger Bands
    bb_period = 20
    num_std_dev = 2
    stock_data['BB_upper'], stock_data['BB_lower'] = bollinger_bands(stock_data["Price"], bb_period, num_std_dev)

    # Calculate Relative Strength Index (RSI)
    stock_data['RSI'] = relative_strength_index(stock_data["Price"], rsi_period)

    # Calculate standard deviation
    stock_data['Std_dev'] = calculate_standard_deviation(stock_data["Price"])

    # Calculate Value at Risk (VaR)
    stock_data['VaR'] = value_at_risk(stock_data['Return'], var_confidence_level)

    stock_data['macd_line'], stock_data["macd_signal"], stock_data[
        "macd_histogram"] = moving_average_convergence_divergence_new(stock_data["Price"], 12, 26, 9)

    # Generate the stock data plots
    figures = [
        plot_stock_data(stock_data["Price"], f'{symbol} Stock Price', 'Price'),
        plot_stock_data(stock_data[[ma_one_name, ma_two_name]], f'{symbol}  Moving Averages', 'Price'),
        plot_stock_data(stock_data['Return'], f'{symbol} Daily Returns', 'Return'),
        plot_stock_data(stock_data[['BB_upper', 'BB_lower']], f'{symbol} Bollinger Bands', 'Price'),
        plot_stock_data(stock_data['RSI'], f'{symbol} Relative Strength Index (RSI)', 'RSI'),
        plot_stock_data(stock_data['Std_dev'], f'{symbol} Standard Deviation', 'Standard Deviation'),
        plot_stock_data(stock_data['VaR'], f'{symbol} Value at Risk ({var_confidence_level * 100:.0f}%)', 'Value at '
                                                                                                          'Risk'),
        plot_stock_data(stock_data[['macd_line', "macd_signal", "macd_histogram"]], f'{symbol} MACD', 'MACD')
    ]

    return stock_data, figures


def analyze_combined_stock_data(stock_data, rsi_period=14, var_confidence_level=0.95):

    analyzed_data = stock_data.copy()
    prices = {}

    print(stock_data.keys())
    for symbol in stock_data.keys():
        print(f'Analyzing {symbol} stock data...')
        if Indicators.PRICE.value not in stock_data[symbol]:
            stock_data[symbol][Indicators.PRICE.value] = stock_data[symbol]["4. close"]
            del stock_data[symbol]["4. close"]
        else:
            print("Price already exists")

        analyzed_data[symbol][Indicators.PRICE.value] = stock_data[symbol][Indicators.PRICE.value]
        analyzed_data[symbol][Indicators.RETURNS.value] = calculate_return(stock_data[symbol][Indicators.PRICE.value])
        analyzed_data[symbol][Indicators.RSI.value] = relative_strength_index(stock_data[symbol][Indicators.PRICE.value], rsi_period)
        analyzed_data[symbol][Indicators.STD_DEV.value] = calculate_standard_deviation(stock_data[symbol][Indicators.PRICE.value])
        analyzed_data[symbol][Indicators.VAR.value] = value_at_risk(stock_data[symbol][Indicators.RETURNS.value], var_confidence_level)
        # Create the target column
        time_horizon = 30
        analyzed_data[symbol]['Target'] = (stock_data[symbol][Indicators.PRICE.value].shift(-time_horizon) - stock_data[symbol][Indicators.PRICE.value]) / stock_data[symbol][Indicators.PRICE.value]

        prices[symbol] = stock_data[symbol][Indicators.PRICE.value]

    # Generate the stock data plots
    figures = [
        plot_stock_data(pd.DataFrame(prices), f'Stock Price', 'Price'),
    ]

    return analyzed_data, figures
