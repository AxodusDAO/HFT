import pandas as pd
from dataclasses import dataclass 
from typing import List
from decimal import Decimal
from hummingbot.core.data_type.common import PriceType
from hummingbot.strategy.__utils__.trailing_indicators.moving_average import MovingAverageIndicator
from hummingbot.strategy.__utils__.trailing_indicators.exponential_moving_average import ExponentialMovingAverageIndicator

# Define the MACross dataclass
@dataclass
class MACross:
    ma_enabled: bool = False  # Indicator for whether the moving average cross strategy is enabled or not
    ma_type: str = "sma"  # The type of moving average to use (e.g., simple moving average)
    fast_ma: int = 9  # The period for the fast moving average
    slow_ma: int = 50  # The period for the slow moving average
    _prices: List[Decimal] = dataclasses.field(default_factory=list)

    def get_price(self) -> float:
        if self._asset_price_delegate is not None:
            price_provider = self._asset_price_delegate
        else:
            price_provider = self._market_info
        if self._price_type is PriceType.LastOwnTrade:
            price = self._last_own_trade_price
        else:
            price = price_provider.get_price_by_type(self._price_type)
        if price.is_nan():
            price = price_provider.get_price_by_type(PriceType.MidPrice)
        return price

    def get_ma(self, price: Decimal, tf: int):
        self._prices.append(price)  # Append the latest price before calculating the MA
        if self.ma_type == "sma":
            ma = MovingAverageIndicator(self._prices, tf)
        elif self.ma_type == "ema":
            ma = ExponentialMovingAverageIndicator(self._prices, tf)
        return ma.get_value()

    def golden_cross(self, fast_ma: Decimal, slow_ma: Decimal) -> bool:
        return fast_ma > slow_ma

    def death_cross(self, fast_ma: Decimal, slow_ma: Decimal) -> bool:
        return slow_ma > fast_ma

    def disable_sells(self, price: Decimal, slow_ma: Decimal) -> None:
        pass  # Implement logic to disable sells

    def disable_buys(self, price: Decimal, slow_ma: Decimal) -> None:
        pass  # Implement logic to disable buys

    # Method to update the prices list and calculate moving averages when enough data is available
    def update(self) -> bool:
        price = self.get_price()
        self._prices.append(price)

        if len(self._prices) >= self.slow_ma:
            fast_ma = self.get_ma(price, self.fast_ma)
            slow_ma = self.get_ma(price, self.slow_ma)

            if price < slow_ma:
                self.disable_sells(price, slow_ma)
            elif price > slow_ma:
                self.disable_buys(price, slow_ma)

            return self.golden_cross(fast_ma, slow_ma) or self.death_cross(fast_ma, slow_ma)

        return False

    # Method to enable or disable the moving average cross strategy
    def switch(self, value: bool) -> None:
        '''
        switch between enabled and disabled state

        :param value: set whether to enable or disable MA Cross:
        '''
        self.ma_enabled = value
