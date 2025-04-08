import datetime
import os
import sys

import htx

if __name__ == '__main__':
    hbg = htx.hbg("综合排名")
    # results = hbg.get_rank()
    # print(results)
    #
    # print(hbg.download_driver())

    print(datetime.datetime.utcfromtimestamp(1742911056607/1000).strftime("%Y-%m-%d %H:%M:%S"))