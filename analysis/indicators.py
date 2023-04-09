import numpy as np


# Function to calculate Simple Moving Average (SMA)
def simple_moving_average(data, window_size):
    return data.rolling(window=window_size).mean()


# Function to calculate Exponential Moving Average (EMA)
def exponential_moving_average(data, window_size):
    return data.ewm(span=window_size).mean()


# Function to calculate Bollinger Bands
def bollinger_bands(data, window_size, num_std_dev):
    sma = simple_moving_average(data, window_size)
    std_dev = data.rolling(window=window_size).std()
    upper_band = sma + (num_std_dev * std_dev)
    lower_band = sma - (num_std_dev * std_dev)
    return upper_band, lower_band


# Function to calculate the Relative Strength Index (RSI)
def relative_strength_index(data, window_size):
    data = data.dropna()  # Add this line to drop all 'None' values
    delta = data.diff()
    gains = delta.where(delta > 0, 0)
    losses = -delta.where(delta < 0, 0)
    avg_gain = gains.rolling(window=window_size).mean()
    avg_loss = losses.rolling(window=window_size).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


# Function to calculate the standard deviation of returns
def calculate_standard_deviation(data):
    return data.std()


# Function to calculate Value at Risk (VaR) using historical simulation
def value_at_risk(data, confidence_level):
    returns = data.pct_change().dropna()

    if returns.empty:  # Add this check to see if the returns array is empty
        return np.nan  # Return np.nan if the returns array is empty

    return -np.percentile(returns, 100 * (1 - confidence_level))


def moving_average_convergence_divergence(data, fast_period, slow_period):
    return exponential_moving_average(data, fast_period) - exponential_moving_average(data, slow_period)


def moving_average_convergence_divergence_new(data, fast_period, slow_period, signal_period):
    macd_line = exponential_moving_average(data, fast_period) - exponential_moving_average(data, slow_period)
    signal_line = exponential_moving_average(macd_line, signal_period)
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram
