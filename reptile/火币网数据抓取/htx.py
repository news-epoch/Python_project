import datetime
import os
import sys
import time

import ccxt
from ccxt.base.exchange import Exchange
import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(InsecureRequestWarning)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import yaml

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


class hbg:
    def __init__(self, rank_type: str = "综合排名"):
        self.rank_type = rank_type
        self.BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))

    def get_rank(self, page):
        params = {
            "rankType": rank_type_map.get(self.rank_type),
            "pageNo": page,
            "pageSize": 12,
            "x-b3-traceid": "d1546a6caf35514cecf3ee7d2bcd17ad"
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
                    print(f"响应结果异常：{response.json()}")
            except Exception as e:
                print(f"请求异常：{e}")
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
        print("================================")
        for order_type in order_types:
            username = chromebro.find_element(By.XPATH, "//label[contains(@class, 'user-name')]").text
            user_sub = chromebro.find_element(By.XPATH, "//ul[contains(@class, 'user-sub-data')]/li/label").text

            if order_type == '历史带单':
                print("获取历史带单数据")
                chromebro.find_element(By.XPATH, f"//li[contains(text(),'{order_type}')]").click()
                time.sleep(60)
                while True:
                    # 获取数量
                    orders = chromebro.find_elements(By.XPATH,
                                                     "//div[@class = 'history-following-wrapper']/div[1]/table/tbody/tr")

                    if len(orders) < 1:
                        print("不存在历史带单数据条停止获取数据")
                        break
                    for i in range(1, len(orders) + 1):
                        print(f"获取第{i}条带单数据")
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
                        print(order_info)
                        history_data.append(order_info)
                    try:
                        chromebro.find_element(By.XPATH,
                                               "//section[@class='pagination-bar']/button[@type ='button' and @class ='pagination-arrow']").click()
                        time.sleep(10)
                        chromebro.execute_script("arguments[0].scrollIntoView();", chromebro.find_element(By.XPATH,
                                                                                                          f"//li[contains(text(),'{order_type}')]"))
                        print("下一页")
                    except Exception as e:
                        print(e)
                        print("最后一页")
                        break
            elif order_type == '当前带单':
                chromebro.find_element(By.XPATH, f"//li[contains(text(),'{order_type}')]").click()
                time.sleep(60)
                print("获取当前带单数据")
                while True:
                    # 获取数量
                    orders = chromebro.find_elements(By.XPATH,
                                                     "//div[@class = 'table-scroll-wrapper']/div[1]/table/tbody/tr")
                    if len(orders) < 1:
                        print("不存在当前带单数据条跳过")
                        break

                    for i in range(1, len(orders) + 1):
                        order_info = dict()
                        element1 = f"//div[@class = 'table-scroll-wrapper']/div[1]/table/tbody/tr[{i}]"
                        element2 = f"//div[@class = 'table-scroll-wrapper']/div[1]/table/tbody/tr[{i + 1}]"
                        order_info['姓名'] = username
                        order_info['跟单人数'] = user_sub
                        order_info['带单类型'] = order_type

                        # 点击详情
                        print("点击详情")
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
                        print("最后一页")
                        break

        print("================================")
        chromebro.close()
        return {"历史带单": history_data, "当前带单": today_data}

    def download_driver(self):
        # 自动下载与Chrome版本匹配的Chromedriver
        driver_path = ChromeDriverManager().install()
        print(driver_path)
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
                        "跟单人数": copy_user_num,
                        "合约": order['symbol'],
                        "方向/杠杆": f"{direction.get(order['direction'])}/{order['lever']}X · 全仓",
                        "开仓价格(USDT)": f"{order['openPrice']}",
                        "开仓数量": f"{order['openAmount']}ETH",
                        "平仓价格(USDT)": order['closePrice'],
                        "收益额(USDT)": f"{order['profit']}%({order['profitRate']}%)",
                        "带单分成(USDT)": order['followTakes'],
                        "跟单人数": order['followerCounts'],
                        "止盈价格(USDT)": order['profitPrice'],
                        "开仓手续费(USDT)": order['openFee'],
                        "平仓手续费(USDT)": order['closeFee'],
                        "平仓方式": close_type_map.get(order['closeType']) if close_type_map.get(
                            order['closeType']) is not None else order['closeType'],
                        "开仓时间": datetime.datetime.utcfromtimestamp(order['openTime'] / 1000).strftime(
                            "%Y-%m-%d %H:%M:%S"),
                        "平仓时间": datetime.datetime.utcfromtimestamp(order['closeTime'] / 1000).strftime(
                            "%Y-%m-%d %H:%M:%S"),
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
                        "跟单人数": str(copy_user_num),
                        "合约": order['symbol'],
                        "方向/杠杆": f"{direction.get(order['direction'])}/{order['lever']}X · 全仓",
                        "开仓价格(USDT)": f"{order['openPrice']}",
                        "开仓数量": f"{order['openAmount']}ETH",
                        "保证金(USDT)": order['bondAmount'],
                        "收益额(USDT)": f"{order['openProfit']}%({order['openProfitRate']}%)",
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
                history_page += 1
                history_data.extend(temp)
                time.sleep(1)
            else:
                break
        while True:
            temp = self.get_today_order_info(user_sign=user_sign['userSign'], nick_name=user_sign['nickName'],
                                             copy_user_num=user_sign['copyUserNum'], page=today_page, page_size=100)
            if len(temp) > 0:
                today_page += 1
                today_data.extend(temp)
                time.sleep(1)
            else:
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

        # exchange = ccxt.binance({
        #     'proxies': {
        #         'http': f'{proxie_type}://127.0.0.1:{proxies_http_port}',  # SOCKS5 代理
        #         'https': f'{proxie_type}://127.0.0.1:{proxies_https_port}',
        #     }
        # })



        # 初始化交易所
        exchange = getattr(ccxt, exchange_name)({
            'enableRateLimit': True,  # 启用请求频率限制
            "proxies": proxies
        })

        # 将时间转换为毫秒时间戳
        since = int(datetime.datetime.strptime(start_time, '%Y-%m-%d').timestamp() * 1000)
        end_time = int(datetime.datetime.strptime(end_time, '%Y-%m-%d').timestamp() * 1000)

        all_ohlcv = []

        while since < end_time:
            try:
                # 获取数据
                ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since)
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
                time.sleep(exchange.rateLimit / 1000)  # 默认延迟

            except Exception as e:
                print(f"Error: {e}")
                break

        return all_ohlcv
