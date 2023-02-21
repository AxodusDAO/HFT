from collections import deque
from decimal import Decimal
from statistics import mean
import os

import pandas as pd

from hummingbot.core.data_type.common import OrderType
from hummingbot.strategy.script_strategy_base import ScriptStrategyBase


class buyLowSellHigh(ScriptStrategyBase):
    markets = {"binance": {"BTC-BUSD"}}
    #: pingpong is a variable to allow alternating between buy & sell signals
    pingpong = 0

    """
    for the sake of simplicity in testing, we will define fast MA as the 5-secondly-MA, and slow MA as the
    20-secondly-MA. User can change this as desired
    """
    timeframe = os.getenv("TIMEFRAME", "1s")
    de_fast_ma = deque([], maxlen=17)
    de_slow_ma = deque([], maxlen=75)
    order_amount = Decimal(os.getenv("BTC","0.003"))

    def _set_resample_rule(self, timeframe):
        """
        Convert timeframe to pandas resample rule value.
        https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.resample.html
        """
        timeframe_to_rule = {
            "1s": "1S",
            "10s": "10S",
            "30s": "30S",
            "1m": "1T",
            "5m": "5T",
            "15m": "15T"
        }
        if timeframe not in timeframe_to_rule.keys():
            self.logger().error(f"{timeframe} timeframe is not mapped to resample rule.")
            HummingbotApplication.main_application().stop()
        self._resample_rule = timeframe_to_rule[timeframe]

    def on_tick(self):
        p = self.connectors["binance"].get_price("BTC-BUSD", True)

        #: with every tick, the new price of the trading_pair will be appended to the deque and MA will be calculated
        self.de_fast_ma.append(p)
        self.de_slow_ma.append(p)
        fast_ma = mean(self.de_fast_ma)
        slow_ma = mean(self.de_slow_ma)

        #: logic for golden cross
        if (fast_ma > slow_ma) & (self.pingpong == 0):
            self.buy(
                connector_name="binance",
                trading_pair="BTC-BUSD",
                amount=Decimal(0.003),
                order_type=OrderType.LIMIT,
            )
            self.logger().info(f'{"0.003 BTC bought"}')
            self.pingpong = 1

        #: logic for death cross
        elif (slow_ma > fast_ma) & (self.pingpong == 1):
            self.sell(
                connector_name="binance",
                trading_pair="BTC-BUSD",
                amount=Decimal(0.003),
                order_type=OrderType.LIMIT,
            )
            self.logger().info(f'{"0.003 BTC sold"}')
            self.pingpong = 0

        else:
            self.logger().info(f'{"wait for a signal to be generated"}')
