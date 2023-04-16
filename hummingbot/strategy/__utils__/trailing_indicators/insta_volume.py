from .base_trailing_indicator import BaseTrailingIndicator
import numpy as np


class VolumeIndicator(BaseTrailingIndicator):
    def __init__(self, sampling_length: int = 10, processing_length: int = 5):
        super().__init__(sampling_length, processing_length)

    def _indicator_calculation(self) -> float:
        # Instead of calculating volatility, we will calculate the sum of volume
        # in the sampling buffer as the instant volume.
        np_sampling_buffer = self._sampling_buffer.get_as_numpy_array()
        volume = np.sum(np_sampling_buffer)
        return volume

    def _processing_calculation(self) -> float:
        # Only the last calculated volume, not an average of multiple past volumes
        return self._processing_buffer.get_last_value()
