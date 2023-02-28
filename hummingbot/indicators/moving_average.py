from typing import List
import numpy as np


class MovingAverage:
    def __init__(self, window_size: int, input_values: List[float] = []):
        super().__init__()
        self._window_size = window_size
        self._input_values = input_values
        self._sma = None
        self._ema = None

    def compute(self) -> float:
        if len(self._input_values) < self._window_size:
            raise ValueError("Insufficient input values to compute moving average.")

        self._sma = np.mean(self._input_values[-self._window_size:])

        alpha = 2 / (self._window_size + 1)
        weights = np.array([(1 - alpha)**i for i in range(self._window_size - 1, -1, -1)])
        weights /= weights.sum()

        if self._ema is None:
            self._ema = self._sma
        else:
            self._ema = alpha * self._input_values[-1] + (1 - alpha) * self._ema

        return self._sma, self._ema

    def update(self, input_values: List[float]) -> None:
        self._input_values.extend(input_values)

        if len(self._input_values) > self._window_size:
            del self._input_values[:-self._window_size]

        self.compute()
