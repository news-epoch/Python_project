import requests
from lxml import etree
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import ResolveDistinctPage
from time import sleep

if __name__ == '__main__':
    data = pd.read_excel('C:\\Users\\Administrator\\Documents\\BaiduNetdiskDownload\\百度资讯搜索_井冈山红色研学-URL.xlsx')
    data1 = []
    count = 1
    for i in data.values.tolist():
        i.append('null')
        try:
            task = ResolveDistinctPage.EYE(url=i[2], with_date=True)
            i[3] = task.main()['content']
        except:
            continue
        data1.append(i)
        count +=1
        if count ==5:
            print("休息5s")
            sleep(5)
            count = 1

    frame = pd.DataFrame(data1)
    frame.to_csv('./copeData1.csv')

