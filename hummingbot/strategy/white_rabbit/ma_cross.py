from typing import List
from decimal import Decimal
from hummingbot.core.event.events import TradeType
from hummingbot.indicators.moving_average import MovingAverageCalculator, MovingAverageType


class MACross:
    def __init__(self, period: int, ma_type: MovingAverageType, fast_ma: int, slow_ma: int):
        self._ma_calculator = MovingAverageCalculator(period, ma_type)
        self._fast_ma = fast_ma
        self._slow_ma = slow_ma
        self._buys = []
        self._sells = []
        self._last_action = None

    @property
    def buys(self) -> List[TradeType]:
        return self._buys

    @property
    def sells(self) -> List[TradeType]:
        return self._sells

    def update(self, price: Decimal):
        self._ma_calculator.add_new_price(price)
        fast_ma = self._ma_calculator.get_moving_average(self._fast_ma)
        slow_ma = self._ma_calculator.get_moving_average(self._slow_ma)

        if fast_ma > slow_ma and self._last_action != TradeType.BUY:
            self._buys.append(TradeType.BUY)
            self._last_action = TradeType.BUY
        elif slow_ma > fast_ma and self._last_action != TradeType.SELL:
            self._sells.append(TradeType.SELL)
            self._last_action = TradeType.SELL

    def is_above_slow_ma(self, price: Decimal) -> bool:
        return price > self._ma_calculator.get_moving_average(self._slow_ma)

    def is_below_slow_ma(self, price: Decimal) -> bool:
        return price < self._ma_calculator.get_moving_average(self._slow_ma)

    def should_buy(self, price: Decimal) -> bool:
        return self.is_above_slow_ma(price) and self._last_action != TradeType.BUY

    def should_sell(self, price: Decimal) -> bool:
        return self.is_below_slow_ma(price) and self._last_action != TradeType.SELL

    def switch(self, value: bool) -> None:
        '''
        switch between enabled and disabled state
        :param value: set whether to enable or disable MACross
        '''
        self.enable = value

