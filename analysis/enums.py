from enum import Enum


# Enum for the type of moving average to use
class MovingAverageType(Enum):
    SMA = "SMA"
    EMA = "EMA"


class Indicators(Enum):
    PRICE = "Price"
    RETURNS = "Returns"
    SMA = "SMA"
    EMA = "EMA"
    BB = "BB"
    RSI = "RSI"
    STD_DEV = "STD_DEV"
    VAR = "VAR"
    MACD = "MACD"