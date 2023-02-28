from typing import Dict, List
import numpy as np


class RSIIndicator:
    def __init__(self, config: Dict[str, any]):
        self._period = config.get("rsi_length", 14)
        self._prev_candles: List[float] = []
        self._rsi_oversold_level = config.get("rsi_oversold_level", 30)
        self._rsi_overbought_level = config.get("rsi_overbought_level", 70)

    def compute(self, candles: List[float]) -> float:
        self._prev_candles += candles

        while len(self._prev_candles) > self._period:
            self._prev_candles.pop(0)

        if len(self._prev_candles) < self._period:
            return np.nan

        np_candles = np.array(self._prev_candles)
        diff = np_candles[1:] - np_candles[:-1]
        gain = diff * (diff > 0)
        loss = -diff * (diff < 0)
        avg_gain = gain.mean()
        avg_loss = loss.mean()
        rs = avg_gain / avg_loss if avg_loss != 0 else np.inf
        rsi = 100 - 100 / (1 + rs)
        return rsi

    def reset(self):
        self._prev_candles.clear()