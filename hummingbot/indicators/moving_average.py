import numpy as np

def get_sma(prices, n):
    """
    Calculate Simple Moving Average (SMA) of a given set of prices over n periods.
    
    Args:
        prices (list): List of closing prices.
        n (int): Number of periods for which to calculate the SMA.
    
    Returns:
        sma (list): List of SMA values for each period.
    """
    sma = []
    for i in range(n-1, len(prices)):
        sma.append(np.mean(prices[i-n+1:i+1]))
    return sma

def get_ema(prices, n):
    """
    Calculate Exponential Moving Average (EMA) of a given set of prices over n periods.
    
    Args:
        prices (list): List of closing prices.
        n (int): Number of periods for which to calculate the EMA.
    
    Returns:
        ema (list): List of EMA values for each period.
    """
    ema = []
    multiplier = 2 / (n + 1)
    for i in range(len(prices)):
        if i == 0:
            ema.append(prices[0])
        else:
            ema.append((prices[i] - ema[i-1]) * multiplier + ema[i-1])
    return ema
