import pandas as pd
import dataclasses

from dataclasses import dataclass
from typing import List
from decimal import Decimal
from hummingbot.indicators.moving_average import MACalc

# Define the MACross dataclass
@dataclass
class MACross:
    ma_enabled: bool = False  # Indicator for whether the moving average cross strategy is enabled or not
    ma_type: str = "sma"  # The type of moving average to use (e.g. simple moving average)
    tf: MACalc = MACalc()  # Instantiate MACalc instead of using the class directly
    fast_ma: int = 9  # The period for the fast moving average
    slow_ma: int = 50  # The period for the slow moving average
    prices: List[float] = dataclasses.field(default_factory=list)  # Initialize the prices list
    buys: List[str] = dataclasses.field(default_factory=list)  # Add buys attribute to store buy actions
    sells: List[str] = dataclasses.field(default_factory=list)  # Add sells attribute to store sell actions

    def __post_init__(self):
        self.prices = []  # Initialize the prices list inside the constructor

    # Method to calculate moving average based on the type and period
    def get_ma(self, price, tf):
        self.tf = tf
        self.prices.append(price)  # Append the latest price before calculating the MA
        if self.ma_type == "sma":
            ma = self.tf.get_sma(self.prices)
        elif self.ma_type == "ema":
            ma = self.tf.get_ema(self.prices)
        return ma[-1]  # Return the last value of the MA

    # Method to determine if a golden cross occurred (fast_ma > slow_ma) and should buy
    def golden_cross(self, fast_ma: Decimal, slow_ma: Decimal) -> bool:
        if fast_ma > slow_ma:
            self.buys.append("BUY")
            return True
        return False

    # Method to determine if a death cross occurred (slow_ma > fast_ma) and should sell
    def death_cross(self, fast_ma: Decimal, slow_ma: Decimal) -> bool:
        if slow_ma > fast_ma:
            self.sells.append("SELL")
            return True
        return False
    
    def disable_sells(self, price, slow_ma):
        self.prices.append(price)
        if len(self.prices) > slow_ma:
            self.sells = []

    def disable_buys(self, price, slow_ma):
        self.prices.append(price)
        if len(self.prices) < slow_ma:
            self.buys = []

    # Method to update the prices list and calculate moving averages when enough data is available
    def update(self, price, slow_ma, fast_ma) -> bool:
        self.prices.append(price)
        if len(self.prices) >= self.slow_ma:
            fast_ma = self.get_ma(self.fast_ma, self.tf)
            slow_ma = self.get_ma(self.slow_ma, self.tf)
            
            if price < slow_ma:
                self.disable_sells(price, slow_ma)
            elif price > slow_ma:
                self.disable_buys(price, slow_ma)
            
            return self.golden_cross(fast_ma, slow_ma) or self.death_cross(fast_ma, slow_ma)
        
        return False


    # Method to enable or disable the moving average cross strategy
    def switch(self, value: bool) -> None:
            '''
            switch between enabled and disabled state

            :param value: set whether to enable or disable MA Cross:
            '''
            self.ma_enabled = value
