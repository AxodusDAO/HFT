from .base_trailing_indicator import BaseTrailingIndicator
import pandas as pd

class VolAvgIndicator(BaseTrailingIndicator):
    def __init__(self, sampling_length: int = 20, processing_length: int = 1):
        if processing_length != 1:
            raise Exception("VolumeAverageIndicator processing_length should be 1")
        super().__init__(sampling_length, processing_length)

    def _indicator_calculation(self) -> float:
        volume_data = pd.DataFrame(self._sampling_buffer.get_as_numpy_array(),
                                   columns=['volume'])
        cumulative_volume = volume_data['volume'].sum()
        vol_avg = cumulative_volume / self.sampling_length

        return vol_avg

    def _processing_calculation(self) -> float:
        return self._processing_buffer.get_last_value()


'''
    volume_indicator = VolAvgIndicator(sampling_length=20)

# Add volume samples to the indicator
for volume_sample in volume_data:
    volume_indicator.add_sample(volume_sample)

# Get the current value of the Volume Average Indicator
current_volume_average = volume_indicator.current_value
print("Current Volume Average:", current_volume_average)
'''
