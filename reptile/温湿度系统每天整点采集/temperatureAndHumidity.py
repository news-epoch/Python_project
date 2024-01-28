import os
import sys
import time

import pymysql
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import logging
import CopeCaptchaImage
import pandas as pd


class temperatureAndHumidity:
    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
        self.realTimeDataList = list()  # 实时数据列表
        self.oldTimeDataList = list()  # 历史数据列表
        self.anonymous_chrome()

    # 无界面显示抓取
    def anonymous_chrome(self):
        chrome_options = Options()
        # chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")
        chrome_options.add_argument('--headless')  # 设置无界面浏览器，浏览器不在标识被控制
        chrome_options.add_argument('--disable-gpu')  # 设置无界面浏览器
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        self.chromebro = webdriver.Chrome(
            service=Service(executable_path=os.path.join(self.BASE_DIR, r'utils/chromedriver')),
            options=chrome_options)  # 创建网页对象
        self.chromebro.set_page_load_timeout(1800)

    # 有界面显示抓取
    def obvious_chrome(self):
        chrome_options = Options()
        # chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        self.chromebro = webdriver.Chrome(
            service=Service(executable_path=os.path.join(self.BASE_DIR, r'utils/chromedriver.exe')),
            options=chrome_options)  # 创建网页对象

    # 登录
    def login(self, username, password):
        """
        通过selenium登录用户，获取到对应的Cookie
        :param username: 用户名
        :param password: 密码
        :return: Cookies
        """

        self.chromebro.get("https://www.0531yun.com/login.html")

        time.sleep(3)
        # 输入账户 //label[contains(text(),'账')]/following-sibling::input[@type="text"]
        self.chromebro.find_element(By.XPATH,
                                    "//label[contains(text(),'账')]/following-sibling::input[@type='text']").send_keys(
            str(username))

        # 输入密码 //label[contains(text(),'密')]/following-sibling::input[@type="password"]
        self.chromebro.find_element(By.XPATH,
                                    "//label[contains(text(),'密')]/following-sibling::input[@type='password']").send_keys(
            str(password))

        # 输入验证码 //img[@id='imgValidCode' and @title='点击刷新验证码']
        ## 查询验证码,循环识别验证码，直到识别成功
        while True:
            captchaImgPath = CopeCaptchaImage.image_cj(driver=self.chromebro, _save_url=(self.BASE_DIR + "/"),
                                                       yuansu="//img[@id='imgValidCode']")  # 验证码图片
            CopeCaptchaText = CopeCaptchaImage.image_text((self.BASE_DIR + "/"), captchaImgPath)  # 识别验证码
            copeText = CopeCaptchaText[0:5].strip()
            if len(copeText) == 0 or len(copeText) != 4:  # 没有内容，或者 内容不超过4个
                self.chromebro.find_element(By.XPATH, "//img[@id='imgValidCode' and @title='点击刷新验证码']").click()  # 刷新验证码
                time.sleep(2)
                continue
            # elif copeText.isalnum() == False:  # 没有包含数字或者单词
            #     self.chromebro.find_element(By.XPATH, "//img[@id='imgValidCode' and @title='点击刷新验证码']").click()  # 刷新验证码
            #     time.sleep(2)
            #     continue
            ## 输入验证码 //label[text()='验证码：']/following-sibling::input
            print("copeText: " + copeText)
            time.sleep(2)
            self.chromebro.find_element(By.XPATH, "//label[text()='验证码：']/following-sibling::input").click()
            self.chromebro.find_element(By.XPATH, "//label[text()='验证码：']/following-sibling::input").send_keys(
                str(copeText))
            break

        # 登录
        while True:
            time.sleep(2)
            self.chromebro.find_element(By.XPATH, "//button[@id='login_btn']").click()
            time.sleep(10)
            try:
                if self.chromebro.find_element(By.XPATH, "//button[@id='login_btn']").text == '立即登录':
                    return "登录失败"
                print(self.chromebro.find_element(By.XPATH, "//a[@id='myname']").text + "：登录成功")
            except Exception:
                print("登录成功")
                break
        # while True:
        #     try:
        #         time.sleep(2)
        #         self.chromebro.find_element(By.XPATH, "//button[@id='login_btn']").click()
        #         time.sleep(15)
        #         if self.chromebro.find_element(By.XPATH, "//button[@id='login_btn']"):
        #             return "登录失败"
        #     except Exception:
        #         print("登录失败")
        #         return "登录失败"

        # 获取登录Cookie
        self.tiktokCookie = self.chromebro.get_cookies()
        return "登录成功"


    def getRealTemperature(self):
        """
        获取实时数据
        :return: 返回实时响应数据的data字典数据
        """
        mTime = int(time.time() * 1000)  # 当前毫秒时间戳
        cookies = '; '.join(item for item in [item["name"] + "=" + item["value"] for item in self.tiktokCookie])
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'www.0531yun.com',
            'Referer': 'https//www.0531yun.com/index.html',
            'Cookie': str(cookies),
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows"
        }
        url = "https://www.0531yun.com/sysData/getRealTimeData?_=" + str(mTime)
        responseJson = requests.session().get(url, headers=headers, verify=False)
        return responseJson.json()['data']

    def getOldTemperature(self, TemperatureData):
        """
        :param realTemperatureData: JSON响应数据中的data字典数据的列表元素
        :return: 返回历史响应数据结果
        """

        # 声明当前时间戳
        timestamp = time.time()
        # 获取Cookie
        cookies = '; '.join(item for item in [item["name"] + "=" + item["value"] for item in self.tiktokCookie])
        # 设置历史数据请求头
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'www.0531yun.com',
            'Referer': 'https://www.0531yun.com/history.html',
            'Cookie': str(cookies),
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows"
        }
        # 循环设备列表
        i = TemperatureData

        try:
            if i['dataItem'] == '' or i['dataItem'] == 'null' or i['dataItem'] == None:
                params = {
                    'deviceAddr': i['deviceAddr'],
                    'factorIds': str(i['deviceAddr']) + '_1_1,' + str(i['deviceAddr']) + '_1_2',
                    # 24251128_1_1 温度   24251128_1_2 湿度
                    'startTime': int(timestamp) * 1000,
                    'endTime': int(CopeCaptchaImage.getBeforeDay(timestamp, day=30)) * 1000,
                    '_': int(timestamp * 1000)
                }
                print("请求的参数为：{}".format(params))
                oldsResponseJson = requests.session().get("https://www.0531yun.com/sysData/multicolumnHistory",
                                                          params=params, headers=headers, verify=False).json()
                try:
                    if oldsResponseJson['data']['dataCollectionList'] != '' or oldsResponseJson['data']['dataCollectionList'] != 'null' or oldsResponseJson['data']['dataCollectionList'] != None:  # 判断是否存在数据
                        print("----------结束抓取该设备数据end--------------------")
                        return oldsResponseJson
                    else:
                        print(str(i['deviceAddr']) + ": 该设备响应数据，有问题,数据为：{}".format(oldsResponseJson))
                        return '无数据'
                except Exception:
                    print(str(i['deviceAddr']) + ": 该设备响应数据，有问题--------------------------------《》")
                    return '无数据'

        except Exception:
            print(str(i['deviceName'])+": "+str(i['deviceAddr']) + ": 该设备无列表数据，有问题--------------------------------《》")
            return '无数据'

        for j in i['dataItem']:  # 循环是否有数据
            if len(j['registerItem']) == 1:  # 只存在温度，或者湿度
                params = {
                    'deviceAddr': i['deviceAddr'],
                    'factorIds': str(i['deviceAddr']) + '_' + str(j['nodeId']) + '_' + str(
                        j['registerItem'][0]['registerId']),  # 24251128_1_1 温度   24251128_1_2 湿度
                    'endTime': int(timestamp) * 1000,
                    'startTime': int(CopeCaptchaImage.getBeforeDay(timestamp, day=30)) * 1000,
                    '_': int(timestamp * 1000)
                }
                print("请求的参数为：{}".format(params))
                oldsResponseJson = requests.session().get("https://www.0531yun.com/sysData/multicolumnHistory",
                                                          params=params, headers=headers, verify=False).json()
                return oldsResponseJson
            elif len(j['registerItem']) == 2:  # 存在温度和湿度
                params = {
                    'deviceAddr': i['deviceAddr'],
                    # 24251128_1_1 温度   24251128_1_2 湿度
                    'factorIds': str(i['deviceAddr']) + '_' + str(j['nodeId']) + '_' + str(j['registerItem'][0]['registerId']) + ',' + str(i['deviceAddr']) + '_' + str(j['nodeId']) + '_' + str(j['registerItem'][1]['registerId']),
                    'endTime': int(timestamp) * 1000,
                    'startTime': int(CopeCaptchaImage.getBeforeDay(timestamp, day=30)) * 1000,
                    '_': int(timestamp * 1000)
                }
                print("请求的参数为：{}".format(params))
                oldsResponseJson = requests.session().get("https://www.0531yun.com/sysData/multicolumnHistory",
                                                          params=params, headers=headers, verify=False).json()
                if oldsResponseJson['message'] == '访问过于频繁，请稍后再试':
                    print(str(i['deviceName'])+": "+str(i['deviceAddr']) + ": 访问过于频繁，请稍后再试--------------------------------《》")
                    return "访问过于频繁，请稍后再试"

                return oldsResponseJson


    def copeRealTimeTemperatureData(self, realTimeData):
        """
        处理实时数据，将实时数据格式化
        :param realTimeData: 实时数据{}
        :return:
        """

        for i in realTimeData:
            data = dict()
            data['device_number'] = i['deviceAddr']  # 设备编号
            if int(i['timeStamp']) != 0:
                data['create_time'] = (int(int(i['timeStamp']) / 1000))  # 创建时间
            elif int(i['timeStamp']) == 0:
                data['create_time'] = 0

            try:
                if len(i['dataItem'][0]['registerItem'][0]['data']) != 0:
                    data['device_temperature'] = i['dataItem'][0]['registerItem'][0]['data']  # 设备温度
            except Exception:
                data['device_temperature'] = '0'
            try:
                if len(i['dataItem'][0]['registerItem'][1]['data']) != 0:
                    data['device_humidity'] = i['dataItem'][0]['registerItem'][1]['data']  # 设备湿度
            except Exception:
                data['device_humidity'] = '0'

            self.realTimeDataList.append(data)

    def copeOldsTimeTemperatureData(self, oldsResponseJson):
        """
        处理历史数据
        :param oldsResponseJson: Json格式的响应数据
        :return: 返回处理的响应数据
        """
        # 用来存放单个机器的oldTemperatureDataList数据
        oldTimeDataList = list()

        # 判断是否存在历史数据列表
        try:
            dataCollectionList = oldsResponseJson['data']['dataCollectionList']
            print("处理数据条数为：{}".format(len(dataCollectionList)))
        except Exception:
            print("-----------------------处理数据异常start-----------------------")
            print(oldsResponseJson)
            print("-----------------------处理数据异常end-----------------------")
            return "无数据"

        for dataCollection in dataCollectionList:
            # 存放单个Temperature的数据
            exportData = dict()
            try:
                exportData['device_number'] = dataCollection['deviceAddr']  # 设备编号
            except Exception:
                exportData['device_number'] = '0'
            try:
                exportData['create_time'] = int(dataCollection['recordTime'] / 1000)  # 创建时间
            except Exception:
                exportData['create_time'] = '0'

            exportData['device_temperature'] = 0  # 设备温度
            exportData['device_humidity'] = 0  # 设备湿度
            # 循环温度湿度数据，判断是否存在
            for z in range(1, 3):
                try:
                    data = dataCollection['dataMap']['1_' + str(z)]
                    if data['registerName'] == '温度':
                        exportData['device_temperature'] = data['value']
                    elif data['registerName'] == '湿度':
                        exportData['device_humidity'] = data['value']
                except Exception:
                    pass

            # 添加当次查询历史数据列表中
            oldTimeDataList.append(exportData)
            # 添加到所有查询的历史数据列表中
            self.oldTimeDataList.append(exportData)

        return oldTimeDataList

    def export_mysql(self, DataList, tableName):
        mysql_config = CopeCaptchaImage.readYml("config.yml")['mysql']
        mysql_config['cursorclass'] = pymysql.cursors.DictCursor
        conn = pymysql.connect(**mysql_config)
        cursor = conn.cursor()
        for i in DataList:
            select_sql = "select * from {} where device_number='{}' and device_temperature='{}' and device_humidity='{}' and create_time={};".format(tableName, i['device_number'], i['device_temperature'], i['device_humidity'], int(i['create_time']))
            insert_sql = "INSERT INTO {}(device_number,device_temperature,device_humidity,create_time) VALUES ('{}', '{}', '{}', {});".format(tableName, i['device_number'], i['device_temperature'], i['device_humidity'], int(i['create_time']))
            try:
                cursor.execute(select_sql)
                if len(cursor.fetchall()) >= 1:
                    continue
                if len(cursor.fetchall()) == 0:
                    cursor.execute(insert_sql)
            except:
                print(insert_sql+"写入错误")
        # 写入数据
        conn.commit()
        cursor.close()
        conn.close()

    # 单独抓取历史数据
    def scrapeAndProcessHistoricalData(self, tableName):
        print("开始抓取历史数据,时间为：{}".format((time.strftime("%Y-%m-%d %H:%M:%S")))+"<<==========================================")
        while True:
            # 开始登录
            loginStatus = self.login(username="h230925gj", password="h230925gj")
            if loginStatus == '登录失败':
                continue
            elif loginStatus == '登录成功':
                break

        # 获取实时数据
        realTemperatureData = self.getRealTemperature()

        print("-----------抓取数据列表-----------")
        for i in realTemperatureData:
            print(i['deviceName']+": "+str(i['deviceAddr']))

        print("-----------抓取数据列表-----------")

        for Temperature in realTemperatureData:
            time.sleep(10)
            while True:
                print("----------1. 开始抓取该设备数据START--------------------")
                print("开始抓取设备的名字：" + Temperature["deviceName"])
                oldsResponseJson = self.getOldTemperature(Temperature)  # 获取历史数据
                if oldsResponseJson != '无数据':
                    print("----------1. 结束抓取该设备数据END--------------------")
                    print("----------2. 开始处理该设备数据START--------------------")
                    self.copeOldsTimeTemperatureData(oldsResponseJson)  # 处理历史数据
                    print("=================2. 结束处理数据结束END================\n\n")
                    break
                if oldsResponseJson == '访问过于频繁，请稍后再试':
                    time.sleep(60)
                    continue
                break


        print("================3. 处理时间相近的数据START================")
        print("处理条数为： {}".format(len(self.oldTimeDataList))+" 条")
        self.copeCreateTime(data=self.oldTimeDataList)
        print("================3. 处理时间相近的数据END================\n\n")
        print("========================全部设备处理完毕，开始导入数据库========================")
        print("导入数据库条数为：{}".format(len(self.oldTimeDataList))+"条")
        self.export_mysql(self.oldTimeDataList, tableName=tableName)

        print("结束抓取历史数据,时间为：{}".format((time.strftime("%Y-%m-%d %H:%M:%S")))+"<<==========================================")

    # 单独抓取实时数据
    def captureRealTimeDataIndividually(self, tableName):
        print("开始抓取实时数据,时间为：{}".format((time.strftime("%Y-%m-%d %H:%M:%S")))+"<<==========================================")
        while True:
            # 开始登录
            loginStatus = self.login(username="h230925gj", password="h230925gj")
            if loginStatus == '登录失败':
                continue
            elif loginStatus == '登录成功':
                break

        # 获取实时数据
        while True:
            print("获取实时数据===========》")
            realTemperatureData = self.getRealTemperature()
            if realTemperatureData != '无数据':
                self.copeRealTimeTemperatureData(realTimeData=realTemperatureData)
                self.export_mysql(self.realTimeDataList, str(tableName))
                print(self.realTimeDataList)
                print("================》结束获取实时数据")
                break
        print("结束抓取实时数据,时间为：{}".format((time.strftime("%Y-%m-%d %H:%M:%S"))) + "<<==========================================")


    # 处理时间重复数据
    def copeCreateTime(self, data):
        for i in range(len(data)-1, -1, -1):
            for j in range(len(data)-2, -1, -1):
                if data[i]['device_number'] == data[j]['device_number']:
                    if time.strftime("%Y-%m-%d %H", time.localtime(data[i]['create_time'])) == time.strftime("%Y-%m-%d %H", time.localtime(data[j]['create_time'])):
                        if int(time.strftime("%M", time.localtime(data[i]['create_time']))) - int(time.strftime("%M", time.localtime(data[j]['create_time']))) > 0:
                            self.oldTimeDataList.pop(j)
                        elif int(time.strftime("%M", time.localtime(data[i]['create_time']))) - int(time.strftime("%M", time.localtime(data[j]['create_time']))) < 0:
                            self.oldTimeDataList.pop(i)
                        else:
                            continue

    # def export_excel(self, dataList, filename):
    #     pf = pd.DataFrame(dataList)
    #     pf['create_time'] = pf['create_time'].astype(str)
    #     pf.to_excel(str(filename) + ".xlsx", index=False)

if __name__ == '__main__':
    temperatureAndHumidity = temperatureAndHumidity()  # 调用程序
    # temperatureAndHumidity.scrapeAndProcessHistoricalData("temperatureTest")
    temperatureAndHumidity.captureRealTimeDataIndividually("temperatureTest")

