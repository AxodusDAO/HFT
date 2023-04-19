from .base_trailing_indicator import BaseTrailingIndicator
import numpy as np
import pandas as pd


class VolumeAverageIndicator(BaseTrailingIndicator):
    def __init__(self, trading_data: pd.DataFrame, sampling_length: int = 30, processing_length: int = 15):
        super().__init__(sampling_length, processing_length)
        self.trading_data = trading_data

    def _indicator_calculation(self) -> float:
        volume_data = pd.DataFrame(self._sampling_buffer.get_as_numpy_array(),
                                   columns=['volume'])
        cumulative_volume = volume_data['volume'].sum()
        return cumulative_volume / self.sampling_length

    def _processing_calculation(self) -> float:
        processing_array = self._processing_buffer.get_as_numpy_array()
        if processing_array.size > 0:
            return np.mean(np.nan_to_num(processing_array))

    def get_current_trading_volume(self) -> float:
        if len(self.trading_data) == 0:
            return 0.0

        last_row = self.trading_data.iloc[-1]
        current_volume = last_row['volume']
        return current_volume


    def get_average_trading_volume(self) -> float:
        avg_volume = self.trading_data['volume'].mean()
        return avg_volume





