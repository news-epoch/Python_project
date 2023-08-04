from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains  # 鼠标事件
from time import sleep
import pickle
import tkinter
import pandas as pd
import os, sys

import openpyxl


class carryTiktok:
    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
        self.data = []

    # 初始化变量
    def anonymous_chrome(self):
        chrome_options = Options()
        # chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")
        chrome_options.add_argument('--headless')  # 设置无界面浏览器，浏览器不在标识被控制
        chrome_options.add_argument('--disable-gpu')  # 设置无界面浏览器
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        self.chromebro = webdriver.Chrome(
            service=Service(executable_path=os.path.join(self.BASE_DIR, 'utils\chromedriver.exe')),
            options=chrome_options)  # 创建网页对象

        self.action = ActionChains(self.chromebro)  # 创建鼠标事件

        # 防止检测
        self.chromebro.set_window_size(width=1050, height=892)
        self.chromebro.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"""})

        with open(os.path.join(self.BASE_DIR, 'utils/stealth.min.js')) as f:
            js = f.read()
        self.chromebro.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": js
        })
        # 存放用户+链接列表
        self.data = []

    def obvious_chrome(self):

        chrome_options = Options()
        # chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        self.chromebro = webdriver.Chrome(
            service=Service(executable_path=os.path.join(self.BASE_DIR, 'utils\chromedriver.exe')),
            options=chrome_options)  # 创建网页对象

        self.action = ActionChains(self.chromebro)  # 创建鼠标事件

        # 防止检测
        self.chromebro.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"""})

        # with open(os.path.join(self.BASE_DIR, 'utils\stealth.min.js'), 'r') as f:
        #     js = f.read()

        self.chromebro.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": ""
        })

        # 存放用户+链接列表

    # 单个执行登录tiktok
    def login(self):

        self.obvious_chrome()

        # 进入链接
        self.chromebro.get("https://www.tiktok.com/live")
        # 等待10s

        sleep(10)

        try:
            login_emailAndphone_element = self.chromebro.find_element(By.XPATH,
                                                                      "//p[contains(text(),'使用二维码')]")
            login_emailAndphone_element.click()
        except:
            print("没有找到使用二维码")

        tiktokCookie = self.chromebro.get_cookies()
        # 保存cookie文件，下次登录使用
        with open("utils/tiktok_cookie.pkl", "wb") as fp:
            pickle.dump(tiktokCookie, fp)

        print("等待360s")
        sleep(5)
        for i in range(1, 720):
            try:
                self.chromebro.find_element(By.XPATH, "//div[@aria-label='打开设置菜单']")
                tiktokCookie = self.chromebro.get_cookies()
                # 保存cookie文件，下次登录使用
                with open("utils/tiktok_cookie.pkl", "wb") as fp:
                    pickle.dump(tiktokCookie, fp)
                sleep(5)
                self.chromebro.quit()
                return "登录成功"
            except:
                print("等待登录中：%d" % (i) + "s")
                sleep(1)



    # 获取数据
    def getData(self, reviewer_max_num, reviewer_min_num,person):

        self.obvious_chrome()

        self.reviewer_max_num = reviewer_max_num
        self.reviewer_min_num = reviewer_min_num
        self.person = int(person)

        self.chromebro.get("https://www.tiktok.com/@difuzhubao/live")

        filePath = os.path.join(self.BASE_DIR, 'utils/tiktok_cookie.pkl')
        cookies = pickle.load(open(filePath, "rb"))
        for cookie in cookies:
            if isinstance(cookie.get('expiry'), float):
                cookie['expiry'] = int(cookie['expiry'])
            self.chromebro.add_cookie(cookie)
        sleep(1)
        # 前往直播数据登录
        self.chromebro.get("https://www.tiktok.com/@difuzhubao/live")

        # 判断是否存在直播视频推荐
        flag = True
        while flag:
            sleep(10)
            try:
                self.chromebro.find_element(By.XPATH, "//h2[text()='直播视频推荐']")
                flag = False
            except:
                flag = True
                print("未找到直播推荐列表，等待10s")

        url_personNum = []
        for j in range(1, self.person):

            # 获取直播推荐列表
            live_lists_xpath = "//div[@data-e2e='live-recommended-list']/div[1]/div[" + str(j) + "]"

            #  循环直播推荐列表数据
            print("循环直播推荐列表数据")
            live_list_url_xpath = "/div[contains(@class,'DivLiveCard')]/div[@data-e2e='hot-live-recommended-card']/a"
            live_list_personNum_xpath = "/div[contains(@class,'DivLiveCard')]/div[@data-e2e='hot-live-recommended-card']/div[@data-e2e='audience-info-tag']/div[contains(text(),'观众')]"
            live_list_move_xpath = "/div[contains(@class,'DivLiveCard')]/div[contains(@class,'DivLiveInfo')]/div[contains(@class,'DivExtraInfo')]/div[@data-e2e='live-card-author-name']"

            # 存放列表数据
            while True:
                try:
                    url = self.chromebro.find_element(By.XPATH, (live_lists_xpath + live_list_url_xpath)).get_attribute(
                        'href').replace('/live', '')
                    personNum = self.chromebro.find_element(By.XPATH, (
                            live_lists_xpath + live_list_personNum_xpath)).text.replace("名观众", "")
                    # 模拟鼠标向下滚动
                    self.action.move_to_element_with_offset(
                        self.chromebro.find_element(By.XPATH, (live_lists_xpath + live_list_move_xpath)), 0,
                        -10).perform()
                    # self.action.send_keys(Keys.PAGE_DOWN).perform()

                    break
                except:
                    print("没有找到url")
                    self.chromebro.set_window_size(self.chromebro.get_window_size()['width'] + 10,
                                                   self.chromebro.get_window_size()['height'] + 10)
                    self.chromebro.set_window_size(self.chromebro.get_window_size()['width'] - 10,
                                                   self.chromebro.get_window_size()['height'] - 10)
                    sleep(5)
                    continue

            personNum = self.copeData(personNum)

            url_personNum.append([url, personNum])  # 存放列表数据
            # if j % 6 != 0:
            #     sleep(10)

            print(url)

        print("读取用户数据")
        for i in url_personNum:
            data1 = self.toSwitchPage(i)

            if data1 != "":
                self.data.append(data1)

        sleep(5)
        filePath1 = os.path.join(self.BASE_DIR, 'data.pickle')
        with open(filePath1, 'wb') as f:
            pickle.dump(self.data, f)

        return self.data

    # 抓取数据
    def toSwitchPage(self, url):
        """
        :param url: 包含主播信息链接和直播间观看人数
        :return: 返回抓取到的完整数据
        """
        ## 清空cookie
        self.chromebro.delete_all_cookies()

        self.chromebro.execute_script('window.open("","_blank");')  # 新建标签页

        all_handles = self.chromebro.window_handles  # 获取所有句柄

        self.chromebro.switch_to.window(self.chromebro.window_handles[1])  # 切换到标签页2

        self.chromebro.get(url[0])  # 前往用户列表
        # 等待5s
        sleep(5)
        anchorId = self.chromebro.find_element(By.XPATH, "//h1[@data-e2e='user-title']").text  # 用户名id
        following = self.chromebro.find_element(By.XPATH,
                                                "//span[text()='已关注' and @data-e2e='following']/preceding-sibling::strong[@title='已关注']").text
        following = self.copeData(following)

        fans = self.chromebro.find_element(By.XPATH,
                                           "//span[text()='粉丝' and @data-e2e='followers']/preceding-sibling::strong[@title='粉丝']").text
        fans = self.copeData(fans)

        likes = self.chromebro.find_element(By.XPATH,
                                            "//span[text()='赞' and @data-e2e='likes']/preceding-sibling::strong[@title='赞']").text
        likes = self.copeData(likes)

        # 关闭当前页面
        print({'anchorId': anchorId, 'following': following, 'fans': fans, 'likes': likes, 'personNum': url[1]})
        self.chromebro.close()  # 关闭标签页2
        self.chromebro.switch_to.window(self.chromebro.window_handles[0])  # 切换到标签页1

        if self.reviewer_max_num >= float(fans) >= self.reviewer_min_num:
            return {'anchorId': anchorId, 'following': following, 'fans': fans, 'likes': likes, 'personNum': url[1]}
        else:
            return ""

    # 处理数据
    def copeData(self, temp):
        """
        :param temp: 传入数据，用来处理字符中包含K和M单位的数据
        :return: 返回处理好的数据
        """
        if temp.find("K") != -1:
            return float(str(temp).replace("K", "")) * 1000
        elif temp.find("M") != -1:
            return float(str(temp).replace("M", "")) * 1000000
        elif temp.find("M") == -1 and temp.find("K") == -1:
            return float(temp)

    def export_excel(self):

        filePath = os.path.join(self.BASE_DIR, 'utils/data.pickle')
        if os.path.exists(filePath):
            pass
        else:
            return "数据文件不存在，请先爬取数据后在导出数据"

        data = pickle.load(open(filePath, "rb"))
        data1 = []
        for i in data:
            if isinstance(i, dict):
                data1.append(i)

        df = pd.DataFrame(data=data1)
        filePath = os.path.join(self.BASE_DIR, 'TikTok数据文件.xlsx')
        try:
            df.to_excel(filePath, index=False)
            return "导出路径：" + filePath
        except Exception as e:
            return str(e)


