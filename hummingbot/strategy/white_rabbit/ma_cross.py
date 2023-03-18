import pandas  as pd
import dataclasses

from dataclasses import dataclass
from typing import List
from decimal import Decimal
from hummingbot.indicators.moving_average import MACalc

#Define the MACross dataclass
@dataclass
class MACross:
    ma_enabled: bool = False # Indicator for whether the moving average cross strategy is enabled or not
    ma_type: str = "sma" # The type of moving average to use (e.g. simple moving average)
    tf: MACalc = MACalc() # Instantiate MACalc instead of using the class directly
    fast_ma: int = 9 # The period for the fast moving average
    slow_ma: int = 50 # The period for the slow moving average
    prices: List[Decimal] = dataclasses.field(default_factory=list) # Use a default factory for mutable types
    last_action: str = None # Add last_action attribute to track the last action taken
    buys: List[str] = dataclasses.field(default_factory=list) # Add buys attribute to store buy actions
    sells: List[str] = dataclasses.field(default_factory=list) # Add sells attribute to store sell actions
    _ma_type: str = "sma"

    # Method to calculate moving average based on the type and period
    def get_ma(self, tf: int) -> List[Decimal]:
        if self.ma_type == "sma":
            return self.tf.get_sma(self.prices, tf)
        elif self.ma_type == "ema":
            return self.tf.get_ema(self.prices, tf)

    @property
    def ma_type(self) -> str:
        return self._ma_type

    @ma_type.setter
    def ma_type(self, value: str): 
        self._ma_type = value


    # Method to determine if a golden cross occurred (fast_ma > slow_ma) and should buy
    def golden_cross(self, fast_ma_value: Decimal, slow_ma_value: Decimal) -> bool:
        if fast_ma_value > slow_ma_value and self.should_buy():
            self.buys.append("BUY")
            self.last_action = "BUY"
            return True
        return False

    # Method to determine if a death cross occurred (slow_ma > fast_ma) and should sell
    def death_cross(self, fast_ma_value: Decimal, slow_ma_value: Decimal) -> bool:
        if slow_ma_value > fast_ma_value and self.should_sell():
            self.sells.append("SELL")
            self.last_action = "SELL"
            return True
        return False

    # Method to check if the last action was not a buy
    def should_buy(self) -> bool:
        return self.last_action != "BUY"

    # Method to check if the last action was not a sell
    def should_sell(self) -> bool:
        return self.last_action != "SELL"

    # Method to update the prices list and calculate moving averages when enough data is available
    def update(self, price: Decimal) -> bool:
        self.prices.append(price)
        if len(self.prices) >= self.slow_ma:
            fast_ma_value = self.get_ma(self.fast_ma)[-1]
            slow_ma_value = self.get_ma(self.slow_ma)[-1]
            return self.golden_cross(fast_ma_value, slow_ma_value) or self.death_cross(fast_ma_value, slow_ma_value)
        return False


    # Method to enable or disable the moving average cross strategy
    def switch(self, value: bool) -> None:
            '''
            switch between enabled and disabled state

            :param value: set whether to enable or disable MA Cross:
            '''
            self.enabled = value