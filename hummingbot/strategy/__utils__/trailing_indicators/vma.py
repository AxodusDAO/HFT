import pandas as pd
from .base_trailing_indicator import BaseTrailingIndicator

class VolumeAverageIndicator(BaseTrailingIndicator):
    def __init__(self, sampling_length: int = 30, processing_length: int = 15):
        super().__init__(sampling_length, processing_length)

    def _indicator_calculation(self) -> float:
        volumes = self._sampling_buffer.get_as_pandas_series()
        if not volumes.empty:
            return volumes.mean()

    def _processing_calculation(self) -> float:
        processing_series = self._processing_buffer.get_as_pandas_series()
        if not processing_series.empty:
            return processing_series.sum() / processing_series.size



