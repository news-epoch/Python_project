import datetime
import os
import time

from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

from htx import createSession

if __name__ == '__main__':
    # t = 1743436800000
    # local_time = time.localtime(t)
    # print(time.strftime("%Y-%m-%d %H:%M:%s", local_time))
    # date = datetime.datetime.utcfromtimestamp(t/1000) + datetime.timedelta(hours=8)
    # print(date.timestamp())
    # print(date.strftime("%Y-%m-%d %H:%M:%S"))
    sql = f"select time,openPrice,maxPrice,minPrice, closePrice,dealCount FROM k_link WHERE type='5m' and time BETWEEN 1743436800000 AND 1743438900000"
    sql = "SELECT CASE WHEN total_records = ((1743438900000/1000 - 1743436800000/1000)/300 + 1) THEN '记录数与时间跨度匹配' ELSE '记录数不匹配（应有 ' || ((1743438900000/1000 - 1743436800000/1000)/300 + 1) || ' 条，实际 ' || total_records || ' 条）' END AS check_result FROM (SELECT COUNT(*) AS total_records FROM k_link WHERE type='5m' and time BETWEEN 1743436800000 AND 1743438900000);"
    # sql = "SELECT CASE WHEN total_records = ((1745577655000/1000 - 1737508263000/1000)/1*24*60*60 + 1) THEN '记录数与时间跨度匹配' ELSE '记录数不匹配（应有 ' || ((1745577655000/1000 - 1737508263000/1000)/1*24*60*60 + 1) || ' 条，实际 ' || total_records || ' 条）' END AS check_result FROM (SELECT COUNT(*) AS total_records FROM k_link WHERE type='1d' and time BETWEEN 1737508263000 AND 1745577655000);"
    # sql = "INSERT INTO 'trading_records' ('id', 'username', 'contract', 'direction', 'leverage', 'open_price', 'close_price', 'yield_rate', 'take_profit_price', 'close_method', 'open_time', 'close_time', 'duration', 'current_followers', 'position_size', 'profit', 'commission_fee', 'total_followers', 'open_fee', 'close_fee') VALUES (1, '1', '1', '1', 1, 1, 1, 1, 1, '1', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1);"
    session = sessionmaker(bind=createSession(".\sqlite\\huobi.db"))()
    sql = "select * from k_link"
    try:
        print(session.execute(text(sql)).fetchall())
    except Exception as e:
        print("异常："+e.__str__())

    # print(data[0])