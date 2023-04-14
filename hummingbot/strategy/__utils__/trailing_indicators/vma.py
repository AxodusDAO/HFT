import pandas as pd
from .base_trailing_indicator import BaseTrailingIndicator


class VolumeAverageIndicator(BaseTrailingIndicator):
    def __init__(self, sampling_length: int = 20, processing_length: int = 15):
        super().__init__(sampling_length, processing_length)

    def _indicator_calculation(self) -> float:
        volume = self._sampling_buffer.get('Volume')
        if not volume.empty:
            return volume.sum() / self.sampling_length

    def _processing_calculation(self) -> float:
        volume = self._processing_buffer.get('Volume')
        if not volume.empty:
            return volume.mean()
