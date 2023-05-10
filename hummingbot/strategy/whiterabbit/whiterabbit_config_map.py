from datetime import datetime, time
from decimal import Decimal
from typing import Dict, Optional, Union

from hummingbot.client.config.config_validators import (
    validate_bool,
    validate_decimal,    
    validate_datetime_iso_string,
    validate_derivative,
    validate_exchange,
    validate_int,
    validate_market_trading_pair,
    validate_time_iso_string,
)
from hummingbot.client.config.config_var import ConfigVar
from hummingbot.client.settings import AllConnectorSettings, required_exchanges
from hummingbot.client.config.config_data_types import BaseClientModel, ClientFieldData
from hummingbot.client.config.strategy_config_data_types import BaseTradingStrategyConfigMap

from pydantic import Field, root_validator, validator

class InfiniteModel(BaseClientModel):
    class Config:
        title = "infinite"


class FromDateToDateModel(BaseClientModel):
    start_datetime: datetime = Field(
        default=...,
        description="The start date and time for date-to-date execution timeframe.",
        client_data=ClientFieldData(
            prompt=lambda mi: "Please enter the start date and time (YYYY-MM-DD HH:MM:SS)",
            prompt_on_new=True,
        ),
    )
    end_datetime: datetime = Field(
        default=...,
        description="The end date and time for date-to-date execution timeframe.",
        client_data=ClientFieldData(
            prompt=lambda mi: "Please enter the end date and time (YYYY-MM-DD HH:MM:SS)",
            prompt_on_new=True,
        ),
    )

    class Config:
        title = "from_date_to_date"

    @validator("start_datetime", "end_datetime", pre=True)
    def validate_execution_time(cls, v: str) -> Optional[str]:
        ret = validate_datetime_iso_string(v)
        if ret is not None:
            raise ValueError(ret)
        return v


class DailyBetweenTimesModel(BaseClientModel):
    start_time: time = Field(
        default=...,
        description="The start time for daily-between-times execution timeframe.",
        client_data=ClientFieldData(
            prompt=lambda mi: "Please enter the start time (HH:MM:SS)",
            prompt_on_new=True,
        ),
    )
    end_time: time = Field(
        default=...,
        description="The end time for daily-between-times execution timeframe.",
        client_data=ClientFieldData(
            prompt=lambda mi: "Please enter the end time (HH:MM:SS)",
            prompt_on_new=True,
        ),
    )

    class Config:
        title = "daily_between_times"

    @validator("start_time", "end_time", pre=True)
    def validate_execution_time(cls, v: str) -> Optional[str]:
        ret = validate_time_iso_string(v)
        if ret is not None:
            raise ValueError(ret)
        return v


EXECUTION_TIMEFRAME_MODELS = {
    InfiniteModel.Config.title: InfiniteModel,
    FromDateToDateModel.Config.title: FromDateToDateModel,
    DailyBetweenTimesModel.Config.title: DailyBetweenTimesModel,
}
class SingleOrderLevelModel(BaseClientModel):
    class Config:
        title = "single_order_level"


class MultiOrderLevelModel(BaseClientModel):
    order_levels: int = Field(
        default=2,
        description="The number of orders placed on either side of the order book.",
        ge=2,
        client_data=ClientFieldData(
            prompt=lambda mi: "How many orders do you want to place on both sides?",
            prompt_on_new=True,
        ),
    )
    level_distances: Decimal = Field(
        default=Decimal("0"),
        description="The spread between order levels, expressed in % of optimal spread.",
        ge=0,
        client_data=ClientFieldData(
            prompt=lambda mi: "How far apart in % of optimal spread should orders on one side be?",
            prompt_on_new=True,
        ),
    )

    class Config:
        title = "multi_order_level"

    @validator("order_levels", pre=True)
    def validate_int_zero_or_above(cls, v: str):
        ret = validate_int(v, min_value=2)
        if ret is not None:
            raise ValueError(ret)
        return v

    @validator("level_distances", pre=True)
    def validate_decimal_zero_or_above(cls, v: str):
        ret = validate_decimal(v, min_value=Decimal("0"), inclusive=True)
        if ret is not None:
            raise ValueError(ret)
        return v


ORDER_LEVEL_MODELS = {
    SingleOrderLevelModel.Config.title: SingleOrderLevelModel,
    MultiOrderLevelModel.Config.title: MultiOrderLevelModel,
}


