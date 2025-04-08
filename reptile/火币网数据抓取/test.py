import os
import sys

from reptile.火币网数据抓取 import htx

if __name__ == '__main__':
    hbg = htx.hbg("综合排名")
    # results = hbg.get_rank()
    # print(results)
    #
    print(hbg.download_driver())