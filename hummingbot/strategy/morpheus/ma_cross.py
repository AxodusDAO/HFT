import pandas as pd
from dataclasses import dataclass
import dataclasses
from typing import List
from decimal import Decimal
from hummingbot.core.data_type.common import PriceType
from hummingbot.strategy.__utils__.trailing_indicators.moving_average import MovingAverageIndicator
from hummingbot.strategy.__utils__.trailing_indicators.exponential_moving_average import ExponentialMovingAverageIndicator

# Define the MACross dataclass
@dataclass
class MACross:
    ma_enabled: bool = False
    ma_type: str = "sma"
    fast_ma: int = 9
    slow_ma: int = 50

    def __init__(self, ma_type: str = "sma", fast_ma: int = 9, slow_ma: int = 50):
        self._ma_type = ma_type
        self._fast_ma = fast_ma
        self._slow_ma = slow_ma
        self._prices: List[Decimal] = []

    @property
    def fast_ma(self):
        return self._fast_ma

    @fast_ma.setter
    def fast_ma(self, fast_ma: int):
        self._fast_ma = fast_ma

    @property
    def slow_ma(self):
        return self._slow_ma

    @slow_ma.setter
    def slow_ma(self, slow_ma: int):
        self._slow_ma = slow_ma

    def get_price(self) -> float:
        # Implement your logic to get the latest price
        pass

    def get_ma(self, price: Decimal, period: int):
        self._prices.append(price)  # Append the latest price before calculating the MA

        if self._ma_type == "sma":
            ma = MovingAverageIndicator(self._prices, period)
        elif self._ma_type == "ema":
            ma = ExponentialMovingAverageIndicator(self._prices, period)

        return ma.get_value()

    def golden_cross(self, fast_ma: Decimal, slow_ma: Decimal):
        return fast_ma > slow_ma

    def death_cross(self, fast_ma: Decimal, slow_ma: Decimal):
        return slow_ma > fast_ma

    def update(self) -> bool:
        price = self.get_price()
        self._prices.append(price)

        if len(self._prices) >= self._slow_ma:
            fast_ma = self.get_ma(price, self._fast_ma)
            slow_ma = self.get_ma(price, self._slow_ma)

            if price < slow_ma:
                # Implement logic to disable sells
                pass
            elif price > slow_ma:
                # Implement logic to disable buys
                pass

            return self.golden_cross(fast_ma, slow_ma) or self.death_cross(fast_ma, slow_ma)

        return False

    # Method to enable or disable the moving average cross strategy
    def switch(self, value: bool) -> None:
        '''
        switch between enabled and disabled state

        :param value: set whether to enable or disable MA Cross:
        '''
        self.ma_enabled = value
