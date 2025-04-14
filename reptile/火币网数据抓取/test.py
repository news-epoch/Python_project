import datetime
import os
import sys

import htx
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QComboBox, QLabel, QLineEdit, QFormLayout, QStackedWidget)


# GUIdemo1.py
# Demo1 of GUI by PqYt5
# Copyright 2021 Youcans, XUPT
# Crated：2021-10-06


if __name__ == '__main__':
    from dateutil.relativedelta import relativedelta

    time_str1 = '2022-01-01 11:59:00'
    time_str2 = '2022-01-01 14:30:00'
    time1 = datetime.datetime.strptime(time_str1, '%Y-%m-%d %H:%M:%S')
    time2 = datetime.datetime.strptime(time_str2, '%Y-%m-%d %H:%M:%S')
    time_interval = relativedelta(time2, time1)
    print(f"{time_interval.days}天{time_interval.hours}小时{time_interval.minutes}分")


# if __name__ == '__main__':
#     hbg = htx.hbg("综合排名")
#     # results = hbg.get_rank()
#     # print(results)
#     #
#     # print(hbg.download_driver())
#
#     print(datetime.datetime.utcfromtimestamp(1742911056607/1000).strftime("%Y-%m-%d %H:%M:%S"))