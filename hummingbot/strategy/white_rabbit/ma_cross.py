import logging
from dataclasses import dataclass
from decimal import Decimal
from hummingbot.core.event.events import TradeType
from hummingbot.indicators.moving_average import MACalc


class MAType:
    def __init__(self, ma_type: str, prices: list, timestamp: float):
        self.ma_type = ma_type
        self.prices = prices
        self.timestamp = timestamp
        
    def get_ma(self):
        if self.ma_type == "sma":
            return MACalc.get_sma(self.prices, self.timestamp)
        elif self.ma_type == "ema":
            return MACalc.get_ema(self.prices, self.timestamp)


@dataclass
class MACross:
    enabled: bool = False
    ma_type = MAType()
    prices: list = []
    timestamp: float = None
    fast_ma: float = None
    slow_ma: float = None
    buys: list = []
    sells: list = []
    last_action: TradeType = None

    def __post_init__(self):
        self.ma_type = MAType(self.ma_type.ma_type, self.prices, self.timestamp)
        self.fast_ma = self.ma_type.get_ma()
        self.slow_ma = self.ma_type.get_ma() * 2

    @classmethod
    def logger(cls):
        return logging.getLogger(__name__)

    def update(self, timestamp: float, price: Decimal) -> bool:
        self.prices.append(price)
        self.fast_ma = self.ma_type.get_ma()
        self.slow_ma = self.ma_type.get_ma() * 2
        return self.golden_cross() or self.death_cross()
    
    def _set_resample_rule(self, timeframe):
        """
        Convert timeframe to pandas resample rule value.
        https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.resample.html
        """
        timeframe_to_rule = {
            "1s": "1S",
            "1m": "1T",
            "5m": "5T",
            "15m": "15T",
            "1h": "60T"
        }
        if timeframe not in timeframe_to_rule.keys():
            self.logger().error(f"{timeframe} timeframe is not mapped to resample rule.")
            HummingbotApplication.main_application().stop()
        self._resample_rule = timeframe_to_rule[timeframe]

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

    def switch(self, value: bool) -> None:
        '''
        switch between enabled and disabled state

        :param value: set whether to enable or disable MovingPriceBand
        '''
        self.enabled = value