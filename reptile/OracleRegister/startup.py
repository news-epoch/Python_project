from RegisterHome.EnterRegisterInformation import page1, page2, page3
from RegisterHome import getEmailUrl, util
from utils.checkChromDriver import checkChromDirver
import os, sys
from time import sleep
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options

inputData = dict()
payData1 = dict()
if __name__ == '__main__':
    # sendEmail.send()
    # 获取本地路径
    BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
    # 登录163邮件
    sleep(10)
    url = getEmailUrl.getNewOracleClode(getEmailUrl.login())
    # 创建对象
    driver = util.createdisguisedriver()
    with open(os.path.join(BASE_DIR,'conf\stealth.min.js'), 'r') as f:
        js = f.read()
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": js
    })

    inputData = util.getLocalYmlFile(BASE_DIR, 'conf\inputData.yml')
    payData1 = util.getLocalYmlFile(BASE_DIR, 'conf\payData.yml')

    #前往注册界面
    driver.get(url)
    # 填写第一页
    sleep(20)
    print("-----------------开始填写第一页基础数据-----------------")
    page1(driver=driver, data=inputData)
    sleep(20)
    # 填写第二页
    print("-----------------开始填写第二页基础数据-----------------")
    page2(driver=driver, data=inputData)
    # 添加银行卡
    sleep(10)
    print("-----------------开始添加银行卡数据-----------------")
    # 填写第三页
    page3(driver=driver, paydata=payData1)
    print("脚本执行完毕")
