from enum import Enum
from ibapi.order import Order
from ibapi.contract import Contract
from typing import Optional

from OrderManager.core.OrderExecutionManager import OrderManager


class OrderType(Enum):
    MARKET = "MKT"
    LIMIT = "LMT"
    STOP = "STP"
    STOP_LIMIT = "STP LMT"
    MARKET_ON_CLOSE = "MOC"
    LIMIT_ON_CLOSE = "LOC"
    MARKET_IF_TOUCHED = "MIT"
    LIMIT_IF_TOUCHED = "LIT"
    RELATIVE = "REL"
    VOLATILITY = "VOL"
    MARKET_TO_LIMIT = "MTL"
    AUCTION = "AUCTION"
    BOX_TOP = "BOX TOP"
    SCALE = "SCALE"
    DARK_ICE = "DARK ICE"
    SWEEP_TO_FILL = "SWEEP"
    CONTINGENT = "CONTINGENT"
    VWAP = "VWAP"


class SecurityType(Enum):
    EQUITY = "STK"
    OPTION = "OPT"
    FUTURE = "FUT"
    CURRENCY = "CASH"
    INDEX = "IND"
    CFD = "CFD"
    BOND = "BOND"
    CRYPTO = "CRYPTO"


class OrderFactory:

    def __init__(self, order_manager: OrderManager):
        self.om = order_manager


    def update_order_id(self):
        self.om.order_id += 1


    @staticmethod
    def create_contract(sec_type: SecurityType, symbol: str, exchange: str = "SMART", currency: str = "USD",
                         **kwargs) -> Contract:
        contract = Contract()
        contract.symbol = symbol
        contract.secType = sec_type.value
        contract.exchange = exchange
        contract.currency = currency

        if sec_type == SecurityType.OPTION:
            contract.lastTradeDateOrContractMonth = kwargs["expiration"]
            contract.strike = kwargs["strike"]
            contract.right = kwargs["right"]  # "C" or "P"
            contract.multiplier = kwargs.get("multiplier", "100")
        elif sec_type == SecurityType.FUTURE:
            contract.lastTradeDateOrContractMonth = kwargs["expiration"]
            contract.multiplier = kwargs.get("multiplier", "1")
        elif sec_type == SecurityType.CURRENCY:
            contract.symbol = kwargs["base_currency"]
            contract.currency = kwargs["quote_currency"]

        return contract


    def create_order(self, order_type: OrderType, action: str, quantity: float, limit_price: Optional[float] = None,
                      stop_price: Optional[float] = None, tif: str = "DAY") -> Order:
        order = Order()
        order.orderId = self.om.order_id
        order.action = action
        order.orderType = order_type.value
        order.totalQuantity = quantity
        order.tif = tif

        if order_type in (OrderType.LIMIT, OrderType.STOP_LIMIT):
            order.lmtPrice = limit_price
        if order_type in (OrderType.STOP, OrderType.STOP_LIMIT):
            order.auxPrice = stop_price

        self.update_order_id()
        return order


    def create_equity_order(self, symbol: str, action: str, quantity: float, order_type: OrderType,
                             limit_price: Optional[float] = None, stop_price: Optional[float] = None) -> tuple[Contract, Order]:
        contract = self.create_contract(
            SecurityType.EQUITY,
            symbol,
            exchange="SMART",
            currency="USD"
        )
        order = self.create_order(
            order_type,
            action,
            quantity,
            limit_price,
            stop_price
        )
        return contract, order


    def create_option_order(self, symbol: str, action: str, quantity: float, expiration: str, strike: float,
                             right: str, order_type: OrderType, limit_price: Optional[float] = None) -> tuple[Contract, Order]:
        contract = self.create_contract(
            SecurityType.OPTION,
            symbol,
            expiration=expiration,
            strike=strike,
            right=right
        )
        order = self.create_order(
            order_type,
            action,
            quantity,
            limit_price=limit_price
        )
        return contract, order


    def create_futures_order(self, symbol: str, action: str, quantity: float, expiration: str, order_type: OrderType,
                              limit_price: Optional[float] = None, exchange: str = "CME") -> tuple[Contract, Order]:
        contract = self.create_contract(
            SecurityType.FUTURE,
            symbol,
            exchange=exchange,
            expiration=expiration
        )
        order = self.create_order(
            order_type,
            action,
            quantity,
            limit_price=limit_price
        )
        return contract, order


    def create_forex_order(self, base_currency: str, quote_currency: str, action: str, quantity: float,
                           order_type: OrderType, limit_price: Optional[float] = None) -> tuple[Contract, Order]:
        contract = self.create_contract(
            SecurityType.CURRENCY,
            "",
            base_currency=base_currency,
            quote_currency=quote_currency
        )
        order = self.create_order(
            order_type,
            action,
            quantity,
            limit_price=limit_price
        )
        return contract, order
