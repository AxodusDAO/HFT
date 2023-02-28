from typing import List

class MovingAverageIndicator:
    def __init__(self, period: int):
        self.period = period
        self.prices = []
    
    def add_price(self, price: float) -> None:
        if len(self.prices) == self.period:
            self.prices.pop(0)
        self.prices.append(price)
    
    def get_sma(self) -> float:
        if len(self.prices) < self.period:
            return None
        return sum(self.prices) / self.period
    
    def get_ema(self, alpha: float = 0.2) -> float:
        if len(self.prices) == 1:
            return self.prices[0]
        elif len(self.prices) < self.period:
            return None
        prev_ema = self.get_ema(alpha)
        curr_price = self.prices[-1]
        curr_ema = (alpha * curr_price) + ((1 - alpha) * prev_ema)
        return curr_ema
    
    def get_wma(self, weights: List[float]) -> float:
        if len(self.prices) < self.period:
            return None
        weighted_prices = [w * p for w, p in zip(weights, self.prices[-self.period:])]
        return sum(weighted_prices) / sum(weights)