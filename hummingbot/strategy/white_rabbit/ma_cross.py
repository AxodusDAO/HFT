import logging
from dataclasses import dataclass
from typing import List
from decimal import Decimal
from hummingbot.core.event.events import TradeType
from hummingbot.indicators.moving_average import MACalc


class MACross:
    enabled: bool = False 
    ma_type: str = "sma"
    period: int = 3200
    fast_ma: int = 9
    slow_ma: int = 50
    
    def __post_init__(self):
        self.ma_calculator = MACalc(self.ma_type, self.period)
        self.buys = []
        self.sells = []
        self.last_action = None
    
    def update(self, price: Decimal):
        self.ma_calculator.add_new_sample(price)
        self.fast_ma = self.ma_calculator.get_moving_average(self.fast_ma)
        self.slow_ma = self.ma_calculator.get_moving_average(self.slow_ma)

        if self.fast_ma > self.slow_ma and self.should_buy():
            self.buys.append(TradeType.BUY)
            self.last_action = TradeType.BUY
            return True

        elif self.slow_ma > self.fast_ma and self.should_sell():
            self.sells.append(TradeType.SELL)
            self.last_action = TradeType.SELL
            return True

        return False

    def should_buy(self) -> bool:
        return self.last_action != TradeType.BUY

    def should_sell(self) -> bool:
        return self.last_action != TradeType.SELL


