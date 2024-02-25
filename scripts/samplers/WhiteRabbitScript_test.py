from hummingbot.strategy.script_strategy_base import ScriptStrategyBase
from hummingbot.strategy.liquidity_mining.liquidity_mining_config_map import liquidity_mining_config_map
from typing import Dict
from decimal import Decimal
from hummingbot.connector.exchange_base import ExchangeBase
from hummingbot.core.event.events import OrderType
from collections import deque
from statistics import mean


class RSIScript(ScriptStrategyBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trading_pair = self.pairs[0]
        self.rsi_period = liquidity_mining_config_map.get("rsi_period").value
        self.rsi_oversold = liquidity_mining_config_map.get("rsi_oversold").value
        self.rsi_overbought = liquidity_mining_config_map.get("rsi_overbought").value

    def on_tick(self):
        price = self.current_price
        prices = [Decimal(p) for p in self.pricing_source.poll_price(self.trading_pair)]
        rsi = self.rsi(prices, self.rsi_period)
        if rsi is not None and rsi <= self.rsi_oversold:
            self.buy(self.trading_pair, price, self.get_quantity(price), OrderType.MARKET)

        elif rsi is not None and rsi >= self.rsi_overbought:
            self.sell(self.trading_pair, price, self.get_quantity(price), OrderType.MARKET)

    def rsi(self, prices, rsi_period):
        if len(prices) <= rsi_period:
            return None

        prices = prices[-rsi_period:]
        price_changes = [prices[i] - prices[i-1] for i in range(1, len(prices))]
        gains = [change if change > 0 else 0 for change in price_changes]
        losses = [-change if change < 0 else 0 for change in price_changes]

        avg_gain = mean(gains)
        avg_loss = mean(losses)
        if avg_loss == 0:
            return 100.0
        rs = avg_gain / avg_loss
        rsi = 100.0 - (100.0 / (1.0 + rs))
        return rsi

    def get_quantity(self, price: Decimal) -> Decimal:
        balance = self.connector.get_available_balance(self.trading_pair.split("-")[1])
        if balance <= Decimal(0):
            return Decimal(0)
        return min(balance, Decimal(1000)) / price


class HiLoScript(ScriptStrategyBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trading_pair = self.pairs[0]
        self.fast_ma_period = 5
        self.slow_ma_period = 20
        self.de_fast_ma = deque([], maxlen=self.fast_ma_period)
        self.de_slow_ma = deque([], maxlen=self.slow_ma_period)

    def on_tick(self):
        price = self.current_price
        self.de_fast_ma.append(price)
        self.de_slow_ma.append(price)
        fast_ma = mean(self.de_fast_ma)
        slow_ma = mean(self.de_slow_ma)

        if fast_ma > slow_ma:
            self.buy(self.trading_pair, price, self.get_quantity(price), OrderType.MARKET)

        elif fast_ma < slow_ma:
            self.sell(self.trading_pair, price, 