class pop_up_box:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title('配置界面')
        self.root.geometry('400x200')

        self.ct = carryTiktok()
        self.tiktok_login = carryTiktok()

    def set_fans(self):
        #
        # 设置文本框，读取粉丝数量范围
        ## 配置标签
        label1 = tkinter.Label(self.root, text='粉丝数区间(小~大)：').grid(row=0, column=0)
        reviewer_max_num = tkinter.IntVar()  # 存放最大粉丝数量

        Entry_reviewer_max = tkinter.Entry(self.root, textvariable=reviewer_max_num, width=10).grid(row=0, column=3)
        label2 = tkinter.Label(self.root, text='~').grid(row=0, column=2)
        reviewer_min_num = tkinter.IntVar()
        Entry_reviewer_min = tkinter.Entry(self.root, textvariable=reviewer_min_num, width=10).grid(row=0, column=1)

        btn = tkinter.Button(self.root, text="确定粉丝区间",
                             command=lambda: self.ct.getData(reviewer_max_num=reviewer_max_num.get(),
                                                             reviewer_min_num=reviewer_min_num.get())).grid(row=0,
                                                                                                            column=4)

    def set_login(self):
        # 配置登录按钮
        # button_login = tkinter.Button(self.root, text="登录tiktok", command=lambda: self.button_click())
        button_login = tkinter.Button(self.root, text="登录TikTok", command=lambda: self.tiktok_login.login())
        button_login.grid(row=1, column=0)

    def export_data(self):
        button_export = tkinter.Button(self.root, text="导出数据文件", command=lambda: self.ct.export_excel())
        button_export.grid(row=1, column=1)

    def start(self):
        self.set_fans()
        self.set_login()
        self.export_data()
        self.root.mainloop()
