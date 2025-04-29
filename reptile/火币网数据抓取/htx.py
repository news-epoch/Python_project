import datetime
import logging
import os
import sqlite3
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from zoneinfo import ZoneInfo

import ccxt
import pandas
import pytz
import requests
import urllib3
from dateutil.relativedelta import relativedelta
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib3.exceptions import InsecureRequestWarning

import model

urllib3.disable_warnings(InsecureRequestWarning)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import yaml

# 创建日志记录器
logger = logging.getLogger(__name__)

url = 'https://futures.htx.com.de/zh-cn/futures/copy_trading/home/'

rank_type_map = {
    '综合排名': 0,
    '收益率': 1,
    '收益额': 2,
    "跟单者人数": 4
}
close_type_map = {
    3: "止盈平仓",
    2: "手动平仓",
    11: "爆仓平仓",
    4: "止损平仓"
}
direction = {
            "short": "开空",
            "long": "开多"
        }

# order_type = {
#     '当前跟单': 0,
#     "历史带单": 1
# }

def load_yaml():
    """
    加载本地配置文件
    """
    BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
    with open(os.path.join(BASE_DIR, 'application.yml'), 'r', encoding='utf-8') as fp:
        a = fp.read()
        return yaml.load(a, Loader=yaml.FullLoader)


def time_diff(start_time: str = None, end_time: str = None):
    """
    对比时间
    """
    time1 = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    time2 = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    time_interval = relativedelta(time1, time2)
    return f"{time_interval.days}天{time_interval.hours}小时{time_interval.minutes}分"




def createSession(BASE_DIR):
    """
    创建sqlite数据库连接
    """
    db_config = {
        # "pool_size": "10",
        "echo": True,
        # "pool_pre_ping": True,
        # 'max_overflow': "20"
    }

    for i in range(0, 3):
        try:
            sqlite3.connect(BASE_DIR)
            # self.conn = create_engine(url=mysql_url, encoding='utf-8', echo=True, pool_size=8)
            conn = create_engine(url='sqlite:///' + BASE_DIR, **db_config)

            # print(f'连接信息：{self.conn}')
            # session = sessionmaker(bind=conn)()
            return conn
        except Exception as e:
            print(e)


def threadInseart(k, session):
    """
    多线程插入数据
    """
    session.add(k)
    session.commit()



