import pandas as pd
import matplotlib.pyplot as plt
from .indicators import (
    simple_moving_average,
    exponential_moving_average,
    bollinger_bands,
    relative_strength_index,
    calculate_standard_deviation,
    value_at_risk,
)
from .enums import MovingAverageType


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
                       bb_period=20, var_confidence_level=0.95):
    # Calculate the moving averages based on the specified type and window sizes
    ma_one_name = f'MA{window_size_1}'
    ma_two_name = f'MA{window_size_2}'
    if ma_type == MovingAverageType.SMA:
        stock_data[ma_one_name] = simple_moving_average(stock_data['4. close'], window_size_1)
        stock_data[ma_two_name] = simple_moving_average(stock_data['4. close'], window_size_2)
    elif ma_type == MovingAverageType.EMA:
        stock_data[ma_one_name] = exponential_moving_average(stock_data['4. close'], window_size_1)
        stock_data[ma_two_name] = exponential_moving_average(stock_data['4. close'], window_size_2)

    # Calculate the daily returns
    stock_data['Return'] = calculate_return(stock_data['4. close'])

    # Calculate Bollinger Bands
    bb_period = 20
    num_std_dev = 2
    stock_data['BB_upper'], stock_data['BB_lower'] = bollinger_bands(stock_data['4. close'], bb_period, num_std_dev)

    # Calculate Relative Strength Index (RSI)
    stock_data['RSI'] = relative_strength_index(stock_data['4. close'], rsi_period)

    # Calculate standard deviation
    stock_data['Std_dev'] = calculate_standard_deviation(stock_data['4. close'])

    # Calculate Value at Risk (VaR)
    stock_data['VaR'] = value_at_risk(stock_data['Return'], var_confidence_level)

    # Generate the stock data plots
    figures = [
        plot_stock_data(stock_data['4. close'], 'Stock Price', 'Price'),
        plot_stock_data(stock_data[[ma_one_name, ma_two_name]], f'{ma_type.value} Moving Averages', 'Price'),
        plot_stock_data(stock_data['Return'], 'Daily Returns', 'Return'),
        plot_stock_data(stock_data[['BB_upper', 'BB_lower']], 'Bollinger Bands', 'Price'),
        plot_stock_data(stock_data['RSI'], 'Relative Strength Index (RSI)', 'RSI'),
        plot_stock_data(stock_data['Std_dev'], 'Standard Deviation', 'Standard Deviation'),
        plot_stock_data(stock_data['VaR'], f'Value at Risk ({var_confidence_level * 100:.0f}%)', 'Value at Risk')
    ]

    return stock_data, figures
