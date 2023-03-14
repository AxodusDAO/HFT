import numpy as np
from decimal import Decimal
from typing import List

class MACalc:

    """
    A class for calculating moving averages.
    """
    @staticmethod
    def get_sma(prices: List[Decimal], timestamp: int) -> List[Decimal]:
        """
        Calculate Simple Moving Average (SMA) of a given set of prices over n periods.

        Args:
            prices (List[Decimal]): List of closing prices.
            timestamp (int): Number of periods for which to calculate the SMA.

        Returns:
            List[Decimal]: List of SMA values for each period.
        """
        sma = []
        for i in range(timestamp-1, len(prices)):
            sma.append(np.mean(prices[i-timestamp+1:i+1]))
        return sma

    @staticmethod
    def get_ema(prices: List[Decimal], timestamp: int) -> List[Decimal]:
        """
        Calculate Exponential Moving Average (EMA) of a given set of prices over n periods.

       Args:
            prices (List[Decimal]): List of closing prices.
            timestamp (int): Number of periods for which to calculate the EMA.

        Returns:
            List[Decimal]: List of EMA values for each period.
        """
        ema = []
        multiplier = 2 / (timestamp + 1)
        for i in range(len(prices)):
            if i == 0:
                ema.append(prices[0])
            else:
                ema.append((prices[i] - ema[i-1]) * multiplier + ema[i-1])
        return ema

# to use this calculator you need call function: 
'''
sma = MACalc.get_sma(prices, timestamp)
ema = MACalc.get_ema(prices, timestamp)
'''