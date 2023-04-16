import numpy as np
from .base_trailing_indicator import BaseTrailingIndicator

class VAvgIndicator(BaseTrailingIndicator):
    def __init__(self, sampling_length: int = 300, processing_length: int = 150):
        super().__init__(sampling_length, processing_length)

    def _indicator_calculation(self) -> float:
        if not self.is_sampling_buffer_full:
            return np.nan

        volume_data = self._sampling_buffer.get_as_numpy_array()
        average_volume = np.mean(volume_data)
        return average_volume

