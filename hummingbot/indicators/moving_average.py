from typing import List
from enum import Enum
from hummingbot.strategy.market_trading_pair_tuple import MarketTradingPairTuple
import pandas as pd


class MovingAverageType(Enum):
    SMA = "SMA"
    EMA = "EMA"
    WMA = "WMA"


class MovingAverageCalculator:
    def __init__(self, prices: MarketTradingPairTuple, period: pd.Timedelta, ma_type: MovingAverageType):
        self.prices = prices
        self.period = period
        self.ma_type = ma_type

    def get_sma(self):
        return sum(self.prices[-self.period.total_seconds():]) / self.period.total_seconds()

    def get_ema(self):
        alpha = 2 / (self.period.total_seconds() + 1)
        ema = self.prices[-1]
        for price in reversed(self.prices[-self.period.total_seconds() + 1:]):
            ema = (price - ema) * alpha + ema
        return ema

    def get_wma(self):
        weights = list(range(1, self.period.total_seconds() + 1))
        weighted_prices = [w * p for w, p in zip(weights, self.prices[-self.period.total_seconds():])]
        return sum(weighted_prices) / sum(weights) if sum(weights) != 0 else 0

    def calculate(self):
        if self.ma_type == MovingAverageType.SMA:
            return self.get_sma()
        elif self.ma_type == MovingAverageType.EMA:
            return self.get_ema()
        elif self.ma_type == MovingAverageType.WMA:
            return self.get_wma()
        else:
            raise ValueError(f"Invalid MovingAverageType: {self.ma_type}")

