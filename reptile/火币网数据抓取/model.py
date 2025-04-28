from sqlalchemy import Column, String, Date, Float, Integer, TIMESTAMP, create_engine, TEXT
from sqlalchemy.orm import declarative_base

ModelBase = declarative_base()  # <-元类

class k_link(ModelBase):
    __tablename__ = "k_link"

    # k线图数据间隔
    type = Column(String, primary_key=True)

    # 时间
    time = Column(TEXT, primary_key=True)

    # 开盘价
    openPrice = Column(Float)

    # 最高价
    maxPrice = Column(Float)

    # 最低价
    minPrice = Column(Float)

    # 收盘价
    closePrice = Column(Float)

    # 成交量
    dealCount = Column(Integer)

    # 所属币
    symbol = Column(String)
