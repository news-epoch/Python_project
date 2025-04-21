import datetime
import logging
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from zoneinfo import ZoneInfo

import ccxt
import pandas
import requests
import urllib3
from dateutil.relativedelta import relativedelta
from urllib3.exceptions import InsecureRequestWarning

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


# order_type = {
#     '当前跟单': 0,
#     "历史带单": 1
# }

def load_yaml():
    BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
    with open(os.path.join(BASE_DIR, 'application.yml'), 'r', encoding='utf-8') as fp:
        a = fp.read()
        return yaml.load(a, Loader=yaml.FullLoader)


def time_diff(start_time: str = None, end_time: str = None):
    time1 = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    time2 = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    time_interval = relativedelta(time2, time1)
    return f"{time_interval.days}天{time_interval.hours}小时{time_interval.minutes}分"


def computer_rank_rate():
    """
    计算最大收益率
    :return:
    """


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

    def create_driver(self, user_sign):
        history_data = []
        today_data = []
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 设置无界面浏览器，浏览器不在标识被控制
        chrome_options.add_argument('--disable-gpu')  # 设置无界面浏览器
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chromebro = webdriver.Chrome(
            service=Service(executable_path=os.path.join(self.BASE_DIR, r'utils/chromedriver.exe')),
            options=chrome_options)  # 创建网页对象
        chromebro.set_page_load_timeout(1800)

        chromebro.get("https://futures.htx.com.de/zh-cn/futures/copy_trading/following/trader/" + user_sign)

        order_types = ['历史带单', '当前带单']

        # 点击带单选项
        logger.info("================================")
        for order_type in order_types:
            username = chromebro.find_element(By.XPATH, "//label[contains(@class, 'user-name')]").text
            user_sub = chromebro.find_element(By.XPATH, "//ul[contains(@class, 'user-sub-data')]/li/label").text

            if order_type == '历史带单':
                logger.info("获取历史带单数据")
                chromebro.find_element(By.XPATH, f"//li[contains(text(),'{order_type}')]").click()
                time.sleep(60)
                while True:
                    # 获取数量
                    orders = chromebro.find_elements(By.XPATH,
                                                     "//div[@class = 'history-following-wrapper']/div[1]/table/tbody/tr")

                    if len(orders) < 1:
                        logger.info("不存在历史带单数据条停止获取数据")
                        break
                    for i in range(1, len(orders) + 1):
                        logger.info(f"获取第{i}条带单数据")
                        order_info = dict()
                        element1 = f"//div[@class = 'history-following-wrapper']/div[1]/table/tbody/tr[{i}]"
                        element2 = f"//div[@class = 'history-following-wrapper']/div[1]/table/tbody/tr[{i + 1}]"
                        order_info['姓名'] = username
                        order_info['跟单人数'] = user_sub
                        order_info['带单类型'] = order_type

                        # 点击详情
                        chromebro.find_element(By.XPATH,
                                               element1 + "/td[@class='sticky border']/div[1]/span[1]").click()
                        time.sleep(2)

                        order_info['合约'] = chromebro.find_element(By.XPATH, element1 + "/td[1]/span").text
                        order_info['方向/杠杆'] = chromebro.find_element(By.XPATH, element1 + "/td[2]/span").text
                        order_info['开仓价格(USDT)'] = chromebro.find_element(By.XPATH, element1 + "/td[3]/span").text
                        order_info['开仓数量'] = chromebro.find_element(By.XPATH, element1 + "/td[4]/span").text
                        order_info['平仓价格(USDT)'] = chromebro.find_element(By.XPATH, element1 + "/td[5]/span").text
                        order_info['收益额(USDT)'] = chromebro.find_element(By.XPATH, element1 + "/td[6]/span").text
                        order_info['跟单人数'] = chromebro.find_element(By.XPATH, element1 + "/td[7]/span").text

                        order_info['止盈价格(USDT)'] = chromebro.find_element(By.XPATH,
                                                                              element2 + "/td[1]/div/div[1]/div[2]/span").text
                        order_info['开仓手续费(USDT)'] = chromebro.find_element(By.XPATH,
                                                                                element2 + "/td[1]/div/div[2]/div[2]/span").text
                        order_info['平仓手续费(USDT)'] = chromebro.find_element(By.XPATH,
                                                                                element2 + "/td[1]/div/div[3]/div[2]/span").text
                        order_info['平仓方式'] = chromebro.find_element(By.XPATH,
                                                                        element2 + "/td[1]/div/div[4]/div[2]/span").text
                        order_info['开仓时间'] = chromebro.find_element(By.XPATH,
                                                                        element2 + "/td[1]/div/div[5]/div[2]/span").text
                        order_info['平仓时间'] = chromebro.find_element(By.XPATH,
                                                                        element2 + "/td[1]/div/div[6]/div[2]/span").text

                        chromebro.find_element(By.XPATH,
                                               element1 + "/td[@class='sticky border']/div[1]/span[1]").click()
                        # 页面滚动
                        chromebro.execute_script("arguments[0].scrollIntoView();", chromebro.find_element(By.XPATH,
                                                                                                          element1 + "/td[@class='sticky border']/div[1]/span[1]"))
                        time.sleep(1)
                        logger.info(order_info)
                        history_data.append(order_info)
                    try:
                        chromebro.find_element(By.XPATH,
                                               "//section[@class='pagination-bar']/button[@type ='button' and @class ='pagination-arrow']").click()
                        time.sleep(10)
                        chromebro.execute_script("arguments[0].scrollIntoView();", chromebro.find_element(By.XPATH,
                                                                                                          f"//li[contains(text(),'{order_type}')]"))
                        logger.info("下一页")
                    except Exception as e:
                        logger.info(e)
                        logger.info("最后一页")
                        break
            elif order_type == '当前带单':
                chromebro.find_element(By.XPATH, f"//li[contains(text(),'{order_type}')]").click()
                time.sleep(60)
                logger.info("获取当前带单数据")
                while True:
                    # 获取数量
                    orders = chromebro.find_elements(By.XPATH,
                                                     "//div[@class = 'table-scroll-wrapper']/div[1]/table/tbody/tr")
                    if len(orders) < 1:
                        logger.info("不存在当前带单数据条跳过")
                        break

                    for i in range(1, len(orders) + 1):
                        order_info = dict()
                        element1 = f"//div[@class = 'table-scroll-wrapper']/div[1]/table/tbody/tr[{i}]"
                        element2 = f"//div[@class = 'table-scroll-wrapper']/div[1]/table/tbody/tr[{i + 1}]"
                        order_info['姓名'] = username
                        order_info['跟单人数'] = user_sub
                        order_info['带单类型'] = order_type

                        # 点击详情
                        logger.info("点击详情")
                        chromebro.find_element(By.XPATH, element1 + "/td[@class='sticky border']").click()
                        time.sleep(1)

                        order_info['合约'] = chromebro.find_element(By.XPATH, element1 + "/td[1]/span").text
                        order_info['方向/杠杆'] = chromebro.find_element(By.XPATH, element1 + "/td[2]/span").text
                        order_info['开仓价格(USDT)'] = chromebro.find_element(By.XPATH, element1 + "/td[3]/span").text
                        order_info['开仓数量'] = chromebro.find_element(By.XPATH, element1 + "/td[4]/span").text
                        order_info['保证金(USDT)'] = chromebro.find_element(By.XPATH, element1 + "/td[5]/span").text
                        order_info['收益额(USDT)'] = chromebro.find_element(By.XPATH, element1 + "/td[6]/span").text

                        order_info['止盈价格(USDT)'] = chromebro.find_element(By.XPATH,
                                                                              element2 + "/td[1]/div/div[1]/div[2]/span").text
                        order_info['止损价格(USDT)'] = chromebro.find_element(By.XPATH,
                                                                              element2 + "/td[1]/div/div[2]/div[2]/span").text
                        order_info['预估爆仓价格(USDT)'] = chromebro.find_element(By.XPATH,
                                                                                  element2 + "/td[1]/div/div[3]/div[2]/span").text
                        order_info['开仓手续费(USDT)'] = chromebro.find_element(By.XPATH,
                                                                                element2 + "/td[1]/div/div[4]/div[2]/span").text
                        order_info['开仓时间'] = chromebro.find_element(By.XPATH,
                                                                        element2 + "/td[1]/div/div[5]/div[2]/span").text
                        # order_info['平仓时间'] = chromebro.find_element(By.XPATH, element2+"/td[1]/div/div[1]/div[6]/span").text

                        chromebro.find_element(By.XPATH, element1 + "/td[@class='sticky border']").click()
                        today_data.append(order_info)
                    # 翻页
                    try:
                        chromebro.find_element(By.XPATH,
                                               "//section[@class='pagination-bar']/button[@type ='button' and @class ='pagination-arrow']").click()
                        time.sleep(10)
                        chromebro.execute_script("arguments[0].scrollIntoView();", chromebro.find_element(By.XPATH,
                                                                                                          f"//li[contains(text(),'{order_type}')]"))
                    except Exception as e:
                        logger.info("最后一页")
                        break

        logger.info("================================")
        chromebro.close()
        return {"历史带单": history_data, "当前带单": today_data}

    def download_driver(self):
        # 自动下载与Chrome版本匹配的Chromedriver
        driver_path = ChromeDriverManager().install()
        logger.info(driver_path)
        # driver = webdriver.Chrome(service=Service(driver_path))

    def get_history_order_info(self, user_sign: str = None, nick_name: str = None, copy_user_num: str = None,
                               page: int = 1, page_size: int = 20):

        direction = {
            "short": "开空",
            "long": "开多"
        }

        history_data = []

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
        response = requests.session().get(url=url, params=params, headers=headers, verify=False)
        if response.status_code == requests.codes.ok:
            result = response.json()
            if len(result['data']['orders']) > 0:
                for order in result['data']['orders']:
                    history_data.append({
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
                        "持仓时间": time_diff(datetime.datetime.utcfromtimestamp(order['closeTime'] / 1000).replace(tzinfo=ZoneInfo("UTC")).astimezone(ZoneInfo("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S"),
                            datetime.datetime.utcfromtimestamp(order['openTime'] / 1000).replace(tzinfo=ZoneInfo("UTC")).astimezone(ZoneInfo("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S")),
                        "当前跟单人数": copy_user_num,
                        "开仓数量": f"{order['openAmount']}ETH",
                        "收益额(USDT)": f"{order['profit']}",
                        "带单分成(USDT)": order['followTakes'],
                        "跟单人数": order['followerCounts'],
                        "开仓手续费(USDT)": order['openFee'],
                        "平仓手续费(USDT)": order['closeFee'],
                    })

        return history_data

    def get_today_order_info(self, user_sign: str = None, nick_name: str = None, copy_user_num: str = None,
                             page: int = 1, page_size: int = 20):

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

        while True:
            temp = self.get_history_order_info(user_sign=user_sign['userSign'], nick_name=user_sign['nickName'],
                                               copy_user_num=user_sign['copyUserNum'], page=history_page, page_size=100)
            if len(temp) > 0:
                logger.info(f"获取成功：{user_sign['nickName']}第{history_page}页的{len(temp)}条历史带单数据")
                history_page += 1
                history_data.extend(temp)
                time.sleep(1)
            else:
                logger.info(f"获取失败：{user_sign['nickName']}第{history_page}页《不存在》当前带单数据")
                break
        while True:
            temp = self.get_today_order_info(user_sign=user_sign['userSign'], nick_name=user_sign['nickName'],
                                             copy_user_num=user_sign['copyUserNum'], page=today_page, page_size=100)

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
               exchange_name: str = 'binance',
               ):
        proxies = {
            'http': f'{proxie_type}://127.0.0.1:{proxies_http_port}',  # SOCKS5 代理
            'https': f'{proxie_type}://127.0.0.1:{proxies_https_port}',
        }

        # exchange = ccxt.binance({
        #     'proxies': {
        #         'http': f'{proxie_type}://127.0.0.1:{proxies_http_port}',  # SOCKS5 代理
        #         'https': f'{proxie_type}://127.0.0.1:{proxies_https_port}',
        #     }
        # })

        # 初始化交易所
        logger.info(f"正在初始化交易所：{exchange_name}")
        exchange = getattr(ccxt, exchange_name)({
            'enableRateLimit': True,  # 启用请求频率限制
            "proxies": proxies
        })

        # 将时间转换为毫秒时间戳
        since = int(datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S').timestamp() * 1000)
        end_time = int(datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S').timestamp() * 1000)

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

        return all_ohlcv

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
            # max_price = max([float(i[1]), float(i[2]), float([3]), float(i[4])])
            # min_price = min([float(i[1]), float(i[2]), float([3]), float(i[4])])
            # max_price = max(i[1:5])
            # min_price = min(i[1:5])
            prices.extend(i[1:5])
            # i.append(f"{round(((float(openAmount) * (float(open_price) - float(max_price))) - (float(openAmount) * (float(open_price) + float(max_price)) * 0.0006))/(float(openAmount) * float(open_price) / int(lever)) * 100, 2)}%")
            # i.append(f"{round(((float(openAmount) * (float(open_price) - float(min_price))) - (float(openAmount) * (float(open_price) + float(min_price)) * 0.0006))/(float(openAmount) * float(open_price) / int(lever)) * 100,2)}%")
            # i.append(f"{round((open_price-max_price)/open_price * lever * 100,2)}%")
            # i.append(f"{round((open_price-min_price)/open_price * lever * 100,2)}%")
        if len(prices) == 0:
            return "0%", "0%", 0, 0
        # max_price = max(prices)
        # min_price = min(prices)

        max_price = 1698.46

        min_price = 1698.46

        logger.info(f"开仓价格：{open_price}\n"
                    f"闭仓价格：{min_price}\n"
                    f"持仓数量：{openAmount}\n"
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

    def comouter_yield(self,
                       historical_leads_file_path,
                       start_time,
                       end_time,
                       timeframe,
                       proxie_type,
                       proxies_http_port,
                       proxies_https_port,
                       exchange_name):

        pd1 = pandas.read_excel(historical_leads_file_path)

        k_data_list = dict()
        export_data = list()
        keys = list()  # 时间类型
        # 获取不同类型的最大时间和最小时间
        if start_time == "" or end_time == "" or end_time == None or start_time == None:
            time1 = pd1.groupby("合约")['开仓时间'].apply(list).to_dict()
            time2 = pd1.groupby("合约")['平仓时间'].apply(list).to_dict()
            for key, value in time1.items():
                time2.get(key).extend(value)
                keys.append(str(key).replace("-", "/") + "_" +
                            datetime.datetime.strptime(str(min(time2.get(key))),"%Y-%m-%d %H:%M:%S").strftime("%Y%m%d%H%M%S") + "_" +
                            datetime.datetime.strptime(str(max(time2.get(key))),"%Y-%m-%d %H:%M:%S").strftime("%Y%m%d%H%M%S"))
        print(keys)
        with ThreadPoolExecutor(max_workers=5) as executor:
            for key in keys:
                logger.info(f"提交任务{key}")
                k_data_list[key] = executor.submit(self.k_link,
                                                   proxie_type,
                                                   proxies_http_port,
                                                   proxies_https_port,
                                                   key.split("_")[0],
                                                   timeframe,
                                                   str(datetime.datetime.strptime(key.split("_")[1], "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")),
                                                   str(datetime.datetime.strptime(key.split("_")[2], "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")),
                                                   exchange_name)
            as_completed(k_data_list.values())
            for key,value in k_data_list.items():
                logger.info(f"获取任务{key}的结果")
                k_data_list[key] = value.result()
        futures = []
        with ThreadPoolExecutor(max_workers=50) as executor:
            for i in pd1.index.values:
                data = pd1.loc[i].to_dict()
                # 查询K线图数据
                # ohlcv = list()
                futures.append(executor.submit(self.thread_computer_yield,data, k_data_list))
            for future in as_completed(futures):
                export_data.append(future.result())

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

        return export_data
    def thread_computer_yield(self, data, all_ohlcv):
        ohlcv = None
        for key, value in all_ohlcv.items():
            df = pandas.DataFrame(value, columns=["时间", "开盘价", "最高价", "最低价", "收盘价", "成交量"])
            # 时间戳转换为 UTC 时间
            df["时间"] = pandas.to_datetime(df["时间"], unit="ms")
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