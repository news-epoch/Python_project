
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float

import tools

ModelBase = declarative_base()



class trader_info(ModelBase):
    __tablename__ = 'trader_info'
    # 股票代码
    security = Column(String(length=20), primary_key=True)
    # 股票名称
    security_name = Column(String(length=30))
    # 委托编码
    trader_code = Column(String(length=30), primary_key=True)
    # 委托类型
    trader_type = Column(String(length=30), primary_key=True)
    # 买单数量
    amount = Column(Integer)
    # 买单价格
    price = Column(Float)
    # 买单挂单时间
    trader_time = Column(DateTime)
    # 买单状态
    status = Column(String(length=100))

class relation_trader(ModelBase):
    __tablename__ = 'relation_trader'
    # 监控的委托编码
    monitor_trader_code = Column(String(length=20), primary_key=True)

    # 反向做t的委托编码
    reverse_trader_code = Column(String(length=20))

    # # 做t是否成功 0表示失败，1表示成功
    do_t_status = Column(Integer)

def 创建库表():
    # 创建数据库引擎，指定数据库文件路径
    engine = create_engine('sqlite:///sqlite/scene.db')

    # 创建所有声明的表
    ModelBase.metadata.create_all(engine)

def 数据库测试():
    application = tools.读取配置文件()
    session = tools.创建数据库连接并且返回操作字段(application.get('db').get('url'))
    print(session.query(relation_trader).filter(relation_trader.monitor_trader_code == '1').count())



if __name__ == '__main__':

    数据库测试()