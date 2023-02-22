from collections import deque
import pandas as pd
from statistics import mean
from hummingbot import strategy
from hummingbot.connector import exchange
from hummingbot.connector.gateway.clob.clob_types import OrderSide

from hummingbot.pmm_script.pmm_script_base import PMMScriptBase
from hummingbot.strategy.white_rabbit.white_rabbit import WhiteRabbitStrategy 

class WhiteRabbitScript(PMMScriptBase):
    """
    pingpong strategy with double Moving Averange 
    """    
    fast_ma = deque([], maxlen=7)
    slow_ma = deque([], maxlen=75)   

    def __init__(self):
        super().__init__()
        self.ping_pong_balance = 0

    
    
    def on_tick(self):
        strategy = self.pmm_parameters
        buys = strategy.order_levels
        sells = strategy.order_levels

    #: with every tick, the new price of the trading_pair will be appended to the deque and MA will be calculated
        p = exchange().get_price()    
        self.fast_ma.append(p)
        self.slow_ma.append(p)
               
               
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