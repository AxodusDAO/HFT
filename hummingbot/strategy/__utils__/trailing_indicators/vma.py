import pandas as pd
from .base_trailing_indicator import BaseTrailingIndicator


class VMA(BaseTrailingIndicator):
    def __init__(self, sampling_length: int = 20, processing_length: int = 10):
        super().__init__(sampling_length, processing_length)

    def _indicator_calculation(self) -> float:
        volume = self._sampling_buffer.get('Volume')
        if not volume.empty:
            return volume.sum() / self.sampling_length

    def _processing_calculation(self) -> float:
        volume = self._processing_buffer.get('Volume')
        if not volume.empty:
            return volume.mean()

'''

vma_indicator = VMA(sampling_length=20, processing_length=10)

    for volume in trading_volumes:
        vma_indicator.add_sample(volume)
        if vma_indicator.is_processing_ready():
            vma_value = vma_indicator.get_processing_result()
            # Do something with vma_value
'''