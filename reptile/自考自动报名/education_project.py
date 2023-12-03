import json
import pickle
from datetime import datetime, timedelta

import requests, os, sys
from time import sleep

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QScrollArea, QVBoxLayout
from PyQt5 import uic
from PyQt5 import QtCore

import urllib3


class education:
    def __init__(self):
        self.BasePath = os.path.dirname(os.path.realpath(sys.argv[0]))
        urllib3.disable_warnings()
        self.cookies = ""

        # 地区市州代码
        self.qxdm = dict()
        with open(os.path.join(self.BasePath, "utils\\四川地市州报名列表.json"), 'r', encoding='utf-8') as fp:
            self.qxdm = json.loads(fp.read())

        # 计算机信息管理科目代码
        self.jsjxxglkmdm = [
            {
                "KC_BM": "02375",
                "KC_BKFY": 35,
                "KSSJ": "2023-04-15 09:00",
                "ZY_MC": "计算机信息管理",
                "SJ_BM": "A",
                "ZY_BM": "Y082208",
                "KC_MC": "运筹学基础"
            },
            {
                "KC_BM": "02378",
                "KC_BKFY": 35,
                "KSSJ": "2023-04-15 09:00",
                "ZY_MC": "计算机信息管理",
                "SJ_BM": "A",
                "ZY_BM": "Y082208",
                "KC_MC": "信息资源管理"
            },
            {
                "KC_BM": "04735",
                "KC_BKFY": 35,
                "KSSJ": "2023-04-15 14:30",
                "ZY_MC": "计算机信息管理",
                "SJ_BM": "B",
                "ZY_BM": "Y082208",
                "KC_MC": "数据库系统原理"
            },
            {
                "KC_BM": "02628",
                "KC_BKFY": 35,
                "KSSJ": "2023-04-16 09:00",
                "ZY_MC": "计算机信息管理",
                "SJ_BM": "C",
                "ZY_BM": "Y082208",
                "KC_MC": "管理经济学"
            },
            {
                "KC_BM": "00015",
                "KC_BKFY": 35,
                "KSSJ": "2023-04-16 14:30",
                "ZY_MC": "计算机信息管理",
                "SJ_BM": "D",
                "ZY_BM": "Y082208",
                "KC_MC": "英语(二)"
            },
            {
                "KC_BM": "04741",
                "KC_BKFY": 35,
                "KSSJ": "2023-04-16 14:30",
                "ZY_MC": "计算机信息管理",
                "SJ_BM": "D",
                "ZY_BM": "Y082208",
                "KC_MC": "计算机网络原理"
            },
            {
                "KC_BM": "02323",
                "KC_BKFY": 35,
                "KSSJ": "2023-04-16 14:30",
                "ZY_MC": "计算机信息管理",
                "SJ_BM": "D",
                "ZY_BM": "Y082208",
                "KC_MC": "操作系统概论"
            }
        ]

        # 地市州状态码
        self.cxdsztdm = dict()
        with open(os.path.join(self.BasePath, "utils\\四川地市州查询状态码.json"), 'r', encoding='utf-8') as fp:
            self.cxdsztdm = json.loads(fp.read())

        self.getHomeCookie()
        self.getCodePng()

    def getCookie(self, response):
        cookie_value = ''
        for key, value in response.cookies.items():
            cookie_value += key + '=' + value + ';'
        return cookie_value

    # 请求主页的cookie
    def getHomeCookie(self):

        homeheader = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'zk.sceea.cn',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        }
        homereponse = requests.get(url="https://zk.sceea.cn/", headers=homeheader, verify=False)

        self.homereponse_Cookie = self.getCookie(homereponse)
        print("homereponse_Cookie：{" + self.homereponse_Cookie + "}")

        # homereponse.close()

    # 获取验证码
    def getCodePng(self):
        """
        获取验证码图片请求
        :return:
        """
        # 请求头
        self.imgheader = {"Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
                          "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "zh-CN,zh;q=0.9",
                          "Connection": "keep-alive", "Host": "zk.sceea.cn", "Referer": "https://zk.sceea.cn/",
                          "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "Windows", "Sec-Fetch-Dest": "image",
                          "Sec-Fetch-Mode": "no-cors", "Sec-Fetch-Site": "same-origin",
                          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
                          # 添加cookie
                          'Cookie': self.homereponse_Cookie}

        # 请求验证码

        regExamCheck = requests.get(url="https://zk.sceea.cn/RegExam/login/AuthImageServlet?t=0.3586720730887125",
                                    headers=self.imgheader, verify=False)
        ## 保存图片

        codePngpath = os.path.join(self.BasePath, "utils\\valcode.gif")
        with open(codePngpath, 'wb') as fp:
            fp.write(regExamCheck.content)

        self.regExamCheck_Cookie = self.getCookie(regExamCheck)
        print("验证码regExamCheck_Cookie{" + self.regExamCheck_Cookie + "}")

        # regExamCheck.close()

    def login(self, username, password, zkzh):
        """
        :param username: 账户
        :param password: 密码
        :param zkzh: 准考证号
        :return:
        登录验证
        """
        self.zkzh = zkzh
        self.username = username
        code = input("请输入验证码：")
        # 登录请求头
        loginheader = {'Accept': 'application/json, text/javascript, */*; q=0.01',
                       'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9',
                       'Connection': 'keep-alive', 'Content-Length': '44',
                       'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Host': 'zk.sceea.cn',
                       'Origin': 'https://zk.sceea.cn', 'Referer': 'https://zk.sceea.cn/', 'sec-ch-ua-mobile': '?0',
                       'sec-ch-ua-platform': "Windows", 'Sec-Fetch-Dest': 'empty', "Sec-Fetch-Mode": 'cors',
                       'Sec-Fetch-Site': 'same-origin',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
                       'X-Requested-With': 'XMLHttpRequest',
                       'Cookie': self.regExamCheck_Cookie + self.homereponse_Cookie}

        print("loginheader_cookies：{" + loginheader['Cookie'] + "}")

        loginData01 = {
            'name': username,
            'pwd': password,
            'code': code.__str__()
        }
        flag = True

        # 重复发送登录请求
        ## 登录请求1
        while flag:
            loginResponse = requests.post(url="https://zk.sceea.cn/RegExam/ks1lm2yt5w0beqomselogin?resourceId=login",
                                          headers=loginheader, data=loginData01, verify=False)
            if loginResponse.text != '7':
                flag = False
                ## 保存登录的cookie
                self.Cookies = self.getCookie(loginResponse) + loginheader['Cookie'].__str__()
                print(loginResponse.text + "---->登录成功")

            else:
                print(loginResponse.text + "--->登录失败。。。。。")

        # flag = True
        # ## 获取相应的ID\USER-UUID等cookie
        # while flag:
        #     session = requests.session()
        #     loginheader02 = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br',
        #                      'Accept-Language': 'zh-CN,zh;q=0.9', 'Connection': 'keep-alive', 'Content-Length': '72',
        #                      'Content-Type': 'application/x-www-form-urlencoded', 'Host': 'zk.sceea.cn',
        #                      'Origin': 'https://zk.sceea.cn', 'Referer': 'https://zk.sceea.cn/',
        #                      'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': "Windows", 'Sec-Fetch-Dest': 'empty',
        #                      'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin',
        #                      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        #                      'X-Requested-With': 'XMLHttpRequest', 'Cookie': self.subjectheader['Cookie']}
        #
        #     logindata02 = {
        #         'login': username,
        #         'password': password,
        #         'captchaText': code.__str__(),
        #         'canLoginValue': ''
        #     }
        #     session.post(url="https://zk.sceea.cn/c/portal/login", headers=loginheader02, data=logindata02,
        #                  verify=False)
        #     self.loginCookies02 = requests.utils.dict_from_cookiejar(session.cookies)
        #     cookie_value = ''
        #     for key, value in self.loginCookies02.items():
        #         if key == 'JSESSIONID' or key == 'COOKIE_SUPPORT' or key == 'GUEST_LANGUAGE_ID' or key == 'X-LB':
        #             continue
        #         cookie_value += key + '=' + value + ';'
        #
        #     self.subjectheader['Cookie'] = cookie_value + loginheader['Cookie']
        #     print("subjectheader：{" + self.subjectheader['Cookie'] + "}")
        #
        #     flag = False

        # 提交报考科目

    def searchPlace(self, ds):
        """
        :param ds:地市名首字母缩写:
        :return:
        """

        headers = {'Accept': 'application/json, text/javascript, */*; q=0.01', 'Accept-Encoding': 'gzip, deflate, br',
                   'Accept-Language': 'zh-CN,zh;q=0.9', 'Connection': 'keep-alive', 'Content-Length': '74',
                   'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8', 'Host': 'zk.sceea.cn',
                   'Origin': 'https://zk.sceea.cn', 'Referer': "https://zk.sceea.cn/RegExam/switchPage?resourceId=view",
                   'Sec-Ch-Ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
                   'Sec-Ch-Ua-Mobile': '?0', 'Sec-Ch-Ua-Platform': '\"Windows\"', 'Sec-Fetch-Dest': 'empty',
                   'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
                   'X-Requested-With': 'XMLHttpRequest', 'Cookie': self.Cookies}

        print("headers['Cookie']:" + headers['Cookie'])

        data = {
            'bkzt': '',
            'qxbm': '',
            'sfzh': self.username,
            'dsz': self.cxdsztdm[ds],
            'stuType': 1,
            'stuScope': self.zkzh[0:4],
            'times': 'B'
        }

        response = requests.post("https://zk.sceea.cn/RegExam/switchPage?resourceId=searchPlace", headers=headers,
                                 data=data, verify=False)
        jsonData = response.json()
        print(jsonData)
        sleep(3)
        print("考区编码\t考区\t\t第一天上午\t第一天下午\t第二天上午\t第二天下午")
        try:
            for i in jsonData["data"]:
                print(str(i["QX_BM"]) + "\t" + str(i["QX_MC"]) + "\t\t" + str(i["REST_A"]) + "\t\t" + str(
                    i["REST_B"]) + "\t\t" + str(i["REST_C"]) + "\t\t" + str(i["REST_D"]))
        except:
            print(jsonData)

        return jsonData["data"]

    def subjectRegExam(self, km, qx, sz):
        """
        :param km: 科目
        :param qx: 区县
        :param sz: 市州
        :return:
        """
        subjectheader = {
            'Accept': 'text/plain, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '188',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Host': 'zk.sceea.cn',
            'Origin': 'https://zk.sceea.cn',
            'Referer': 'https://zk.sceea.cn/RegExam/switchPage?resourceId=view',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

        subjectheader['Cookie'] = self.Cookies
        # print("subjectheader['Cookie']:" + self.Cookies)

        zy_bm, kc_bm, mainIds, qxname, coursejson, qxdm = "", "", "", "", [], []

        if str(sz).__contains__("成都"):
            qxdm = self.qxdm['cd']
            self.searchPlace('cd')
        elif str(sz).__contains__("自贡"):
            qxdm = self.qxdm['zg']
            self.searchPlace('zg')
        elif str(sz).__contains__("乐山"):
            qxdm = self.qxdm['ls']
            self.searchPlace('ls')
        elif str(sz).__contains__("攀枝花"):
            qxdm = self.qxdm['pzh']
            self.searchPlace('pzh')
        elif str(sz).__contains__("泸州"):
            qxdm = self.qxdm['lz']
            self.searchPlace('lz')
        elif str(sz).__contains__("德阳"):
            qxdm = self.qxdm['dy']
            self.searchPlace('dy')
        elif str(sz).__contains__("绵阳"):
            qxdm = self.qxdm['my']
            self.searchPlace('my')
        elif str(sz).__contains__("广元"):
            qxdm = self.qxdm['gy']
            self.searchPlace('gy')
        elif str(sz).__contains__("遂宁"):
            qxdm = self.qxdm['sn']
            self.searchPlace('sn')
        elif str(sz).__contains__("内江"):
            qxdm = self.qxdm['nj']
            self.searchPlace('nj')
        elif str(sz).__contains__("南充"):
            qxdm = self.qxdm['nc']
            self.searchPlace('nc')
        elif str(sz).__contains__("宜宾"):
            qxdm = self.qxdm['yb']
            self.searchPlace('yb')
        elif str(sz).__contains__("广安"):
            qxdm = self.qxdm['ga']
            self.searchPlace('ga')
        elif str(sz).__contains__("达州"):
            qxdm = self.qxdm['dz']
            self.searchPlace('dz')
        elif str(sz).__contains__("雅安"):
            qxdm = self.qxdm['ya']
            self.searchPlace('ya')
        elif str(sz).__contains__("阿坝"):
            qxdm = self.qxdm['abz']
            self.searchPlace('abz')
        elif str(sz).__contains__("甘孜"):
            qxdm = self.qxdm['gz']
            self.searchPlace('gz')
        elif str(sz).__contains__("凉山"):
            qxdm = self.qxdm['lsz']
            self.searchPlace('lsz')
        elif str(sz).__contains__("巴中"):
            qxdm = self.qxdm['bz']
            self.searchPlace('bz')
        elif str(sz).__contains__("眉山"):
            qxdm = self.qxdm['ms']
            self.searchPlace('ms')
        elif str(sz).__contains__("资阳"):
            qxdm = self.qxdm['zy']
            self.searchPlace('zy')

        for j in km:
            for i in self.jsjxxglkmdm:
                if i.get("KC_MC").__contains__(j):
                    temp = {"zy_bm": i.get("ZY_BM"), "kc_bm": i.get("KC_BM")}
                    coursejson.append(temp)
                    break

        for i in qxdm:
            if i.get("QX_MC").__eq__(qx):
                mainIds = i.get("QX_BM")
                qxname = i.get("QX_MC")

        # 进行科目报考
        ## 读取配置文件

        ## 创建请求参数
        subjectData = {
            # 身份证件号
            'sfzh': self.username,
            # 准考证号
            'zkzh': self.zkzh,
            # 考生类别 默认为1
            'kslb': 1,
            # 报考区县代码
            'mainIds': mainIds,
            # 报考区县名称
            'qxname': qxname,
            # 准考证号前4位
            'xx_bm': self.zkzh[0:4],
            # 报考科目
            'courseJson': coursejson.__str__()
        }
        sleep(1)
        subjectResponse = requests.post(url='https://zk.sceea.cn/RegExam/switchPage?resourceId=reg',
                                        headers=subjectheader, data=subjectData, verify=False)

        if str(subjectResponse.text).__contains__("success"):
            print(str(subjectResponse.text) + "---->报考成功")
            return str(subjectResponse.text) + "---->报考成功"
        else:
            print(str(subjectResponse.text) + "---->报考失败")
            return str(subjectResponse.text) + "---->报考失败"

        # 备用功能通过cookie 打开网页
        # def chrome(self):
        #     # chrome_options = Options()
        #     # chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        #
        #     options = Options()
        #     options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")
        #     # chrome_options.add_experimental_option('useAutomationExtension', False)
        #
        #     # 创建网页对象
        #     chromebro = webdriver.Chrome(
        #         service=Service(executable_path=os.path.join(self.BasePath, 'utils\\chromedriver.exe')),
        #         options=options)
        #
        #     # 防止检测
        #     # chromebro.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        #     #     "source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"""})
        #     # chromebro.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        #     #     "source": ""
        #     # })
        #
        #     chromebro.get("https://zk.sceea.cn")
        #
        #     chromebro.delete_all_cookies()
        #     sleep(5)
        #
        #     # 添加cookie
        #     dictionary = {}
        #     pairs = self.subjectheader['Cookie'].split(';')
        #     print(pairs)
        #     for i in pairs:
        #         if i.__eq__(''):
        #             continue
        #
        #         key, value = i.split('=')
        #         dictionary[key] = value
        #
        #     # for k, v in self.loginCookies02.items():
        #     for k, v in dictionary.items():
        #         if k == 'JSESSIONID':
        #             chromebro.add_cookie(
        #                 {"name": k, "value": v, "path": '/', "domain": "zk.sceea.cn",
        #                  'httpOnly': True, 'secure': False})
        #         if k == 'USER_UUID':
        #             chromebro.add_cookie(
        #                 {"name": k, "value": v, "path": '/', "domain": ".zk.sceea.cn",
        #                  'httpOnly': True, 'secure': False})
        #         if k == 'COMPANY_ID':
        #             chromebro.add_cookie(
        #                 {"name": k, "value": v, "path": '/', "domain": ".sceea.cn",
        #                  'httpOnly': True, 'secure': False})
        #         if k == 'ID':
        #             chromebro.add_cookie(
        #                 {"name": k, "value": v, "path": '/', "domain": ".sceea.cn",
        #                  'httpOnly': True, 'secure': False})
        #         if k == 'X-LB':
        #             chromebro.add_cookie(
        #                 {"name": k, "value": v, "path": '/', "domain": "zk.sceea.cn",
        #                  'httpOnly': False, 'secure': False, 'expiry': int((datetime.now() + timedelta(hours=5)).timestamp())})
        #         if k == 'COOKIE_SUPPORT':
        #             chromebro.add_cookie(
        #                 {"name": k, "value": v, "path": '/', "domain": "zk.sceea.cn",
        #                  'httpOnly': True, 'secure': False, 'expiry': int((datetime.now() + timedelta(weeks=52)).timestamp())})
        #         if k == 'GUEST_LANGUAGE_ID':
        #             chromebro.add_cookie(
        #                 {"name": k, "value": v, "path": '/', "domain": "zk.sceea.cn",
        #                  'httpOnly': True, 'secure': False, 'expiry': int((datetime.now() + timedelta(weeks=52)).timestamp())})
        #
        #     chromebro.add_cookie(
        #         {"name": 'LFR_SESSION_STATE_170411', 'value': '1694318298198', "path": "/", "domain": "zk.sceea.cn", 'httpOnly': False, 'secure': True})
        #
        #     print("loginCookies02：{"+self.loginCookies02+"}")
        #
        #     # with open('utils\\zk.pkl', 'rb') as f:
        #     #     cookies = pickle.load(f)
        #     # for cookie in cookies:
        #     #     chromebro.add_cookie(cookie)
        #
        #     chromebro.get("https://zk.sceea.cn/group/ks")
        #
        #     sleep(720)


class MyWindow(QWidget):
    def __init__(self):
        self.ed = education()
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
        self.ui = uic.loadUi(os.path.join(self.BASE_DIR, "zikao.ui"))

        self.usernameLabel = self.ui.usernameLabel
        self.passwordLabel = self.ui.passwordLabel
        self.usernameEdit = self.ui.usernameEdit
        self.passwordEdit = self.ui.passwordEdit
        self.codeLabel = self.ui.codeLabel
        self.codeEdit = self.ui.codeEdit
        self.loginButton = self.ui.loginButton
        self.messagelabel = self.ui.messagelabel
        self.countyBox = self.ui.countyBox
        self.countylabel = self.ui.countylabel
        self.subjectBox = self.ui.subjectBox
        self.disciplinelabel = self.ui.disciplinelabel
        self.disciplineBox = self.ui.disciplineBox
        self.registrationNoLabel = self.ui.registrationNoLabel
        self.registrationNoEdit = self.ui.registrationNoEdit
        self.candidateButton = self.ui.loginButton_2
        self.flushCodeButton = self.ui.flushCodeButton

        self.design()

    def design(self):
        ft = QFont()
        # 配置下拉框
        _translate = QtCore.QCoreApplication.translate
        subjectdata, num = ["操作系统概论",
                            "计算机网络原理",
                            "英语(二)",
                            "管理经济学",
                            "数据库系统原理",
                            "信息资源管理",
                            "运筹学基础"], 0

        with open(os.path.join(self.BASE_DIR, "utils\\cdqxdm.txt"), "r", encoding="utf-8") as fp:
            qxdm = json.load(fp)

        for i in qxdm:
            self.countyBox.addItem("")
            self.countyBox.setItemText(num, _translate("Form", i["QX_MC"]))
            num += 1

        num = 0

        for i in subjectdata:
            self.subjectBox.addItem("")
            self.subjectBox.setItemText(num, _translate("Form", i))
            num += 1

        # 配置消息加载框
        ## 图片加载
        pix = QPixmap(os.path.join(self.BASE_DIR, 'utils\\valcode.gif'))
        width = pix.width()  ##获取图片宽度
        height = pix.height()  ##获取图片高度
        if width / self.messagelabel.width() >= height / self.messagelabel.height():  ##比较图片宽度与label宽度之比和图片高度与label高度之比
            ratio = width / self.messagelabel.width()
        else:
            ratio = height / self.messagelabel.height()

        self.messagelabel.setPixmap(pix.scaled(int(width / ratio), int(height / ratio)))

        ## 配置消息文字
        ft.setPointSize(14)
        ft.setFamily("SimSun")
        self.messagelabel.setFont(ft)

        ## 配置消息滚动
        # self.scroll_msg = QScrollArea(self.ui.MyWindow)
        # self.scroll_msg.setWidget(self.messagelabel)
        # self.scroll_msg.setGeometry(QtCore.QRect(353, 10, 441, 201))
        # self.messagelabel.setAlignment(Qt.AlignTop)
        # v_layout = QVBoxLayout()
        # v_layout.addWidget(self.scroll_msg)

        # 配置触发器绑定
        import threading

        self.loginButton.clicked.connect(self.login)
        self.flushCodeButton.clicked.connect(lambda: self.code())
        self.candidateButton.clicked.connect(lambda: self.subject())

    def login(self):
        try:
            self.ed.login(username=self.usernameEdit.text(), password=self.passwordEdit.text(),
                          zkzh=self.registrationNoEdit.text(), code=self.codeEdit.text())
            self.messagelabel.setText("【" + str(self.usernameEdit.text()) + "】登录成功")
        except Exception as e:
            print(e)
            self.messagelabel.setText("登陆失败")

    def subject(self):
        try:
            self.ed.subjectRegExam(qx=self.countyBox.currentText(), km=self.subjectBox.currentText())
            self.messagelabel.setText("报考\"" + self.subjectBox.currentText() + "\"成功")
        except Exception as e:
            self.messagelabel.setText("报考失败")

    def code(self):
        try:
            self.ed.getCodePng()
        except Exception as e:
            print(e)
            self.messagelabel.setText("获取验证码失败。")
            self.messagelabel.repaint()

        pix = QPixmap(os.path.join(self.BASE_DIR, 'utils\\valcode.gif'))
        width = pix.width()  ##获取图片宽度
        height = pix.height()  ##获取图片高度
        if width / self.messagelabel.width() >= height / self.messagelabel.height():  ##比较图片宽度与label宽度之比和图片高度与label高度之比
            ratio = width / self.messagelabel.width()
        else:
            ratio = height / self.messagelabel.height()

        self.messagelabel.setPixmap(pix.scaled(int(width / ratio), int(height / ratio)))

        self.messagelabel.repaint()
