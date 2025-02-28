from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class TestTable(Base):
    __tablename__ = 'test'
    trade_id = Column(Integer, primary_key=True)
    ticker = Column(String)
    side = Column(String)
    volume = Column(Integer)
    price = Column(Float)

