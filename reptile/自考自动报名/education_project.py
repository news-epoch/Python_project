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
        self.cdqxdm = [{"QX_BM": "0123", "QX_MC": "温江区"},
                       {"QX_BM": "0132", "QX_MC": "新津区"},
                       {"QX_BM": "0108", "QX_MC": "成华区"},
                       {"QX_BM": "0112", "QX_MC": "龙泉驿区"},
                       {"QX_BM": "0121", "QX_MC": "金堂县"},
                       {"QX_BM": "0104", "QX_MC": "锦江区"},
                       {"QX_BM": "0183", "QX_MC": "邛崃市"},
                       {"QX_BM": "0106", "QX_MC": "金牛区"},
                       {"QX_BM": "0184", "QX_MC": "崇州市"},
                       {"QX_BM": "0195", "QX_MC": "双流区(信息工程大学)"},
                       {"QX_BM": "0105", "QX_MC": "青羊区"},
                       {"QX_BM": "0107", "QX_MC": "武侯区"},
                       {"QX_BM": "0124", "QX_MC": "郫都区"},
                       {"QX_BM": "0129", "QX_MC": "大邑县"},
                       {"QX_BM": "0182", "QX_MC": "彭州市"},
                       {"QX_BM": "0113", "QX_MC": "青白江区"},
                       {"QX_BM": "0111", "QX_MC": "天府新区"},
                       {"QX_BM": "0180", "QX_MC": "简阳市"},
                       {"QX_BM": "0181", "QX_MC": "都江堰市"},
                       {"QX_BM": "0122", "QX_MC": "双流区"},
                       {"QX_BM": "0125", "QX_MC": "新都区"},
                       {"QX_BM": "0131", "QX_MC": "蒲江县"}]
        self.zgqxdm = [{"QX_MC": "自流井区", "QX_BM": "0302"},
                       {"QX_MC": "沿滩区", "QX_BM": "0311"},
                       {"QX_MC": "大安区", "QX_BM": "0304"},
                       {"QX_MC": "富顺县", "QX_BM": "0322"},
                       {"QX_MC": "荣  县", "QX_BM": "0321"},
                       {"QX_MC": "贡井区", "QX_BM": "0303"}]
        self.leqxdm = [{"QX_MC": "沙湾区", "REST_A": 149, "REST_B": 37, "REST_C": 130, "REST_D": 0, "QX_BM": "1111"},
                       {"QX_MC": "金口河区", "REST_A": 34, "REST_B": 19, "REST_C": 32, "REST_D": 18, "QX_BM": "1113"},
                       {"QX_MC": "沐川县", "REST_A": 255, "REST_B": 245, "REST_C": 258, "REST_D": 242, "QX_BM": "1129"},
                       {"QX_MC": "市中区", "REST_A": 0, "REST_B": 0, "REST_C": 0, "REST_D": 0, "QX_BM": "1102"},
                       {"QX_MC": "夹江县", "REST_A": 0, "REST_B": 0, "REST_C": 3, "REST_D": 0, "QX_BM": "1126"},
                       {"QX_MC": "马边县", "REST_A": 842, "REST_B": 815, "REST_C": 847, "REST_D": 815, "QX_BM": "1133"},
                       {"QX_MC": "井研县", "REST_A": 13, "REST_B": 0, "REST_C": 22, "REST_D": 0, "QX_BM": "1124"},
                       {"QX_MC": "峨边县", "REST_A": 71, "REST_B": 47, "REST_C": 64, "REST_D": 49, "QX_BM": "1132"},
                       {"QX_MC": "五通桥区", "REST_A": 61, "REST_B": 0, "REST_C": 69, "REST_D": 0, "QX_BM": "1112"},
                       {"QX_MC": "峨眉山市", "REST_A": 27, "REST_B": 0, "REST_C": 49, "REST_D": 0, "QX_BM": "1181"},
                       {"QX_MC": "犍为县", "REST_A": 384, "REST_B": 338, "REST_C": 401, "REST_D": 322, "QX_BM": "1123"}]
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

    def getCodePng(self):
        """
        获取验证码图片请求
        :return:
        """
        # 请求头
        self.imgheader = {
            "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Host": "zk.sceea.cn",
            "Referer": "https://zk.sceea.cn/",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "Sec-Fetch-Dest": "image",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"

        }

        # 添加cookie
        self.imgheader['Cookie'] = self.homereponse_Cookie

        # 请求验证码

        regExamCheck = requests.get(url="https://zk.sceea.cn/RegExam/login/AuthImageServlet?t=0.3586720730887125",
                                    headers=self.imgheader, verify=False)
        ## 保存图片

        codePngpath = os.path.join(self.BasePath, "utils\\valcode.gif")
        with open(codePngpath, 'wb') as fp:
            fp.write(regExamCheck.content)

        self.regExamCheck_Cookie = self.getCookie(regExamCheck)
        print("regExamCheck_Cookie{" + self.regExamCheck_Cookie + "}")

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
        loginheader = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '44',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
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

        loginheader['Cookie'] = self.regExamCheck_Cookie + self.homereponse_Cookie

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
            loginResponse = requests.post(url="https://zk.sceea.cn/RegExam/elogin?resourceId=login",
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

    def searchPlace(self):
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '74',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Cookie': 'JSESSIONID=0672791BFD94E8219872A68C26538992; X-LB=2.69.44db11e9.1f90; JSESSIONID=C74355E1C659DFCC732D284D08E688B7; allan=Z59Z9M72P59M732M72O555325M7B399P592M73P55',
            'Host': 'zk.sceea.cn',
            'Origin': 'https://zk.sceea.cn',
            'Referer': "https://zk.sceea.cn/RegExam/switchPage?resourceId=view&zkz=010818443102",
            'Sec-Ch-Ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '\"Windows\"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        headers['Cookie'] = self.Cookies
        data = {
            'bkzt': '',
            'qxbm': '',
            'sfzh': '51302919980523555x',
            'dsz': '01',
            'stuType': '1',
            'stuScope': '0108',
            'times': 'D'
        }
        response = requests.post("https://zk.sceea.cn/RegExam/switchPage?resourceId=searchPlace", headers=headers,
                                 data=data, verify=False)
        jsonData = response.json()
        sleep(1)
        print("考区编码\t考区\t\t第一天上午\t第一天下午\t第二天上午\t第二天下午")
        for i in jsonData["data"]:
            print(str(i["QX_BM"]) + "\t" + str(i["QX_MC"]) + "\t\t" + str(i["REST_A"]) + "\t\t" + str(
                i["REST_B"]) + "\t\t" + str(i["REST_C"]) + "\t\t" + str(i["REST_D"]))

        return jsonData

    def subjectRegExam(self, km, qx):
        """
        :param km: 科目
        :param qx: 区县
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

        zy_bm, kc_bm, mainIds, qxname, coursejson = "", "", "", "", []

        for j in km:
            for i in self.jsjxxglkmdm:
                if i.get("KC_MC").__contains__(j):
                    temp = {"zy_bm": i.get("ZY_BM"), "kc_bm": i.get("KC_BM")}
                    coursejson.append(temp)
                    break

        for i in self.cdqxdm:
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
        print(subjectResponse.text + "---->报考失败")
        return subjectResponse.text

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


if __name__ == '__main__':
    education01 = education()
    # education01.getHomeCookie()
    # education01.getCodePng()
    education01.login(username="51302919980523555X", password="23555X", zkzh="010818443102")
    # education01.login(username="510411199904011426", password="011426", zkzh="010818443068")
    # education01.chrome()
    while True:
        json = education01.searchPlace()
        for i in json["data"]:
            if i['QX_MC'] == '新都区' and i['REST_D'] != 0:
                text = education01.subjectRegExam(["计算机网络原理"], "新都区")
                if text != '5' or text == 'success':
                    break
                elif text == '5' or text == 5:
                    continue
                break

    # QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    # App = QApplication(sys.argv)  # 创建QApplication对象，作为GUI主程序入口
    # stats = MyWindow()
    # stats.ui.show()  # 显示主窗体
    # sys.exit(App.exec_())
