from collections import deque
from decimal import Decimal
from statistics import mean

from hummingbot.core.data_type.common import OrderType
from hummingbot.strategy.script_strategy_base import ScriptStrategyBase
from hummingbot.core.event.events import (
    BuyOrderCompletedEvent,
    SellOrderCompletedEvent
)
from hummingbot.pmm_script.pmm_script_base import PMMScriptBase

class WhiteRabbitPMM(PMMScriptBase):
# Start with pingpong = 0 (hedge)
    def __init__(self):
        super().__init__()
        self.ping_pong_balance = 0
# increase or reduce position according to pingpong ballance
    def on_buy_order_completed(self, event: BuyOrderCompletedEvent):
        self.ping_pong_balance += 1
    def on_sell_order_completed(self, event: SellOrderCompletedEvent):
        self.ping_pong_balance -= 1

#### Moving Averange 
    de_fast_ma = deque([], maxlen=50)
    de_slow_ma = deque([], maxlen=200)

        super().on_tick()
# check if the price is higher than the fast moving average 
# and lower than the slow moving average
    def on_candle(self, event: CandleEvent):
        self.de_fast_ma.append(event.candle.close)
        self.de_slow_ma.append(event.candle.close)
        if len(self.de_fast_ma) < 50 or len(self.de_slow_ma) < 200:
            return

        strategy = self.pmm_parameters

        if self.de_fast_ma[-1] > self.de_slow_ma[-1]:
            strategy.buy = True
            strategy.sell = False

        elif self.de_fast_ma[-1] < self.de_slow_ma[-1]:
            strategy.buy = False
            strategy.sell = True

# show status of pingpong ballance
    def on_status(self):
        # return the current balance here to be displayed when status command is executed.
        return f"ping_pong_balance: {self.ping_pong_balance}"