class TrackHangingOrdersModel(BaseClientModel):
    hanging_orders_cancel_pct: Decimal = Field(
        default=Decimal("10"),
        description="The spread percentage at which hanging orders will be cancelled.",
        gt=0,
        lt=100,
        client_data=ClientFieldData(
            prompt=lambda mi: (
                "At what spread percentage (from mid price) will hanging orders be canceled?"
                " (Enter 1 to indicate 1%)"
            ),
        )
    )

    class Config:
        title = "track_hanging_orders"

    @validator("hanging_orders_cancel_pct", pre=True)
    def validate_pct_exclusive(cls, v: str):
        ret = validate_decimal(v, min_value=Decimal("0"), max_value=Decimal("100"), inclusive=False)
        if ret is not None:
            raise ValueError(ret)
        return v


class IgnoreHangingOrdersModel(BaseClientModel):
    class Config:
        title = "ignore_hanging_orders"


HANGING_ORDER_MODELS = {
    TrackHangingOrdersModel.Config.title: TrackHangingOrdersModel,
    IgnoreHangingOrdersModel.Config.title: IgnoreHangingOrdersModel,
}

class WhiteRabbitConfigMap(BaseTradingStrategyConfigMap):
    strategy: str = Field(default="avellaneda_market_making", client_data=None)
    execution_timeframe_mode: Union[InfiniteModel, FromDateToDateModel, DailyBetweenTimesModel] = Field(
        default=...,
        description="The execution timeframe.",
        client_data=ClientFieldData(
            prompt=lambda mi: f"Select the execution timeframe ({'/'.join(EXECUTION_TIMEFRAME_MODELS.keys())})",
            prompt_on_new=True,
        ),
    )
    order_amount: Decimal = Field(
        default=...,
        description="The strategy order amount.",
        gt=0,
        client_data=ClientFieldData(
            prompt=lambda mi: WhiteRabbitConfigMap.order_amount_prompt(mi),
            prompt_on_new=True,
        )
    )
    order_optimization_enabled: bool = Field(
        default=True,
        description=(
            "Allows the bid and ask order prices to be adjusted based on"
            " the current top bid and ask prices in the market."
        ),
        client_data=ClientFieldData(
            prompt=lambda mi: "Do you want to enable best bid ask jumping? (Yes/No)"
        ),
    )
    risk_factor: Decimal = Field(
        default=Decimal("1"),
        description="The risk factor (\u03B3).",
        gt=0,
        client_data=ClientFieldData(
            prompt=lambda mi: "Enter risk factor (\u03B3)",
            prompt_on_new=True,
        ),
    )
    order_amount_shape_factor: Decimal = Field(
        default=Decimal("0"),
        description="The amount shape factor (\u03b7)",
        ge=0,
        le=1,
        client_data=ClientFieldData(
            prompt=lambda mi: "Enter order amount shape factor (\u03B7)",
        ),
    )
    min_spread: Decimal = Field(
        default=Decimal("0"),
        description="The minimum spread limit as percentage of the mid price.",
        ge=0,
        client_data=ClientFieldData(
            prompt=lambda mi: "Enter minimum spread limit (as % of mid price)",
        ),
    )
    order_refresh_time: float = Field(
        default=...,
        description="The frequency at which the orders' spreads will be re-evaluated.",
        gt=0.,
        client_data=ClientFieldData(
            prompt=lambda mi: "How often do you want to cancel and replace bids and asks (in seconds)?",
            prompt_on_new=True,
        ),
    )
    max_order_age: float = Field(
        default=1800.,
        description="A given order's maximum lifetime irrespective of spread.",
        gt=0.,
        client_data=ClientFieldData(
            prompt=lambda mi: (
                "How long do you want to cancel and replace bids and asks with the same price (in seconds)?"
            ),
        ),
    )
    order_refresh_tolerance_pct: Decimal = Field(
        default=Decimal("0"),
        description=(
            "The range of spreads tolerated on refresh cycles."
            " Orders over that range are cancelled and re-submitted."
        ),
        ge=-10,
        le=10,
        client_data=ClientFieldData(
            prompt=lambda mi: (
                "Enter the percent change in price needed to refresh orders at each cycle"
                " (Enter 1 to indicate 1%)"
            )
        ),
    )
    filled_order_delay: float = Field(
        default=60.,
        description="The delay before placing a new order after an order fill.",
        gt=0.,
        client_data=ClientFieldData(
            prompt=lambda mi: (
                "How long do you want to wait before placing the next order"
                " if your order gets filled (in seconds)?"
            )
        ),
    )
    inventory_target_base_pct: Decimal = Field(
        default=Decimal("50"),
        description="Defines the inventory target for the base asset.",
        ge=0,
        le=100,
        client_data=ClientFieldData(
            prompt=lambda mi: "What is the inventory target for the base asset? Enter 50 for 50%",
            prompt_on_new=True,
        ),
    )
    add_transaction_costs: bool = Field(
        default=False,
        description="If activated, transaction costs will be added to order prices.",
        client_data=ClientFieldData(
            prompt=lambda mi: "Do you want to add transaction costs automatically to order prices? (Yes/No)",
        ),
    )
    volatility_buffer_size: int = Field(
        default=200,
        description="The number of ticks that will be stored to calculate volatility.",
        ge=1,
        le=10_000,
        client_data=ClientFieldData(
            prompt=lambda mi: "Enter amount of ticks that will be stored to estimate order book liquidity",
        ),
    )
    trading_intensity_buffer_size: int = Field(
        default=200,
        description="The number of ticks that will be stored to calculate order book liquidity.",
        ge=1,
        le=10_000,
        client_data=ClientFieldData(
            prompt=lambda mi: "Enter amount of ticks that will be stored to estimate order book liquidity",
        ),
    )
    order_levels_mode: Union[SingleOrderLevelModel, MultiOrderLevelModel] = Field(
        default=SingleOrderLevelModel.construct(),
        description="Allows activating multi-order levels.",
        client_data=ClientFieldData(
            prompt=lambda mi: f"Select the order levels mode ({'/'.join(list(ORDER_LEVEL_MODELS.keys()))})",
        ),
    )
    order_override: Optional[Dict] = Field(
        default=None,
        description="Allows custom specification of the order levels and their spreads and amounts.",
        client_data=None,
    )
    hanging_orders_mode: Union[IgnoreHangingOrdersModel, TrackHangingOrdersModel] = Field(
        default=IgnoreHangingOrdersModel(),
        description="When tracking hanging orders, the orders on the side opposite to the filled orders remain active.",
        client_data=ClientFieldData(
            prompt=(
                lambda mi: f"How do you want to handle hanging orders? ({'/'.join(list(HANGING_ORDER_MODELS.keys()))})"
            ),
        ),
    )

    should_wait_order_cancel_confirmation: bool = Field(
        default=True,
        description=(
            "If activated, the strategy will await cancellation confirmation from the exchange"
            " before placing a new order."
        ),
        client_data=ClientFieldData(
            prompt=lambda mi: (
                "Should the strategy wait to receive a confirmation for orders cancellation"
                " before creating a new set of orders?"
                " (Not waiting requires enough available balance) (Yes/No)"
            ),
        )
    )

    class Config:
        title = "whiterabbit"

    # === prompts ===

