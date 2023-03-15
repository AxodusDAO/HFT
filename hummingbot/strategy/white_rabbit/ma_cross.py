import logging
from dataclasses import dataclass
from decimal import Decimal
from hummingbot.core.event.events.trade_type import TradeType
from hummingbot.indicators.moving_average import MACalc


class MACross:
    def __init__(self, ma_type: str = "sma"):
        self.enabled = False
        self.ma_type = ma_type
        self.timestamp = None
        self.fast_ma = None
        self.slow_ma = None
        self.prices = []
        self.buys = []
        self.sells = []
        self.last_action = None
        self.logger = logging.getLogger(__name__)

    def get_ma(self):
        if self.ma_type == "sma":
            return MACalc.get_sma(self.prices, self.timestamp)
        elif self.ma_type == "ema":
            return MACalc.get_ema(self.prices, self.timestamp)

    def golden_cross(self) -> bool:
        if self.fast_ma > self.slow_ma and self.should_buy():
            self.buys.append(TradeType.BUY)
            self.last_action = TradeType.BUY
            return True
        return False

    def death_cross(self) -> bool:
        if self.slow_ma > self.fast_ma and self.should_sell():
            self.sells.append(TradeType.SELL)
            self.last_action = TradeType.SELL
            return True
        return False

    def should_buy(self) -> bool:
        return self.last_action != TradeType.BUY

    def should_sell(self) -> bool:
        return self.last_action != TradeType.SELL

    def update(self, timestamp: float, price: Decimal) -> bool:
        self.prices.append(price)
        self.fast_ma = self.get_ma()
        self.slow_ma = self.get_ma() * 2
        return self.golden_cross() or self.death_cross()

    def switch(self, value: bool) -> None:
        '''
        switch between enabled and disabled state

        :param value: set whether to enable or disable MovingPriceBand:
        '''
        self.enabled = value