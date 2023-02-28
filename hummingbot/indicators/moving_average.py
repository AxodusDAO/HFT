from typing import List
from enum import Enum
from decimal import Decimal


class MovingAverageType(Enum):
    SMA = "SMA"
    EMA = "EMA"
    WMA = "WMA"


class MovingAverageIndicator:
    def __init__(self, period: int, ma_type: MovingAverageType, fast_ma: int, slow_ma: int):
        self.period = period
        self.ma_type = ma_type
        self.fast_ma = fast_ma
        self.slow_ma = slow_ma
        self.prices = []

    def add_price(self, price: Decimal) -> None:
        if len(self.prices) == self.period:
            self.prices.pop(0)
        self.prices.append(price)

    def get_sma(self) -> Decimal:
        if len(self.prices) < self.period:
            return None
        return sum(self.prices) / self.period

    def get_ema(self) -> Decimal:
        alpha = 2 / (self.fast_ma + 1)
        if len(self.prices) == 1:
            return self.prices[0]
        elif len(self.prices) < self.fast_ma:
            return None
        prev_ema = self.get_ema()
        curr_price = self.prices[-1]
        curr_ema = (alpha * curr_price) + ((1 - alpha) * prev_ema)
        return curr_ema

    def get_wma(self) -> Decimal:
        if len(self.prices) < self.period:
            return None
        weights = list(range(1, self.period + 1))
        weighted_prices = [w * p for w, p in zip(weights, self.prices[-self.period:])]
        return sum(weighted_prices) / sum(weights)

    def on_status(self):
        if self.ma_type == MovingAverageType.SMA:
            ma_level = self.get_sma()
        elif self.ma_type == MovingAverageType.EMA:
            ma_level = self.get_ema()
        elif self.ma_type == MovingAverageType.WMA:
            ma_level = self.get_wma()
        else:
            raise ValueError(f"Invalid MovingAverageType: {self.ma_type}")
        
        if ma_level is not None:
            print(f"{self.ma_type.value} MA level: {ma_level}") 