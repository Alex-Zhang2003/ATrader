from ibapi.client import EClient
from ibapi.wrapper import EWrapper

from OrderManager.core.OrderFactory import OrderFactory


class OrderManager(EWrapper, EClient):

    def __init__(self):
        EClient.__init__(self, self)
        self.order_id = None
        self.order_factory = OrderFactory(self)

    def nextValidId(self, orderId: int):
        if self.order_id is None or self.order_id < orderId:
            self.order_id = orderId

    def orderStatus(self, orderId, status, filled, remaining, avgPrice, permId, parentId, lastFillPrice, clientId,
                    whyHeld, mktCapPrice):
        pass

    def error(self, reqId, errorCode, errorString, **kwargs):
        pass
