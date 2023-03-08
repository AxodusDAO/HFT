import logging
from dataclasses import dataclass
from typing import List
from decimal import Decimal
from hummingbot.core.event.events import TradeType
from hummingbot.indicators.moving_average import MovingAverageCalculator, MovingAverageType

mac_logger = None

@dataclass
class MACross:
    enabled: bool = False
    ma_type = MovingAverageType
    period: int = None
    _ma_calculator = MovingAverageCalculator
    _fast_ma: int = 0
    _slow_ma: int = 0
    _buys: TradeType = BUY
    _sells: TradeType = SELL
    _last_action: TradeType = None

    def __post_init__(self):
        self._ma_calculator = MovingAverageCalculator(self.period.interval, self.ma_type)

    @property
    def period(self) -> int:
        return self._
    
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
        self.enabled = value

    @classmethod
    def logger(cls):
        global mac_logger
        if mac_logger is None:
            mac_logger = logging.getLogger(__name__)
        return mac_logger
    