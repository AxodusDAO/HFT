from .base_trailing_indicator import BaseTrailingIndicator
import pandas as pd
import numpy as np

class VolumeIndicator(BaseTrailingIndicator):
    def __init__(self, sampling_length: int = 1, processing_length: int = 1):
        if sampling_length != 1:
            raise Exception("VolumeIndicator sampling_length should be 1")
        super().__init__(sampling_length, processing_length)

    def _indicator_calculation(self) -> float:
        np_sampling_buffer = self._sampling_buffer.get_as_numpy_array()
        
        if not np_sampling_buffer.size:
            trading_vol = 0
        else:
            trading_vol = np.sum(np_sampling_buffer)
            
        return trading_vol

    def _processing_calculation(self) -> float:
        return self._processing_buffer.get_last_value()
