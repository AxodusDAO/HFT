import logging
from dataclasses import dataclass
from typing import List
from decimal import Decimal
from hummingbot.core.event.events import TradeType
from hummingbot.indicators.moving_average import MACalc


@dataclass
class MAType(MACalc):
    prices: List[Decimal]
    n: int
    fast_sma: Decimal = None
    fast_ema: Decimal = None
    slow_sma: Decimal = None
    slow_ema: Decimal = None

    def __post_init__(self):
        self.fast_sma = self.get_sma(self.prices, self.fast_ma)
        self.fast_ema = self.get_ema(self.prices, self.fast_ma)
        self.slow_sma = self.get_sma(self.prices, self.slow_ma)
        self.slow_ema = self.get_ema(self.prices, self.slow_ma)


class MACross:
    enabled = False 
    ma_type: MAType
    period = 3200
    fast_ma = 9
    slow_ma = 50
    buys = []
    sells = []
    last_action = None

    def __init__(self, prices: List[Decimal], n: int):
        self.ma_type = MAType(prices, n)
        self.ma_calculator = MACalc()

    def update(self, price: Decimal):
        self.ma_calculator.add_new_sample(price)
        self.fast_ma = self.ma_calculator.get_moving_average(self.ma_type.fast_ema if self.ma_type.ma_type == "ema" else self.ma_type.fast_sma)
        self.slow_ma = self.ma_calculator.get_moving_average(self.ma_type.slow_ema if self.ma_type.ma_type == "ema" else self.ma_type.slow_sma)

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
