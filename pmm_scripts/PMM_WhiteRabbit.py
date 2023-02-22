from collections import deque
from typing import Self
import pandas as pd
from statistics import mean


from hummingbot.core.event.events import (
    BuyOrderCompletedEvent,
    SellOrderCompletedEvent
)
from hummingbot.pmm_script.pmm_script_base import PMMScriptBase
from hummingbot.strategy.white_rabbit.white_rabbit import WhiteRabbitStrategy 

class WhiteRabbitScript(PMMScriptBase):
    """
    pingpong strategy with double Moving Averange 
    """    
    
    def __init__(self):
        super().__init__()
        self.ping_pong_balance = 0

    def moving_averange(self):
    de_fast_ma = deque([], maxlen=7)
    de_slow_ma = deque([], maxlen=75)
    p = self.exchange().get_price(trading_pair)    

    #: with every tick, the new price of the trading_pair will be appended to the deque and MA will be calculated
        self.de_fast_ma.append(p)
        self.de_slow_ma.append(p)
        fast_ma = mean(self.de_fast_ma)
        slow_ma = mean(self.de_slow_ma)
    

    
    def on_tick(self):
        strategy = self.pmm_parameters
        buys = strategy.order_levels
        sells = strategy.order_levels
        
        if (fast_ma > slow_ma) & (self.ping_pong_balance > 0):
            buys -= self.ping_pong_balance
            buys = max(0, buys)
        elif (slow_ma > fast_ma) & (self.ping_pong_balance < 0):
            sells -= abs(self.ping_pong_balance)
            sells = max(0, sells)
        strategy.buy_levels = buys
        strategy.sell_levels = sells
        
    def on_order_filled(self, order):
        if order.side == OrderSide.BUY:
            self.ping_pong_balance += 1
        elif order.side == OrderSide.SELL:
            self.ping_pong_balance -= 1

    def on_order_cancelled(self, order):
        if order.side == OrderSide.BUY:
            self.ping_pong_balance -= 1
        elif order.side == OrderSide.SELL:
            self.ping_pong_balance += 1

    def on_strategy_parameters(self, parameters):
        parameters['order levels'] = 3

# Alter pingpong status after order filled
#    def on_buy_order_completed(self, event: BuyOrderCompletedEvent):
#        self.ping_pong_balance += 1
#    def on_sell_order_completed(self, event: SellOrderCompletedEvent):
#        self.ping_pong_balance -= 1

# return the current balance here to be displayed when status command is executed.
    def on_status(self):
        return f"ping_pong_balance: {self.ping_pong_balance}"