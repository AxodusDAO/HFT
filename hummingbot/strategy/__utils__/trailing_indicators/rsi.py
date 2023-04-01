from .base_trailing_indicator import BaseTrailingIndicator
import pandas as pd

class RSIIndicator(BaseTrailingIndicator):
    def __init__(self, sampling_length: int = 14, processing_length: int = 1):
        if processing_length != 1:
            raise Exception("Relative Strength Index processing_length should be 1")
        super().__init__(sampling_length, processing_length)

    def _indicator_calculation(self) -> float:
        price_data = pd.Series(self._sampling_buffer.get_as_numpy_array())
        delta = price_data.diff().dropna()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.rolling(window=self._sampling_length).mean()
        avg_loss = loss.rolling(window=self._sampling_length).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        return rsi.iloc[-1]

    def _processing_calculation(self) -> float:
        return self._processing_buffer.get_last_value()
