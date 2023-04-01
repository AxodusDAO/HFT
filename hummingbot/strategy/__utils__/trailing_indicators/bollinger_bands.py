from .base_trailing_indicator import BaseTrailingIndicator
import pandas as pd
import numpy as np

class BollingerBands(BaseTrailingIndicator):
    def bollinger_bands(data, window=20, num_std_dev=2):
        """
        Calculate Bollinger Bands for a given dataset.
        
        Parameters:
        data (pandas.Series): Price data for a financial instrument.
        window (int): Number of periods for the simple moving average.
        num_std_dev (int): Number of standard deviations for the upper and lower bands.
        
        Returns:
        pandas.DataFrame: A dataframe with columns for the middle, upper, and lower bands.
        """
        sma = data.rolling(window=window).mean()
        std_dev = data.rolling(window=window).std()
        
        upper_band = sma + (std_dev * num_std_dev)
        lower_band = sma - (std_dev * num_std_dev)
        
        bands = pd.DataFrame({'Middle': sma, 'Upper': upper_band, 'Lower': lower_band})
        return bands