import logging
from dataclasses import dataclass
from typing import List
from decimal import Decimal
from hummingbot.core.event.events import TradeType
from hummingbot.indicators.moving_average import MovingAverageCalculator, MovingAverageType


class MACross:
    def __init__(self, period: int, fast_ma: int, slow_ma: int, ma_type: MovingAverageType = MovingAverageType.SMA, enabled = False):
        self.enabled = enabled
        self.ma_type = ma_type
        self.period = period
        self.ma_calculator = MovingAverageCalculator(self._ma_type, self._period)
        self.fast_ma = fast_ma
        self.slow_ma = slow_ma
        self.buys = []
        self.sells = []
        self.last_action = None

    def update(self, price: Decimal) -> bool:
        self.ma_calculator.add_new_sample(price)
        self.fast_ma = self.ma_calculator.get_moving_average(self.fast_ma)
        self.slow_ma = self.ma_calculator.get_moving_average(self.slow_ma)

        if self.fast_ma > self.slow_ma and self.last_action != TradeType.BUY:
            self.buys.append(TradeType.BUY)
            self.last_action = TradeType.BUY
            return True

        elif self.slow_ma > self.fast_ma and self.last_action != TradeType.SELL:
            self.sells.append(TradeType.SELL)
            self.last_action = TradeType.SELL
            return True

        return False

    def is_above_slow_ma(self, price: Decimal) -> bool:
        return price > self.ma_calculator.get_moving_average(self.slow_ma)

    def is_below_slow_ma(self, price: Decimal) -> bool:
        return price < self.ma_calculator.get_moving_average(self.slow_ma)

    def should_buy(self, price: Decimal) -> bool:
        return self.is_above_slow_ma(price) and self.last_action != TradeType.BUY

    def should_sell(self, price: Decimal) -> bool:
        return self.is_below_slow_ma(price) and self.last_action != TradeType.SELL

    def switch(self, value: bool) -> None:
        '''
        switch between enabled and disabled state
        :param value: set whether to enable or disable MACross
        '''
        self.enabled = value