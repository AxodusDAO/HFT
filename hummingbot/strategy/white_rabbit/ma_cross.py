from typing import Tuple 
from decimal import Decimal 
from dataclasses import dataclass 
from hummingbot.core.event.events import TradeType

@dataclass 
class MACross: 
    balance_level: int
    trade_type: TradeType

    def get_balance_level(balance: Decimal, price: Decimal, fast_ma: Decimal, slow_ma: Decimal) -> int:
        if balance <= 0:
            return -1
        elif fast_ma > slow_ma and price < fast_ma:
            return 0
        elif slow_ma > fast_ma and price > fast_ma:
            return 0
        else:
            return 1

    def get_crossover(fast_ma: Decimal, slow_ma: Decimal, price: Decimal) -> Tuple[bool, bool]:
        golden_cross = False
        death_cross = False
        if fast_ma > slow_ma:
            golden_cross = True
        elif slow_ma > fast_ma:
            death_cross = True
        if golden_cross and price < fast_ma:
            return (True, False)
        elif death_cross and price > fast_ma:
            return (False, True)
        else:
            return (False, False)