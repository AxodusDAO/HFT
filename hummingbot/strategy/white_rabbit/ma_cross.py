from typing import List
from decimal import Decimal
from collections import deque
from hummingbot.core.event.events import TradeType
from hummingbot.indicators.moving_average import MovingAverageCalculator, MovingAverageType

class MACross:
    enable: bool = False
    def __init__(self, period: int, ma_type: MovingAverageType, fast_ma: int, slow_ma: int):
        assert isinstance(period, int) and isinstance(fast_ma, int) and isinstance(slow_ma, int), \
            "period, fast_ma, and slow_ma must be integers"
        assert period > fast_ma and period > slow_ma, "period must be greater than fast_ma and slow_ma"
        self._ma_calculator = MovingAverageCalculator(period, ma_type)
        self._fast_ma = fast_ma
        self._slow_ma = slow_ma
        self._buys = deque()
        self._sells = deque()

    @property
    def buys(self) -> List[TradeType]:
        return list(self._buys)

    @property
    def sells(self) -> List[TradeType]:
        return list(self._sells)

    def update(self, price: Decimal):
        self._ma_calculator.add_new_price(price)
        fast_ma = self._ma_calculator.get_moving_average(self._fast_ma)
        slow_ma = self._ma_calculator.get_moving_average(self._slow_ma)

        if fast_ma > slow_ma:
            self._buys.append(TradeType.BUY)
        elif slow_ma > fast_ma:
            self._sells.append(TradeType.SELL)
    
    def toggle(self) -> None:
        '''
        toggle between enabled and disabled state
        '''
        self.enable = not self.enable