def maker_trading_pair_prompt():
    derivative = whiterabbit_config_map.get("derivative").value
    example = AllConnectorSettings.get_example_pairs().get(derivative)
    return "Enter the token trading pair you would like to trade on %s%s >>> " \
           % (derivative, f" (e.g. {example})" if example else "")


# strategy specific validators
def validate_derivative_trading_pair(value: str) -> Optional[str]:
    derivative = whiterabbit_config_map.get("derivative").value
    return validate_market_trading_pair(derivative, value)


def validate_derivative_position_mode(value: str) -> Optional[str]:
    if value not in ["One-way", "Hedge"]:
        return "Position mode can either be One-way or Hedge mode"


def order_amount_prompt() -> str:
    trading_pair = whiterabbit_config_map["market"].value
    base_asset, quote_asset = trading_pair.split("-")
    return f"What is the amount of {base_asset} per order? >>> "


def validate_price_source(value: str) -> Optional[str]:
    if value not in {"current_market", "external_market", "custom_api"}:
        return "Invalid price source type."


def on_validate_price_source(value: str):
    if value != "external_market":
        whiterabbit_config_map["price_source_derivative"].value = None
        whiterabbit_config_map["price_source_market"].value = None
    if value != "custom_api":
        whiterabbit_config_map["price_source_custom_api"].value = None
    else:
        whiterabbit_config_map["price_type"].value = "custom"


def validate_price_type(value: str) -> Optional[str]:
    error = None
    price_source = whiterabbit_config_map.get("price_source").value
    if price_source != "custom_api":
        valid_values = {"mid_price",
                        "last_price",
                        "last_own_trade_price",
                        "best_bid",
                        "best_ask"}
        if value not in valid_values:
            error = "Invalid price type."
    elif value != "custom":
        error = "Invalid price type."
    return error


