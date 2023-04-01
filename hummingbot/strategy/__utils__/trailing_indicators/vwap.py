from .base_trailing_indicator import BaseTrailingIndicator
import pandas as pd

class VWAPIndicator(BaseTrailingIndicator):
    def __init__(self, sampling_length: int = 14, processing_length: int = 1):
        if processing_length != 1:
            raise Exception("VWAPIndicator processing_length should be 1")
        super().__init__(sampling_length, processing_length)

    def _indicator_calculation(self) -> float:
        price_data = pd.DataFrame(self._sampling_buffer.get_as_numpy_array(),
                                  columns=['high', 'low', 'close', 'volume'])
        typical_price = (price_data['high'] + price_data['low'] + price_data['close']) / 3
        tpv = typical_price * price_data['volume']
        cumulative_tpv = tpv.sum()
        cumulative_volume = price_data['volume'].sum()
        vwap = cumulative_tpv / cumulative_volume

        return vwap

    def _processing_calculation(self) -> float:
        return self._processing_buffer.get_last_value()
