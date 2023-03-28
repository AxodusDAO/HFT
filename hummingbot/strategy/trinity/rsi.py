from typing import Optional
from hummingbot.strategy.market_trading_pair_tuple import MarketTradingPairTuple
from hummingbot.indicators.rsi import RSICalculator
from hummingbot.strategy.miner_pot import WhiteRabbitStrategy
from hummingbot.core.event.events import TradeType
from hummingbot.core.utils.tracking_nonce import get_tracking_nonce
from hummingbot.logger import HummingbotLogger


class RSIStrategy:
    def __init__(self,
                 market_info: MarketTradingPairTuple,
                 rsi_enabled: bool,
                 rsi_timeframe: Optional[str],
                 rsi_oversold: float,
                 rsi_overbought: float):
        self._market_info = market_info
        self._rsi_enabled = rsi_enabled
        self._rsi_timeframe = rsi_timeframe
        self._rsi_oversold = rsi_oversold
        self._rsi_overbought = rsi_overbought
        self._rsi = None
        self._logger = None

    def create(self, market_info: MarketTradingPairTuple):
        self._market_info = market_info

    def tick(self, timestamp: float):
        if self._rsi_enabled:
            self._rsi = self._rsi or RelativeStrengthIndex(
                self._market_info.trading_pair,
                self._rsi_timeframe,
                self._market_info.market,
                self._rsi_oversold,
                self._rsi_overbought
            )
            rsi_value = self._rsi.rsi()

            if rsi_value >= self._rsi_overbought:
                self._logger().info(f"RSI level is overbought with value {rsi_value:.2f}. Don't create buy orders.")
                return

            if rsi_value <= self._rsi_oversold:
                self._logger().info(f"RSI level is oversold with value {rsi_value:.2f}. Don't create sell orders.")
                return

        # The rest of the tick() logic goes here

    def format_status(self) -> str:
        if self._rsi_enabled:
            rsi_value = self._rsi.rsi() if self._rsi else None
            return f"RSI: {rsi_value:.2f}" if rsi_value else ""
        else:
            return ""

    def did_complete_buy(self, order_completed_event):
        # Implement your logic here for handling completed buy orders
        pass

    def did_complete_sell(self, order_completed_event):
        # Implement your logic here for handling completed sell orders
        pass

    def did_trade(self, trade_type: TradeType, trade_info):
        # Implement your logic here for handling trades
        pass

    def logger(self) -> HummingbotLogger:
        if not self._logger:
            self._logger = HummingbotLogger(__name__)
        return self._logger

    @property
    def exchange(self):
        return self._market_info.market.name

    @property
    def trading_pair(self):
        return self._market_info.trading_pair

    @property
    def base_asset(self):
        return self._market_info.trading_pair.split("-")[0]

    @property
    def quote_asset(self):
        return self._market_info.trading_pair.split("-")[1]

    @property
    def order_amount(self):
        # Implement your logic here for calculating order amount
        pass

    @property
    def tracking_nonce(self):
        return get_tracking_nonce()
