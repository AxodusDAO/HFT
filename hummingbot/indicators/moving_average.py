from enum import Enum
from typing import List
from hummingbot.strategy.market_trading_pair_tuple import MarketTradingPairTuple

class MovingAverageType(Enum):
    SMA = "SMA"
    EMA = "EMA"
    WMA = "WMA"


class MovingAverageCalculator:
    def __init__(self, prices: MarketTradingPairTuple, period: int, ma_type: MovingAverageType):
        self._prices = prices
        self._period = period
        self._ma_type = ma_type

    def get_sma(self) -> float:
        return sum(self._prices[-self._period:]) / self._period

    def get_ema(self) -> float:
        alpha = 2 / (self._period + 1)
        ema = self._prices[-1]
        for price in reversed(self._prices[-self._period + 1:]):
            ema = (price - ema) * alpha + ema
        return ema

    def get_wma(self) -> float:
        weights = list(range(1, self._period + 1))
        weighted_prices = [w * p for w, p in zip(weights, self._prices[-self._period:])]
        return sum(weighted_prices) / sum(weights) if sum(weights) != 0 else 0

    def calculate(self) -> float:
        if self._ma_type == MovingAverageType.SMA:
            return self.get_sma()
        elif self._ma_type == MovingAverageType.EMA:
            return self.get_ema()
        elif self._ma_type == MovingAverageType.WMA:
            return self.get_wma()
        else:
            raise ValueError(f"Invalid MovingAverageType: {self._ma_type}")

