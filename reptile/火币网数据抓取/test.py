import datetime
import logging
import os
import sys

import pandas

import htx
import sys
# from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
#                              QComboBox, QLabel, QLineEdit, QFormLayout, QStackedWidget)


# GUIdemo1.py
# Demo1 of GUI by PqYt5
# Copyright 2021 Youcans, XUPT
# Crated：2021-10-06
import logging.config as log_config

# if __name__ == '__main__':
#     from dateutil.relativedelta import relativedelta
application = htx.load_yaml()
log_config.dictConfig(application['logging'])
logger = logging.getLogger(__name__)

def test01():
    hbg = htx.hbg()
    data = hbg.comouter_yield(
        historical_leads_file_path=r"D:\code\python\Python_project\reptile\火币网数据抓取\2025041720历史带单数据.xlsx",
        start_time="2025-03-01 00:00:00",
        end_time="2025-04-17 00:00:00",
        timeframe="5m",
        proxie_type="socks5",
        proxies_http_port="10809",
        proxies_https_port="10808",
        exchange_name="binance"
    )
    pd = pandas.DataFrame(data)
    pd.to_excel("test.xlsx", index=False)

def test02():
    hbg = htx.hbg()
    hbg.k_link_profit()
if __name__ == '__main__':
    test01()

    # df = pandas.DataFrame(test, columns=["时间", "开盘价", "最高价", "最低价", "收盘价", "成交量", "最小收益率", "最大收益率"])
    # df["时间"] = pandas.to_datetime(df["时间"], unit="ms")
    # df.to_excel("test.xlsx", index=False)
    # results = hbg.get_rank()
    # print(results)
    #
    # print(hbg.download_driver())

    # print(datetime.datetime.utcfromtimestamp(1742911056607/1000).strftime("%Y-%m-%d %H:%M:%S"))