import numpy as np
from typing import List

class MACalc:
    sma = get_sma()
    ema = get_ema()
    """
    A class for calculating moving averages.
    """
    @staticmethod
    def get_sma(prices: List[float], n: int) -> List[float]:
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

    @staticmethod
    def get_ema(prices: List[float], n: int) -> List[float]:
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

# to use this calculator you need call function: 
'''
sma = MACalc.get_sma(prices, n)
ema = MACalc.get_ema(prices, n)
'''