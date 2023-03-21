import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator

class RSICalculator:

    def __init__(self, period=14):
        self.period = period
        self.prices = []

    def update_price(self, price):
        self.prices.append(price)
        if len(self.prices) > self.period + 1:
            self.prices.pop(0)

    def calculate_rsi(self):
        if len(self.prices) < self.period + 1:
            return None

        data = pd.DataFrame(self.prices, columns=['close'])
        rsi_indicator = RSIIndicator(data['close'], window=self.period)
        rsi = rsi_indicator.rsi().iloc[-1]
        return rsi
