import logging
from collections import deque
from decimal import Decimal
from statistics import mean


from hummingbot.core.data_type.common import OrderType
from hummingbot.pmm_script.pmm_script_base import PMMScriptBase


class HiLoSpot(PMMScriptBase):
    """
        Demonstrates how to set up a ping pong trading strategy which alternates buy and sell orders.
        If a buy order is filled, there will be one less buy order submitted at the next refresh cycle.
        If a sell order is filled, there will be one less sell order submitted at the next refresh cycle.
        The balance is positive if there are more completed buy orders than sell orders.
    """
     
    #: pingpong is a variable to allow alternating between buy & sell signals
    def __init__(self):
        super().__init__()
        self.ping_pong_balance = 0

    """
        for the sake of simplicity in testing, we will define fast MA as the 7-candles-MA, and slow MA as the
        75-candles-MA. User can change this as desired
    """
    de_fast_ma = deque([], maxlen=7)
    de_slow_ma = deque([], maxlen=75)

    def logger(cls):
        global mpb_logger
        if mpb_logger is None:
            mpb_logger = logging.getLogger(__name__)
        return mpb_logger

    def on_tick(self):
        strategy = self.pmm_parameters
        buy = strategy.order_levels
        sell = strategy.order_levels
        
        #: with every tick, the new price of the trading_pair will be appended to the deque and MA will be calculated
        self.de_fast_ma.append(p)
        self.de_slow_ma.append(p)
        fast_ma = mean(self.de_fast_ma)
        slow_ma = mean(self.de_slow_ma)

        #: logic for golden cross
        if (fast_ma > slow_ma) & (self.pingpong == 0):
            self.buy(
                order_type=OrderType.LIMIT,
            )
            self.logger().info(f'{"%s BTC bought"}')
            self.pingpong = 1

        #: logic for death cross
        elif (slow_ma > fast_ma) & (self.pingpong == 1):
            self.sell(
                order_type=OrderType.LIMIT,
            )
            self.logger().info(f'{"%s BTC sold"}')
            self.pingpong = 0

        else:
            self.logger().info(f'{"wait for a signal to be generated"}')
