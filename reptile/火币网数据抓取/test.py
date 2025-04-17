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


if __name__ == '__main__':
    hbg = htx.hbg()
    hbg.k_link()
    test = hbg.k_link_profit(
        open_price="1817.01",
        lever=200,
        openAmount="0.12",
        # symbol="ETH/USDT",
        # timeframe="30m",
        # start_time="2025-04-01 02:00:00",
        # end_time="2025-04-06 21:00:00",
        # proxie_type="socks5",
        # proxies_http_port="10809",
        # proxies_https_port="10808",
        # exchange_name="binance"
    )

    # df = pandas.DataFrame(test, columns=["时间", "开盘价", "最高价", "最低价", "收盘价", "成交量", "最小收益率", "最大收益率"])
    # df["时间"] = pandas.to_datetime(df["时间"], unit="ms")
    # df.to_excel("test.xlsx", index=False)
    # results = hbg.get_rank()
    # print(results)
    #
    # print(hbg.download_driver())

    # print(datetime.datetime.utcfromtimestamp(1742911056607/1000).strftime("%Y-%m-%d %H:%M:%S"))