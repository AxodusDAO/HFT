from typing import List
from decimal import Decimal
from hummingbot.core.event.events import TradeType
from hummingbot.indicators.moving_average import MovingAverageCalculator, MovingAverageType

class MACross:
    enable: bool = False
    def __init__(self, period: int, ma_type: MovingAverageType, fast_ma: int, slow_ma: int):
        self._ma_calculator = MovingAverageCalculator(period, ma_type)
        self._fast_ma = fast_ma
        self._slow_ma = slow_ma
        self._buys = []
        self._sells = []

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

        if fast_ma > slow_ma:
            self._buys.append(TradeType.BUY)
        elif slow_ma > fast_ma:
            self._sells.append(TradeType.SELL)
    
    def switch(self, value: bool) -> None:
        '''
        switch between enabled and disabled state

        :param value: set whether to enable or disable MACross
        '''
        self.enable = value
