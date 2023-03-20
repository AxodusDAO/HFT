import logging
import dataclasses

from dataclasses import dataclass
from typing import List
from decimal import Decimal
from hummingbot.indicators.moving_average import MACalc

mac_logger = None

@dataclass
class MACross:
    ma_enabled: bool = False
    ma_type: str = "sma"
    tf: MACalc = MACalc()
    fast_ma: int = 9
    slow_ma: int = 50
    _last_action: str = None
    _buys: List[str] = dataclasses.field(default_factory=list)
    _sells: List[str] = dataclasses.field(default_factory=list)
    _prices: List[Decimal] = dataclasses.field(default_factory=list)
    

    @classmethod
    def logger(cls):
        global mac_logger
        if mac_logger is None:
            mac_logger = logging.getLogger(__name__)
        return mac_logger

    @property
    def last_action(self) -> str:
        return self._last_action

    @property
    def fast_ma(self) -> int:
        return self._fast_ma

    @property
    def slow_ma(self) -> int:
        return self._slow_ma

    def get_ma(self, tf: int) -> List[Decimal]:
        if self.ma_type == "sma":
            return self.tf.get_sma(self._prices, tf)
        elif self.ma_type == "ema":
            return self.tf.get_ema(self._prices, tf)

    def golden_cross(self, fast_ma: Decimal, slow_ma: Decimal) -> bool:
        if fast_ma > slow_ma and self.should_buy():
            self._buys.append("BUY")
            self._last_action = "BUY"
            self.logger().info("Golden Cross: fast_ma: %s slow_ma: %s crossed up", fast_ma, slow_ma)
            return True
        return False

    def death_cross(self, fast_ma: Decimal, slow_ma: Decimal) -> bool:
        if slow_ma > fast_ma and self.should_sell():
            self._sells.append("SELL")
            self._last_action = "SELL"
            self.logger().info("Death Cross: fast_ma: %s slow_ma: %s crossed down", fast_ma, slow_ma)
            return True
        return False

    def should_buy(self) -> bool:
        return self._last_action != "BUY"

    def should_sell(self) -> bool:
        return self._last_action != "SELL"

    def update(self, price: Decimal) -> bool:
        self._prices.append(price)
        if len(self._prices) >= self._slow_ma:  # Use self._prices instead of self.prices
            fast_ma = self.get_ma(self._fast_ma)[-1]
            slow_ma = self.get_ma(self._slow_ma)[-1]
            return self.golden_cross(fast_ma, slow_ma) or self.death_cross(fast_ma, slow_ma)
        return False

    def switch(self, value: bool) -> None:
        self.ma_enabled = value
