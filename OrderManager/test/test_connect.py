import unittest
import time

from ibapi.client import EClient
from ibapi.wrapper import EWrapper

from common.variables import TWS_PAPER_PORT


class IBAPI(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def accountSummary(self, reqId: int, account: str, tag: str, value: str, currency: str):
        print("AccountSummary. ReqId:", reqId, "Account:", account, "Tag: ", tag, "Value:", value, "Currency:",
              currency)


def connect():
    app = IBAPI()
    app.connect('127.0.0.1', TWS_PAPER_PORT, 123)
    time.sleep(1)
    app.reqAccountSummary(9001, "All", 'NetLiquidation')
    app.run()
    time.sleep(1)
    app.disconnect()


class TestCase(unittest.TestCase):

    def test_connect(self):
        self.assertEqual(connect(), True)  # add assertion here



