from .base_trailing_indicator import BaseTrailingIndicator
import numpy as np
import pandas as pd


class VolumeAverageIndicator(BaseTrailingIndicator):
    def __init__(self, trading_data: pd.DataFrame, sampling_length: int = 30, processing_length: int = 15):
        super().__init__(sampling_length, processing_length)
        self.trading_data = trading_data

    def _indicator_calculation(self) -> float:
        volume_data = self._sampling_buffer.get_as_numpy_array()
        cumulative_volume = volume_data[:, 0][-self.sampling_length:].sum()
        return cumulative_volume / self.sampling_length

    def _processing_calculation(self) -> float:
        processing_array = self._processing_buffer.get_as_numpy_array()
        if processing_array.size > 0:
            return np.nan_to_num(processing_array).mean()

    def get_current_trading_volume(self) -> float:
        if len(self.trading_data) == 0:
            return 0.0

        last_row = self.trading_data.iloc[-1]
        current_volume = last_row.get('volume', 0.0)
        return current_volume

    def get_average_trading_volume(self) -> float:
        avg_volume = self.trading_data.get('volume', pd.Series(dtype=float)).mean()
        return avg_volume







