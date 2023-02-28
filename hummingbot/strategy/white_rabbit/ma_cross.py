from typing import Tuple
from decimal import Decimal
from dataclasses import dataclass

from hummingbot.indicators.moving_average import MovingAverageIndicator

@dataclass
class MACross:
    fast_ma: int
    slow_ma: int
    ma_type: str
    prices: list = None
    fast_ma_indicator: MovingAverageIndicator = None
    slow_ma_indicator: MovingAverageIndicator = None

    def __post_init__(self):
        self.prices = []
        self.fast_ma_indicator = MovingAverageIndicator(self.fast_ma)
        self.slow_ma_indicator = MovingAverageIndicator(self.slow_ma)

    def add_price(self, price: Decimal) -> None:
        self.prices.append(price)
        self.fast_ma_indicator.add_price(price)
        self.slow_ma_indicator.add_price(price)

    def calculate(self) -> Tuple[Decimal, Decimal]:
        fast_ma = 0
        slow_ma = 0
        if self.ma_type == "SMA":
            fast_ma = self.fast_ma_indicator.get_sma()
            slow_ma = self.slow_ma_indicator.get_sma()
        elif self.ma_type == "EMA":
            fast_ma = self.fast_ma_indicator.get_ema()
            slow_ma = self.slow_ma_indicator.get_ema()
        elif self.ma_type == "WMA":
            weights = list(range(1, self.fast_ma + 1))
            fast_ma = self.fast_ma_indicator.get_wma(weights)
            weights = list(range(1, self.slow_ma + 1))
            slow_ma = self.slow_ma_indicator.get_wma(weights)
        return fast_ma, slow_ma

    def get_crossover(self, price: Decimal) -> int:
        if len(self.prices) < max(self.fast_ma, self.slow_ma):
            return 0
        fast_ma, slow_ma = self.calculate()
        if fast_ma > slow_ma:
            if price < fast_ma:
                return -1
            else:
                return 0
        elif fast_ma < slow_ma:
            if price > fast_ma:
                return 1
            else:
                return 0
        else:
            return 0