class hbg:
    def __init__(self, rank_type: str = "综合排名"):
        self.rank_type = rank_type
        self.BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))


    def get_rank(self, page):
        params = {
            "rankType": rank_type_map.get(self.rank_type),
            "pageNo": page,
            "pageSize": 12,
            # "x-b3-traceid": "232338957620d3014ae8538c09ae7c7e"
        }
        headers = {
            "host": "futures.htx.com.de",
            "content-type": "application/json",
            "referer": "https://futures.htx.com.de/zh-cn/futures/copy_trading/home/",
        }
        url = 'https://futures.htx.com.de/-/x/hbg/v1/copytrading/rank'
        for i in range(1, 3):
            try:
                response = requests.session().get(url=url, params=params, headers=headers, verify=False)
                if response.status_code == requests.codes.ok:
                    return response.json()
                else:
                    logger.info(f"响应结果异常：{response.json()}")
            except Exception as e:
                logger.info(f"请求异常：{e}")
        return None



    def get_history_order_info(self, user_sign: str = None, nick_name: str = None, copy_user_num: str = None,
                               page: int = 1, page_size: int = 40):

        history_data = []
        session = sessionmaker(bind=createSession(os.path.join(self.BASE_DIR, "sqlite\\huobi.db")))()
        url = 'https://futures.htx.com.de/-/x/hbg/v1/copytrading/trader/open-matched-orders'
        params = {
            "queryType": 2,
            "pageNo": page,
            "pageSize": page_size,
            "userSign": user_sign
        }
        headers = {
            'accept': "application/json, text/plain, */*",
            "referer": "https://futures.htx.com.de/zh-cn/futures/copy_trading/following/trader/" + user_sign,
            # "sec-ch-ua:": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"'
        }
        check_num = 0
        for i in range(1, 6):
            try:
                response = requests.session().get(url=url, params=params, headers=headers, verify=False)
                if response.status_code == requests.codes.ok:
                    result = response.json()
                    if len(result['data']['orders']) > 0:
                        for order in result['data']['orders']:
                            temp = {
                                "id": order['id'],
                                "用户名": nick_name,
                                "合约": order['symbol'],
                                "方向": f"{direction.get(order['direction'])}",
                                "杠杆": f"{order['lever']}",
                                "开仓价格(USDT)": f"{order['openPrice']}",
                                "平仓价格(USDT)": order['closePrice'],
                                "收益率(%)": f"{round(float(order['profitRate']) * 100, 3)}%",
                                "止盈价格(USDT)": order['profitPrice'],
                                "平仓方式": close_type_map.get(order['closeType']) if close_type_map.get(
                                    order['closeType']) is not None else order['closeType'],
                                "开仓时间": datetime.datetime.utcfromtimestamp(order['openTime'] / 1000).replace(tzinfo=ZoneInfo("UTC")).astimezone(ZoneInfo("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S"),
                                "平仓时间": datetime.datetime.utcfromtimestamp(order['closeTime'] / 1000).replace(tzinfo=ZoneInfo("UTC")).astimezone(ZoneInfo("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S"),
                                "持仓时间": time_diff(datetime.datetime.utcfromtimestamp(order['closeTime'] / 1000).replace(tzinfo=ZoneInfo("UTC")).astimezone(ZoneInfo("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S"),datetime.datetime.utcfromtimestamp(order['openTime'] / 1000).replace(tzinfo=ZoneInfo("UTC")).astimezone(ZoneInfo("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S")),
                                "当前跟单人数": copy_user_num,
                                "开仓数量": f"{order['openAmount']}ETH",
                                "收益额(USDT)": f"{order['profit']}",
                                "带单分成(USDT)": order['followTakes'],
                                "跟单人数": order['followerCounts'],
                                "开仓手续费(USDT)": order['openFee'],
                                "平仓手续费(USDT)": order['closeFee'],
                            }
                            try:
                                sql = f"INSERT INTO 'trading_records' ('id', 'username', 'contract', 'direction', 'leverage', 'open_price', 'close_price', 'yield_rate', 'take_profit_price', 'close_method', 'open_time', 'close_time', 'duration', 'current_followers', 'position_size', 'profit', 'commission_fee', 'total_followers', 'open_fee', 'close_fee') " \
                                      f"VALUES ('{temp.get('id')}', '{temp.get('用户名')}', '{temp.get('合约')}', " \
                                      f"'{temp.get('方向')}', '{temp.get('杠杆')}', '{temp.get('开仓价格(USDT)')}', " \
                                      f"'{temp.get('平仓价格(USDT)')}', '{temp.get('收益率(%)')}', '{temp.get('止盈价格(USDT)')}', " \
                                      f"'{temp.get('平仓方式')}', '{temp.get('开仓时间')}', '{temp.get('平仓时间')}', '{temp.get('持仓时间')}', '{temp.get('当前跟单人数')}', " \
                                      f"'{temp.get('开仓数量')}', '{temp.get('收益额(USDT)')}', '{temp.get('带单分成(USDT)')}', '{temp.get('跟单人数')}', " \
                                      f"'{temp.get('开仓手续费(USDT)')}', '{temp.get('平仓手续费(USDT)')}');"
                                session.execute(text(sql))
                            except Exception as e:
                                check_num += 1

                            history_data.append(temp)
                    else:
                        return False
                    if check_num == len(result['data']['orders']):
                        return False
                    return True
            except Exception as e:
                logger.error(f"获取历史数据异常：{e}")

        return history_data
    def get_today_order_info(self, user_sign: str = None, nick_name: str = None, copy_user_num: str = None,
                             page: int = 1, page_size: int = 40):

        direction = {
            "short": "开空",
            "long": "开多"
        }

        today_data = []

        url = 'https://futures.htx.com.de/-/x/hbg/v1/copytrading/trader/open-unmatch-orders'
        params = {
            "pageNo": page,
            "pageSize": page_size,
            "userSign": user_sign
        }
        headers = {
            'accept': "application/json, text/plain, */*",
            "referer": "https://futures.htx.com.de/zh-cn/futures/copy_trading/following/trader/" + user_sign,
        }
        response = requests.session().get(url=url, params=params, headers=headers, verify=False)
        if response.status_code == requests.codes.ok:
            result = response.json()
            if len(result['data']['orders']) > 0:
                for order in result['data']['orders']:
                    today_data.append({
                        "用户名": str(nick_name),
                        "合约": order['symbol'],
                        "方向": f"{direction.get(order['direction'])}",
                        "杠杆": f"{order['lever']}",
                        "跟单人数": str(copy_user_num),
                        "开仓价格(USDT)": f"{order['openPrice']}",
                        "开仓数量": f"{order['openAmount']}ETH",
                        "保证金(USDT)": order['bondAmount'],
                        "收益额(USDT)": f"{order['openProfit']}",
                        "收益率(%)": f"{round(float(order['openProfitRate']) * 100, 3)}%",
                        "止盈价格(USDT)": order['stopProfitPrice'],
                        "开仓手续费(USDT)": order['openFee'],
                        "止损价格(USDT)": order['stopLossPrice'],
                        "预估爆仓价格(USDT)": order['explosionPrice'],
                        "开仓时间": datetime.datetime.utcfromtimestamp(order['openTime'] / 1000).strftime(
                            "%Y-%m-%d %H:%M:%S"),
                    })
        return today_data

    def startup(self, user_sign):
        history_page = 1
        today_page = 1
        history_data = []
        today_data = []
        session = sessionmaker(bind=createSession(os.path.join(self.BASE_DIR, "sqlite\\huobi.db")))()
        while True:
            temp = self.get_history_order_info(user_sign=user_sign['userSign'], nick_name=user_sign['nickName'], copy_user_num=user_sign['copyUserNum'], page=history_page, page_size=100)
            if temp is False:
                logger.info(f"{user_sign['nickName']}第{history_page}页历史带单数据已存入数据库")
                history_data.extend(session.execute(text(f"select * from trading_records where user_sign = {user_sign}")).fetchall())
                break
            if temp is True:
                logger.info(f"获取成功：{user_sign['nickName']}第{history_page}页的{len(temp)}条历史带单数据")
                history_page += 1
                time.sleep(1)
            else:
                logger.info(f"获取失败：{user_sign['nickName']}第{history_page}页《不存在》历史带单数据")
                break
        while True:
            temp = self.get_today_order_info(user_sign=user_sign['userSign'], nick_name=user_sign['nickName'], copy_user_num=user_sign['copyUserNum'], page=today_page, page_size=100)
            if len(temp) > 0:
                logger.info(f"获取成功：{user_sign['nickName']}第{today_page}页的{len(temp)}条当前带单数据")
                today_page += 1
                today_data.extend(temp)
                time.sleep(1)
            else:
                logger.info(f"获取失败：{user_sign['nickName']}第{today_page}页《不存在》当前带单数据")
                break
        return {"历史带单": history_data, "当前带单": today_data}

    def k_link(self,
               proxie_type: str = 'socks5',
               proxies_http_port: str = '10809',
               proxies_https_port: str = '10808',
               symbol: str = 'BTC/USDT',
               timeframe: str = '1d',
               start_time: str = '2023-01-01',
               end_time: str = '2023-01-31',
               exchange_name: str = 'binance'
               ):
        proxies = {
            'http': f'{proxie_type}://127.0.0.1:{proxies_http_port}',  # SOCKS5 代理
            'https': f'{proxie_type}://127.0.0.1:{proxies_https_port}',
        }
        # 将时间转换为毫秒时间戳
        since = int(datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S').timestamp() * 1000)
        end_time = int(datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S').timestamp() * 1000)

        session = sessionmaker(bind=createSession(os.path.join(self.BASE_DIR, "sqlite\\huobi.db")))()
        tf = 1
        if timeframe.__contains__("s"):
            tf = int(timeframe.replace("s", ""))
        elif timeframe.__contains__("m"):
            tf = int(timeframe.replace("s", "")) * 60
        elif timeframe.__contains__("h"):
            tf = int(timeframe.replace("s", "")) * 60 * 60
        elif timeframe.__contains__("d"):
            tf = int(timeframe.replace("d", "")) * 60 * 60 * 24

        sql = f"SELECT CASE WHEN total_records >= ((({end_time}/1000 - {since}/1000)/{tf})) THEN '记录数与时间跨度匹配' ELSE '记录数不匹配（应有 ' || ((({end_time}/1000 - {since}/1000)/{tf}) + 1) || ' 条，实际 ' || total_records || ' 条）' END AS check_result FROM (SELECT COUNT(*) AS total_records FROM k_link WHERE type='{timeframe}' and symbol = '{symbol}' and time BETWEEN {since} AND {end_time});"
        result = session.execute(text(sql)).fetchall()[0][0]
        logger.info(result)
        # logger.info(result[0])
        # result = "记录数与时间跨度匹配"
        # exchange = ccxt.binance({
        #     'proxies': {
        #         'http': f'{proxie_type}://127.0.0.1:{proxies_http_port}',  # SOCKS5 代理
        #         'https': f'{proxie_type}://127.0.0.1:{proxies_https_port}',
        #     }
        # })

        # 初始化交易所
        if result != "记录数与时间跨度匹配":
            logger.info(f"正在初始化交易所：{exchange_name}")
            exchange = getattr(ccxt, exchange_name)({
                'enableRateLimit': True,  # 启用请求频率限制
                "proxies": proxies
            })
            all_ohlcv = []
            while since < end_time:
                try:
                    logger.info(f"{symbol} K线图数据获取数据中.......")
                    ohlcv = None
                    # 获取数据
                    for i in range(1, 10):
                        try:
                            ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since)

                            break
                        except Exception as e:
                            logger.error(f"Error: {e}，重试10次")
                            time.sleep(10)
                            continue

                    if not ohlcv:
                        break  # 无更多数据
                    # 提取最后一条数据的时间戳，作为下次请求的起始点
                    last_timestamp = ohlcv[-1][0]
                    if last_timestamp >= end_time:
                        # 过滤超出结束时间的数据
                        filtered = [candle for candle in ohlcv if candle[0] < end_time]
                        all_ohlcv.extend(filtered)
                        break
                    else:
                        all_ohlcv.extend(ohlcv)

                    # 更新起始时间（避免重复）
                    since = last_timestamp + 1  # 加1毫秒

                    # 控制请求频率（根据交易所限制调整）
                    time.sleep(exchange.rateLimit / 500)  # 默认延迟

                except Exception as e:
                    logger.error(f"Error: {e}")
                    break
            logger.info("K线图数据获取完成")
            for oh in all_ohlcv:
                with ThreadPoolExecutor(max_workers=50) as executor:
                    k = model.k_link()
                    k.type = timeframe
                    k.time = oh[0]
                    k.openPrice = oh[1]
                    k.maxPrice = oh[2]
                    k.minPrice = oh[3]
                    k.closePrice = oh[4]
                    k.dealCount = oh[5]
                    k.symbol = symbol
                    executor.submit(threadInseart, k, session)
            return all_ohlcv
        else:
            logger.info(result)
            return session.execute(text(f"select time,openPrice,maxPrice,minPrice, closePrice,dealCount FROM k_link WHERE type='{timeframe}' and symbol = '{symbol}' and time BETWEEN {since} AND {end_time};")).fetchall()
    def k_link_profit(self,
                      open_price,
                      lever,
                      openAmount,
                      direction: str = "开多",
                      all_ohlcv: list = list()
                      ):
        """
        :param open_price:  开仓价格
        :param lever:  杠杆
        :param openAmount: 持仓数量
        :return:
        """
        prices = list()
        for i in all_ohlcv:
            prices.extend(i[1:5])

        if len(prices) == 0:
            return "0%", "0%", 0, 0

        max_price = max(prices)
        min_price = min(prices)

        # max_price = 1698.46
        #
        # min_price = 1698.46

        logger.info(f"开仓价格：{open_price}\n"
                    f"闭仓价格：{min_price}\n"
                    f"持仓数量：{openAmount}\n"
                    f"最大价格：{max_price}"
                    f"最小价格：{min_price}"
                    f"杠杆：{lever}\n"
                    f"手续费：{0.0006}\n")

        logger.info("计算最大收益率：")
        价值变化 = float(openAmount) * (float(open_price) - float(min_price))
        logger.info(f"价值变化：{价值变化}")
        总手续费 = float(openAmount) * (float(open_price) + float(min_price)) * 0.0006
        logger.info(f"总手续费：{总手续费}")
        净收益 = 价值变化 - 总手续费
        logger.info(f"净收益：{净收益}")
        保证金 = (float(openAmount) * float(open_price)) / 200
        logger.info(f"保证金：{保证金}")
        # 收益率 = f"{(净收益 / 保证金) * 100}%"
        # logger.info(f"验证公式1：{收益率}")
        max_rate_price = None
        min_rate_price = None

        if direction == "开空":
            logger.info(f"=====================开空=========================")
            max_rate_price = round(((float(openAmount) * (float(open_price) - float(min_price))) - (
                    float(openAmount) * (float(open_price) + float(min_price)) * 0.0006)) / (
                                           float(openAmount) * float(open_price) / int(lever)) * 100, 2)
            min_rate_price = round(((float(openAmount) * (float(open_price) - float(max_price))) - (
                    float(openAmount) * (float(open_price) + float(max_price)) * 0.0006)) / (
                                           float(openAmount) * float(open_price) / int(lever)) * 100, 2)
            logger.info(f"最大收益率：{max_rate_price}%")
            logger.info(f"最小收益率：{min_rate_price}%")
            max_rate_price = f"{max_rate_price}%"
            min_rate_price = f"{min_rate_price}%"
            logger.info("==============================================\n")
        elif direction == "开多":
            logger.info(f"=====================开多=========================")

            min_rate_price = round(((float(openAmount) * (float(min_price) - float(open_price))) - (
                    float(openAmount) * (float(open_price) + float(min_price)) * 0.0006)) / (
                                           float(openAmount) * float(open_price) / int(lever)) * 100, 2)
            max_rate_price = round(((float(openAmount) * (float(max_price) - float(open_price))) - (
                    float(openAmount) * (float(open_price) + float(max_price)) * 0.0006)) / (
                                           float(openAmount) * float(open_price) / int(lever)) * 100, 2)
            logger.info(f"最大收益率：{max_rate_price}%")
            logger.info(f"最小收益率：{min_rate_price}%")
            max_rate_price = f"{max_rate_price}%"
            min_rate_price = f"{min_rate_price}%"
            logger.info("==============================================\n")

        # print(
        #     f"验证公式：{round(((float(openAmount) * (float(open_price) - float(1698.46))) - (float(openAmount) * (float(open_price) + float(1698.46)) * 0.0006)) / (float(openAmount) * float(open_price) / int(lever)) * 100, 2)}")

        return max_rate_price, min_rate_price, max_price, min_price


    def k_link_profit(self, history_order_info: dict, timeframe: str):
        """
        根据k线图数据计算最大收益率和最小收益率
        """
        session = sessionmaker(bind=createSession(os.path.join(self.BASE_DIR, "sqlite\\huobi.db")))()
        open_price = history_order_info.get("开仓价格(USDT)")
        lever = history_order_info.get("杠杆")
        symbol = str(history_order_info.get("合约")).replace("-", "/")
        open_amount = str(history_order_info.get("开仓数量")).replace("ETH", "")
        start_timestamp = int(datetime.datetime.strptime(history_order_info.get("开仓时间"), '%Y-%m-%d %H:%M:%S').timestamp() * 1000)
        end_timestamp = int(datetime.datetime.strptime(history_order_info.get("平仓时间"), '%Y-%m-%d %H:%M:%S').timestamp() * 1000)

        # 计算最大价格 和 最小价格
        max_sql = f"select max(max(openPrice),max(maxPrice),max(minPrice),max(closePrice)) as max_value from k_link where type='{timeframe}' and symbol = '{symbol}' and time between {start_timestamp} and {end_timestamp};"
        min_sql = f"select min(min(openPrice),min(maxPrice),min(minPrice),min(closePrice)) as min_value from k_link where type='{timeframe}' and symbol = '{symbol}' and time between {start_timestamp} and {end_timestamp};"
        max_price = session.execute(text(max_sql)).fetchall()[0][0]

        min_price = session.execute(text(min_sql)).fetchall()[0][0]
        logger.info(f"开仓价格：{open_price}\n"
                    f"持仓数量：{open_amount}\n"
                    f"最大价格：{max_price}\n"
                    f"最小价格：{min_price}\n"
                    f"杠杆：{lever}\n"
                    f"手续费：{0.0006}\n")
        max_rate_price = 0
        min_rate_price = 0
        if history_order_info['方向'] == "开空":
            logger.info(f"=====================开空=========================")
            max_rate_price = round(((float(open_amount) * (float(open_price) - float(min_price))) - (
                    float(open_amount) * (float(open_price) + float(min_price)) * 0.0006)) / (
                                           float(open_amount) * float(open_price) / int(lever)) * 100, 2)
            min_rate_price = round(((float(open_amount) * (float(open_price) - float(max_price))) - (
                    float(open_amount) * (float(open_price) + float(max_price)) * 0.0006)) / (
                                           float(open_amount) * float(open_price) / int(lever)) * 100, 2)
            logger.info(f"最大收益率：{max_rate_price}%")
            logger.info(f"最小收益率：{min_rate_price}%")
            max_rate_price = f"{max_rate_price}%"
            min_rate_price = f"{min_rate_price}%"
            logger.info("==============================================\n")
        elif history_order_info['方向'] == "开多":
            logger.info(f"=====================开多=========================")
            min_rate_price = round(((float(open_amount) * (float(min_price) - float(open_price))) - (float(open_amount) * (float(open_price) + float(min_price)) * 0.0006)) / (float(open_amount) * float(open_price) / int(lever)) * 100, 2)
            max_rate_price = round(((float(open_amount) * (float(max_price) - float(open_price))) - (
                    float(open_amount) * (float(open_price) + float(max_price)) * 0.0006)) / (float(open_amount) * float(open_price) / int(lever)) * 100, 2)
            logger.info(f"最大收益率：{max_rate_price}%")
            logger.info(f"最小收益率：{min_rate_price}%")
            max_rate_price = f"{max_rate_price}%"
            min_rate_price = f"{min_rate_price}%"
            logger.info("==============================================\n")
        history_order_info['最大收益率'] = max_rate_price
        history_order_info['最小收益率'] = min_rate_price
        history_order_info['最大价格'] = max_price
        history_order_info['最小价格'] = min_price

        return history_order_info
    def comouter_yield(self,
                       historical_leads_file_path,
                       timeframe,
                       proxie_type,
                       proxies_http_port,
                       proxies_https_port,
                       exchange_name,
                       max_workers: int = 5):
        """
        构建获取数据
        """

        pd1 = pandas.read_excel(historical_leads_file_path)

        k_data_list = dict()
        export_data = list()
        # keys = list()  # 时间类型
        # 获取不同类型的最大时间和最小时间
        # if start_time == "" or end_time == "" or end_time == None or start_time == None:
        #     start_timestamp = int(datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S').timestamp() * 1000)
        #     time1 = pd1.groupby("合约")['开仓时间'].apply(list).to_dict()
        #     time2 = pd1.groupby("合约")['平仓时间'].apply(list).to_dict()
        #     for key, value in time1.items():
        #         time2.get(key).extend(value)
        #         keys.append(str(key).replace("-", "/") + "_" +
        #                     datetime.datetime.strptime(str(min(time2.get(key))),"%Y-%m-%d %H:%M:%S").strftime("%Y%m%d%H%M%S") + "_" +
        #                     datetime.datetime.strptime(str(max(time2.get(key))),"%Y-%m-%d %H:%M:%S").strftime("%Y%m%d%H%M%S"))
        futures = []
        with ThreadPoolExecutor(max_workers=50) as executor:
            for i in pd1.index.values:
                data = pd1.loc[i].to_dict()
                result = self.k_link(proxie_type, proxies_http_port, proxies_https_port, str(pd1.loc[i]['合约']).replace("-", "/"), timeframe, pd1.loc[i]['开仓时间'], pd1.loc[i]['平仓时间'], exchange_name)
                if len(result) == 0:
                    data['最大收益率']= "当前时间段未获取到K线图数据"
                    data['最小收益率']= "当前时间段未获取到K线图数据"
                    data['最大价格']= "当前时间段未获取到K线图数据"
                    data['最小价格'] = "当前时间段为获取到K线图数据"
                    export_data.append(data)
                    continue
                futures.append(executor.submit(self.k_link_profit, data, timeframe))
            for future in as_completed(futures):
                export_data.append(future.result())
        return export_data

        # with ThreadPoolExecutor(max_workers=max_workers) as executor:
        #     for key in keys:
        #         logger.info(f"提交任务{key}")
        #         k_data_list[key] = executor.submit(self.k_link,
        #                                            proxie_type,
        #                                            proxies_http_port,
        #                                            proxies_https_port,
        #                                            key.split("_")[0],
        #                                            timeframe,
        #                                            str(datetime.datetime.strptime(key.split("_")[1], "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")),
        #                                            str(datetime.datetime.strptime(key.split("_")[2], "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")),
        #                                            exchange_name)
        #     as_completed(k_data_list.values())
        #     for key,value in k_data_list.items():
        #         logger.info(f"获取任务{key}的结果")
        #         k_data_list[key] = value.result()
        # futures = []
        # with ThreadPoolExecutor(max_workers=50) as executor:
        #     for i in pd1.index.values:
        #         data = pd1.loc[i].to_dict()
        #         # 查询K线图数据
        #         # ohlcv = list()
        #         futures.append(executor.submit(self.thread_computer_yield,data, k_data_list))
        #     for future in as_completed(futures):
        #         export_data.append(future.result())

            # for key, value in k_data_list.items():
            #     df = pandas.DataFrame(value, columns=["时间", "开盘价", "最高价", "最低价", "收盘价", "成交量"])
            #     # 时间戳转换为 UTC 时间
            #     df["时间"] = pandas.to_datetime(df["时间"], unit="ms")
            #     if str(key).split("_")[0] == (str(data['合约']).replace('-', '/')):
            #         logger.info(
            #             f"查询{data['开仓时间']}~{data['平仓时间']}：{str(data['合约']).replace('-', '/')}K线图数据")
            #         mask = df['时间'].between(data['开仓时间'], data['平仓时间'])
            #         ohlcv = df[mask].values.tolist()
            #
            # data['最大收益率'], data['最小收益率'], data['最大价格'], data['最小价格'] = self.k_link_profit(
            #     open_price=data['开仓价格(USDT)'],
            #     lever=data['杠杆'],
            #     direction=data["方向"],
            #     openAmount=str(data['开仓数量']).replace("ETH", ''),
            #     all_ohlcv=ohlcv
            # )


    def thread_computer_yield(self, data, all_ohlcv):
        ohlcv = None
        for key, value in all_ohlcv.items():
            if value is []:
                continue
            logger.info(f"获取{key}的数据")
            df = pandas.DataFrame(value, columns=["时间", "开盘价", "最高价", "最低价", "收盘价", "成交量"])
            # 时间戳转换为 UTC 时间
            # logger.info(df["时间"])
            df["时间"] = pandas.to_datetime(df["时间"], unit="ms").dt.tz_localize('UTC').dt.tz_convert(
                'Asia/Shanghai').dt.tz_localize(None)

            if str(key).split("_")[0] == (str(data['合约']).replace('-', '/')):
                logger.info(f"查询{data['开仓时间']}~{data['平仓时间']}：{str(data['合约']).replace('-', '/')}K线图数据")
                mask = df['时间'].between(data['开仓时间'], data['平仓时间'])
                ohlcv = df[mask].values.tolist()

        data['最大收益率'], data['最小收益率'], data['最大价格'], data['最小价格'] = self.k_link_profit(
            open_price=data['开仓价格(USDT)'],
            lever=data['杠杆'],
            direction=data["方向"],
            openAmount=str(data['开仓数量']).replace("ETH", ''),
            all_ohlcv=ohlcv
        )
        return data