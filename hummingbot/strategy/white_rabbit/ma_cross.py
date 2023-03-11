import logging
from dataclasses import dataclass
from typing import List
from decimal import Decimal
from hummingbot.core.event.events import TradeType
from hummingbot.indicators.moving_average import MACalc


class MAType(MACalc):
    def __init__(self, prices: List[Decimal], n: int):
        self.fast_sma = MACalc.get_sma(prices, self.fast_ma)
        self.fast_ema = MACalc.get_ema(prices, self.fast_ma)
        self.slow_sma = MACalc.get_sma(prices, self.slow_ma)
        self.slow_ema = MACalc.get_ema(prices, self.slow_ma)

class MACross:
    enabled: bool = False 
    ma_type: MAType = None
    period: int = 3200
    fast_ma: int = 9
    slow_ma: int = 50

    def __init__(self, prices: List[Decimal], n: int):
        self.ma_calculator = MACalc()
        self.buys = []
        self.sells = []
        self.last_action = None
        self.ma_type = MAType(prices, n)
    
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
