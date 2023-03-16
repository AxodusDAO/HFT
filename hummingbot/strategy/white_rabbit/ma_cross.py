from typing import List
from decimal import Decimal
from hummingbot.indicators.moving_average import MACalc

@dataclass
class MACross:
    enabled: bool = False
    ma_type: str = "sma"
    tf = MACalc
    fast_ma: int = 9
    slow_ma: int = 50
    prices: List[Decimal] = []

    def get_ma(self, tf: int) -> List[Decimal]:
        return self.tf.get_ma(self.prices, tf, self.ma_type)

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

    def update(self, tf: float, price: Decimal) -> bool:
        self.prices.append(price)
        if len(self.prices) >= self.slow_ma:
            self.fast_ma = self.get_ma(self.fast_ma)[-1]
            self.slow_ma = self.get_ma(self.slow_ma)[-1]
            return self.golden_cross() or self.death_cross()
        return False

    def switch(self, value: bool) -> None:
        '''
        switch between enabled and disabled state

        :param value: set whether to enable or disable MA Cross:
        '''
        self.enabled = value
