from dataclasses import dataclass
from typing import List
from decimal import Decimal
from hummingbot.core.event.events import TradeType
from hummingbot.indicators.moving_average import MACalc


@dataclass
class MAType(MACalc):
    prices: List[Decimal]
    n: int
    ma_type: str = "sma"

    def __post_init__(self):
        if self.ma_type == "sma":
            self.fast_ma = self.get_sma(self.prices, self.n)
            self.slow_ma = self.get_sma(self.prices, self.n * 2)
        elif self.ma_type == "ema":
            self.fast_ma = self.get_ema(self.prices, self.n)
            self.slow_ma = self.get_ema(self.prices, self.n * 2)


class MACross:
    def __init__(self, prices: List[Decimal], n: int):
        self.ma_type = MAType(prices, n)
        self.enabled = False
        self.period = 3200
        self.fast_ma = self.ma_type.fast_ma
        self.slow_ma = self.ma_type.slow_ma
        self.buys = []
        self.sells = []
        self.last_action = None

    def update(self, price: Decimal):
        self.ma_type.prices.append(price)
        self.ma_type.fast_ma = self.ma_type.get_moving_average(self.ma_type.fast_ma, price)
        self.ma_type.slow_ma = self.ma_type.get_moving_average(self.ma_type.slow_ma, price)
        self.fast_ma = self.ma_type.fast_ma
        self.slow_ma = self.ma_type.slow_ma

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
