import unittest

import pandas as pd

from Database.core.connection import create_conn_engine, create_session
from Database.tables.test import TestTable


class TestCase(unittest.TestCase):

    def test_connect(self):
        engine = create_conn_engine()
        session = create_session(engine)

        with session() as db_session:
            # new_trade = TestTable(trade_id=1, ticker='AAPL', side='B', volume=100, price=140.4)
            # db_session.add(new_trade)
            # db_session.commit()

            qry = db_session.query(TestTable)
            df = pd.read_sql(qry.statement, db_session.bind)
        self.assertEqual(True, True)