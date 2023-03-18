import pandas as pd
from decimal import Decimal
from typing import List


class MACalc:
    """
    A class for calculating moving averages.
    """
    @staticmethod
    def get_sma(prices: List[Decimal], tf: pd.Timedelta) -> List[Decimal]:
        """
        Calculate Simple Moving Average (SMA) of a given set of prices over n periods.

        Args:
            prices (List[Decimal]): List of closing prices.
            tf (pd.Timedelta): Time period for which to calculate the SMA.

        Returns:
            List[Decimal]: List of SMA values for each period.
        """
        sma = pd.Series(prices).rolling(window=tf).mean().tolist()
        return sma

    @staticmethod
    def get_ema(prices: List[Decimal], tf: pd.Timedelta) -> List[Decimal]:
        """
        Calculate Exponential Moving Average (EMA) of a given set of prices over n periods.

        Args:
            prices (List[Decimal]): List of closing prices.
            tf (pd.Timedelta): Time period for which to calculate the EMA.

        Returns:
            List[Decimal]: List of EMA values for each period.
        """
        seconds = int(tf.total_seconds())
        ema = pd.Series(prices).ewm(span=seconds).mean().tolist()
        return ema

# to use this calculator you need call function: 
'''
sma = MACalc.get_sma(prices, tf)
ema = MACalc.get_ema(prices, tf)
'''