def price_source_market_prompt() -> str:
    external_market = whiterabbit_config_map.get("price_source_derivative").value
    return f'Enter the token trading pair on {external_market} >>> '


def validate_price_source_derivative(value: str) -> Optional[str]:
    if value == whiterabbit_config_map.get("derivative").value:
        return "Price source derivative cannot be the same as maker derivative."
    if validate_derivative(value) is not None and validate_exchange(value) is not None:
        return "Price source must must be a valid exchange or derivative connector."


def on_validated_price_source_derivative(value: str):
    if value is None:
        whiterabbit_config_map["price_source_market"].value = None


def validate_price_source_market(value: str) -> Optional[str]:
    market = whiterabbit_config_map.get("price_source_derivative").value
    return validate_market_trading_pair(market, value)


def validate_price_floor_ceiling(value: str) -> Optional[str]:
    try:
        decimal_value = Decimal(value)
    except Exception:
        return f"{value} is not in decimal format."
    if not (decimal_value == Decimal("-1") or decimal_value > Decimal("0")):
        return "Value must be more than 0 or -1 to disable this feature."

def derivative_on_validated(value: str):
    required_exchanges.add(value)

whiterabbit_config_map = {
    "strategy":
        ConfigVar(key="strategy",
                  prompt=None,
                  default="whiterabbit"),
    "derivative":
        ConfigVar(key="derivative",
                  prompt="Enter your maker derivative connector exchange name >>> ",
                  validator=validate_derivative,
                  on_validated=derivative_on_validated,
                  prompt_on_new=True),
    "market":
        ConfigVar(key="market",
                  prompt=maker_trading_pair_prompt,
                  validator=validate_derivative_trading_pair,
                  prompt_on_new=True),
    "leverage":
        ConfigVar(key="leverage",
                  prompt="How much leverage do you want to use? "
                         "(Binance Perpetual supports up to 75X for most pairs) >>> ",
                  type_str="int",
                  validator=lambda v: validate_int(v, min_value=0, inclusive=False),
                  prompt_on_new=True),
    "position_mode":
        ConfigVar(key="position_mode",
                  prompt="Which position mode do you want to use? (One-way/Hedge) >>> ",
                  validator=validate_derivative_position_mode,
                  type_str="str",
                  default="One-way",
                  prompt_on_new=True),
    "bid_spread":
        ConfigVar(key="bid_spread",
                  prompt="How far away from the mid price do you want to place the "
                         "first bid order? (Enter 1 to indicate 1%) >>> ",
                  type_str="decimal",
                  validator=lambda v: validate_decimal(v, 0, 100, inclusive=False),
                  prompt_on_new=True),
    "ask_spread":
        ConfigVar(key="ask_spread",
                  prompt="How far away from the mid price do you want to place the "
                         "first ask order? (Enter 1 to indicate 1%) >>> ",
                  type_str="decimal",
                  validator=lambda v: validate_decimal(v, 0, 100, inclusive=False),
                  prompt_on_new=True),
    "minimum_spread":
        ConfigVar(key="minimum_spread",
                  prompt="At what minimum spread should the bot automatically cancel orders? (Enter 1 for 1%) >>> ",
                  required_if=lambda: False,
                  type_str="decimal",
                  default=Decimal(-100),
                  validator=lambda v: validate_decimal(v, -100, 100, True)),
    "order_refresh_time":
        ConfigVar(key="order_refresh_time",
                  prompt="How often do you want to cancel and replace bids and asks "
                         "(in seconds)? >>> ",
                  type_str="float",
                  validator=lambda v: validate_decimal(v, 0, inclusive=False),
                  prompt_on_new=True),
    "order_refresh_tolerance_pct":
        ConfigVar(key="order_refresh_tolerance_pct",
                  prompt="Enter the percent change in price needed to refresh orders at each cycle "
                         "(Enter 1 to indicate 1%) >>> ",
                  type_str="decimal",
                  default=Decimal("0"),
                  validator=lambda v: validate_decimal(v, -10, 10, inclusive=True)),
    "order_amount":
        ConfigVar(key="order_amount",
                  prompt=order_amount_prompt,
                  type_str="decimal",
                  validator=lambda v: validate_decimal(v, min_value=Decimal("0"), inclusive=False),
                  prompt_on_new=True),
    "long_profit_taking_spread":
        ConfigVar(key="long_profit_taking_spread",
                  prompt="At what spread from the entry price do you want to place a short order to reduce position? (Enter 1 for 1%) >>> ",
                  type_str="decimal",
                  default=Decimal("0"),
                  validator=lambda v: validate_decimal(v, 0, 100, True),
                  prompt_on_new=True),
    "short_profit_taking_spread":
        ConfigVar(key="short_profit_taking_spread",
                  prompt="At what spread from the position entry price do you want to place a long order to reduce position? (Enter 1 for 1%) >>> ",
                  type_str="decimal",
                  default=Decimal("0"),
                  validator=lambda v: validate_decimal(v, 0, 100, True),
                  prompt_on_new=True),
    "long_stop_spread":
        ConfigVar(key="long_stop_spread",
                  prompt="At what spread from position entry price do you want to place stop_loss order? (Enter 1 for 1%) >>> ",
                  type_str="decimal",
                  default=Decimal("0"),
                  validator=lambda v: validate_decimal(v, -100, 100, False),
                  prompt_on_new=True),
    "short_stop_spread":
        ConfigVar(key="short_stop_spread",
                  prompt="At what spread from position entry price do you want to place stop_loss order? (Enter 1 for 1%) >>> ",
                  type_str="decimal",
                  default=Decimal("0"),
                  validator=lambda v: validate_decimal(v, -100, 100, False),
                  prompt_on_new=True),     
    "safe_stop_rate":
        ConfigVar(key="safe_stop_rate",
                  prompt="At what rate from position entry price do you want to place safe stop order? (Enter 1 for 1%) >>> ",
                  type_str="decimal",
                  default=Decimal("0"),
                  validator=lambda v: validate_decimal(v, -100, 100, False),
                  prompt_on_new=True),            
    "time_between_stop_loss_orders":
        ConfigVar(key="time_between_stop_loss_orders",
                  prompt="How much time should pass before refreshing a stop loss order that has not been executed? (in seconds) >>> ",
                  type_str="float",
                  default=60,
                  validator=lambda v: validate_decimal(v, 0, inclusive=False),
                  prompt_on_new=True),
    "stop_loss_slippage_buffer":
        ConfigVar(key="stop_loss_slippage_buffer",
                  prompt="How much buffer should be added in stop loss orders' price to account for slippage? (Enter 1 for 1%)? >>> ",
                  type_str="decimal",
                  default=Decimal("0.5"),
                  validator=lambda v: validate_decimal(v, 0, inclusive=True),
                  prompt_on_new=True),
    "price_ceiling":
        ConfigVar(key="price_ceiling",
                  prompt="Enter the price point above which only sell orders will be placed "
                         "(Enter -1 to deactivate this feature) >>> ",
                  type_str="decimal",
                  default=Decimal("-1"),
                  validator=validate_price_floor_ceiling),
    "price_floor":
        ConfigVar(key="price_floor",
                  prompt="Enter the price below which only buy orders will be placed "
                         "(Enter -1 to deactivate this feature) >>> ",
                  type_str="decimal",
                  default=Decimal("-1"),
                  validator=validate_price_floor_ceiling),



   "moving_price_band_enabled":
        ConfigVar(key="moving_price_band_enabled",
                  prompt="Would you like to enable moving price floor and ceiling? (Yes/No) >>> ",
                  type_str="bool",
                  default=False,
                  validator=validate_bool),
    "price_band_refresh_time":
        ConfigVar(key="price_band_refresh_time",
                  prompt="After this amount of time (in seconds), the price bands are reset based on the current price >>> ",
                  type_str="float",
                  default=86400,
                  required_if=lambda: whiterabbit_config_map.get("moving_price_band_enabled").value,
                  validator=validate_decimal),
    "ping_pong_enabled":
        ConfigVar(key="ping_pong_enabled",
                  prompt="Would you like to use the ping pong feature and alternate between buy and sell orders after fills? (Yes/No) >>> ",
                  type_str="bool",
                  default=False,
                  prompt_on_new=True,
                  validator=validate_bool),
    "order_levels":
        ConfigVar(key="order_levels",
                  prompt="How many orders do you want to place on both sides? >>> ",
                  type_str="int",
                  validator=lambda v: validate_int(v, min_value=0, inclusive=False),
                  default=1),
    "order_level_amount":
        ConfigVar(key="order_level_amount",
                  prompt="How much do you want to increase or decrease the order size for each "
                         "additional order? (decrease < 0 > increase) >>> ",
                  required_if=lambda: whiterabbit_config_map.get("order_levels").value > 1,
                  type_str="decimal",
                  validator=lambda v: validate_decimal(v),
                  default=0),
    "order_level_spread":
        ConfigVar(key="order_level_spread",
                  prompt="Enter the price increments (as percentage) for subsequent "
                         "orders? (Enter 1 to indicate 1%) >>> ",
                  required_if=lambda: whiterabbit_config_map.get("order_levels").value > 1,
                  type_str="decimal",
                  validator=lambda v: validate_decimal(v, 0, 100, inclusive=False),
                  default=Decimal("1")),
    "filled_order_delay":
        ConfigVar(key="filled_order_delay",
                  prompt="How long do you want to wait before placing the next order "
                         "if your order gets filled (in seconds)? >>> ",
                  type_str="float",
                  validator=lambda v: validate_decimal(v, min_value=0, inclusive=False),
                  default=60),
    "stop_order_delay":
        ConfigVar(key="stop_order_delay",
                  prompt="How long do you want to wait before placing the next order after STOP LOSS occurs"
                         "if your order gets filled (in seconds)? >>> ",
                  type_str="float",
                  validator=lambda v: validate_decimal(v, min_value=0, inclusive=False),
                  default=3600),
    "order_optimization_enabled":
        ConfigVar(key="order_optimization_enabled",
                  prompt="Do you want to enable best bid ask jumping? (Yes/No) >>> ",
                  type_str="bool",
                  default=False,
                  validator=validate_bool),
    "ask_order_optimization_depth":
        ConfigVar(key="ask_order_optimization_depth",
                  prompt="How deep do you want to go into the order book for calculating "
                         "the top ask, ignoring dust orders on the top "
                         "(expressed in base asset amount)? >>> ",
                  required_if=lambda: whiterabbit_config_map.get("order_optimization_enabled").value,
                  type_str="decimal",
                  validator=lambda v: validate_decimal(v, min_value=0),
                  default=0),
    "bid_order_optimization_depth":
        ConfigVar(key="bid_order_optimization_depth",
                  prompt="How deep do you want to go into the order book for calculating "
                         "the top bid, ignoring dust orders on the top "
                         "(expressed in base asset amount)? >>> ",
                  required_if=lambda: whiterabbit_config_map.get("order_optimization_enabled").value,
                  type_str="decimal",
                  validator=lambda v: validate_decimal(v, min_value=0),
                  default=0),
    "add_transaction_costs":
        ConfigVar(key="add_transaction_costs",
                  prompt="Do you want to add transaction costs automatically to order prices? (Yes/No) >>> ",
                  type_str="bool",
                  default=False,
                  validator=validate_bool),
    "price_source":
        ConfigVar(key="price_source",
                  prompt="Which price source to use? (current_market/external_market/custom_api) >>> ",
                  type_str="str",
                  default="current_market",
                  validator=validate_price_source,
                  on_validated=on_validate_price_source),
    "price_type":
        ConfigVar(key="price_type",
                  prompt="Which price type to use? (mid_price/last_price/last_own_trade_price/best_bid/best_ask) >>> ",
                  type_str="str",
                  required_if=lambda: whiterabbit_config_map.get("price_source").value != "custom_api",
                  default="mid_price",
                  validator=validate_price_type),
    "price_source_derivative":
        ConfigVar(key="price_source_derivative",
                  prompt="Enter external price source connector name or derivative name >>> ",
                  required_if=lambda: whiterabbit_config_map.get("price_source").value == "external_market",
                  type_str="str",
                  validator=validate_price_source_derivative,
                  on_validated=on_validated_price_source_derivative),
    "price_source_market":
        ConfigVar(key="price_source_market",
                  prompt=price_source_market_prompt,
                  required_if=lambda: whiterabbit_config_map.get("price_source").value == "external_market",
                  type_str="str",
                  validator=validate_price_source_market),
    "price_source_custom_api":
        ConfigVar(key="price_source_custom_api",
                  prompt="Enter pricing API URL >>> ",
                  required_if=lambda: whiterabbit_config_map.get("price_source").value == "custom_api",
                  type_str="str"),
    "custom_api_update_interval":
        ConfigVar(key="custom_api_update_interval",
                  prompt="Enter custom API update interval in second (default: 5.0, min: 0.5) >>> ",
                  required_if=lambda: False,
                  default=float(5),
                  type_str="float",
                  validator=lambda v: validate_decimal(v, Decimal("0.5"))),
    "order_override":
        ConfigVar(key="order_override",
                  prompt=None,
                  required_if=lambda: False,
                  default=True,
                  type_str="json"),
}