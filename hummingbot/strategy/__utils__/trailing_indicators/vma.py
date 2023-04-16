import numpy as np
from .base_trailing_indicator import BaseTrailingIndicator

class VAvgIndicator(BaseTrailingIndicator):
    def __init__(self, sampling_length: int = 300, processing_length: int = 150):
        super().__init__(sampling_length, processing_length)

    def _indicator_calculation(self) -> float:
        volumes = self._sampling_buffer.get_as_numpy_array()
        if volumes.size > 0:
            return np.mean(volumes)

    def _processing_calculation(self) -> float:
        processing_array = self._processing_buffer.get_as_numpy_array()
        if processing_array.size > 0:
            return np.sum(processing_array) / processing_array.size

'''
    vma_indicator = VolumeAverageIndicator(sampling_length=300, processing_length=150)

        for volume in trading_volumes:
            vma_indicator.add_sample(volume)
            if vma_indicator.is_processing_ready():
                vma_value = vma_indicator.get_processing_result()
                # Do something with vma_value
'''
