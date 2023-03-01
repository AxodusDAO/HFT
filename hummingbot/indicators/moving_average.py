from typing import List
from enum import Enum
from decimal import Decimal

class MovingAverageType(Enum):
sma = "SMA"
ema = "EMA"
wma = "WMA"

class MovingAverageCalculator:
    def init(self, prices: List[Decimal], period: int, ma_type: MovingAverageType):
        self.prices = prices
        self.period = period
        self.ma_type = ma_type

    def get_sma(self) -> Decimal:
        if len(self.prices) < self.period:
            return None
        return sum(self.prices[-self.period:]) / Decimal(self.period)

    def get_ema(self) -> Decimal:
        alpha = 2 / (self.period + 1)
        ema = self.prices[-self.period]
        for price in reversed(self.prices[-self.period + 1:]):
            ema = (price - ema) * alpha + ema
        return ema

    def get_wma(self) -> Decimal:
        if len(self.prices) < self.period:
            return None
        weights = list(range(1, self.period + 1))
        weighted_prices = [w * p for w, p in zip(weights, self.prices[-self.period:])]
        return sum(weighted_prices) / Decimal(sum(weights))

    def calculate(self) -> Decimal:
        if self.ma_type == MovingAverageType.sma:
            return self.get_sma()
        elif self.ma_type == MovingAverageType.ema:
            return self.get_ema()
        elif self.ma_type == MovingAverageType.wma:
            return self.get_wma()
        else:
            raise ValueError(f"Invalid MovingAverageType: {self.ma_type}")