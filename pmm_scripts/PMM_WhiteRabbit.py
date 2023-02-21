from collections import deque
from hummingbot.core.event.events import (
    BuyOrderCompletedEvent,
    SellOrderCompletedEvent
)
from hummingbot.pmm_script.pmm_script_base import PMMScriptBase
from statistics import mean
import pandas as pd


class WhiteRabbitScript(PMMScriptBase):
    """
    Demonstrates how to set up a ping pong trading strategy which alternates buy and sell orders.
    If a buy order is filled, there will be one less buy order submitted at the next refresh cycle.
    If a sell order is filled, there will be one less sell order submitted at the next refresh cycle.
    The balance is positive if there are more completed buy orders than sell orders.
    """
    de_fast_ma = deque([], maxlen=7)
    de_slow_ma = deque([], maxlen=75)

    def __init__(self):
        super().__init__()
        self.ping_pong_balance = 0

    def on_tick(self):
        strategy = self.pmm_parameters
        buys = strategy.order_levels
        sells = strategy.order_levels
    
    #: with every tick, the new price of the trading_pair will be appended to the deque and MA will be calculated
        self.de_fast_ma.append(mid_price)
        self.de_slow_ma.append(mid_price)
        fast_ma = mean(self.de_fast_ma)
        slow_ma = mean(self.de_slow_ma)

        if (fast_ma > slow_ma) & (self.ping_pong_balance > 0):
            buys -= self.ping_pong_balance
            buys = max(0, buys)
        elif (slow_ma > fast_ma) & (self.ping_pong_balance < 0):
            sells -= abs(self.ping_pong_balance)
            sells = max(0, sells)
        strategy.buy_levels = buys
        strategy.sell_levels = sells
    
    def calculate_ma(df: pd.DataFrame, )

# Alter pingpong status after order filled
    def on_buy_order_completed(self, event: BuyOrderCompletedEvent):
        self.ping_pong_balance += 1
    def on_sell_order_completed(self, event: SellOrderCompletedEvent):
        self.ping_pong_balance -= 1

# return the current balance here to be displayed when status command is executed.
    def on_status(self):
        return f"ping_pong_balance: {self.ping_pong_balance}"