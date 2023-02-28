from typing import Tuple
from decimal import Decimal


class MACross:
    def __init__(
        self,
        market_info: Tuple[str, str],
        max_order_age: float,
        minimum_spread: Decimal,
        ping_pong_enabled: bool,
        fast_ma: int,
        slow_ma: int,
    ):
        self.market_info = market_info
        self.max_order_age = max_order_age
        self.minimum_spread = minimum_spread
        self.ping_pong_enabled = ping_pong_enabled
        self.fast_ma = fast_ma
        self.slow_ma = slow_ma

    def ma_cross(self, fast_ma: Decimal, slow_ma: Decimal) -> int:
        """
        Determines whether to enter a long position, short position or do nothing.

        :param fast_ma: value of the fast moving average
        :param slow_ma: value of the slow moving average
        :return: -1 for short, 0 for nothing, 1 for long
        """
        if fast_ma > slow_ma:
            pingpong = 1
        elif fast_ma < slow_ma:
            pingpong = -1
        else:
            pingpong = 0

        # Ping pong enabled and cross detected
        if self.ping_pong_enabled and pingpong != 0:
            return pingpong
        else:
            return 0
