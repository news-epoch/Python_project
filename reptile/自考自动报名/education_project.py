import json
import threading

import requests, os, sys
from time import sleep

import urllib3

import util


class education:
    def __init__(self):
        self.BasePath = os.path.dirname(os.path.realpath(sys.argv[0]))
        urllib3.disable_warnings()
        self.cookies = ""

        # 地区市州代码
        self.qxdm = dict()
        with open(os.path.join(self.BasePath, "utils/四川地市州报名列表.json"), 'r', encoding='utf-8') as fp:
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
        with open(os.path.join(self.BasePath, "utils/四川地市州查询状态码.json"), 'r', encoding='utf-8') as fp:
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

        regExamCheck = requests.get(url="https://zk.sceea.cn/RegExam/login/AuthImageServlet",
                                    headers=self.imgheader, verify=False)
        ## 保存图片

        codePngpath = os.path.join(self.BasePath, "utils\\valcode.png")
        with open(codePngpath, 'wb') as fp:
            fp.write(regExamCheck.content)

        self.regExamCheck_Cookie = self.getCookie(regExamCheck)
        print("验证码regExamCheck_Cookie{" + self.regExamCheck_Cookie + "}")

        # regExamCheck.close()

    # 获取登录信息
    def getLoginInfo(self, username, password, zkzh):
        """
        获取登录信息
        :param username: 账户
        :param password: 密码
        :param zkzh: 准考证号
        """
        self.zkzh = zkzh
        self.username = username
        self.password = password
        # code = util.image_text((self.BasePath+"/"), "valcode.png")
        self.code = input("请输入验证码：")

    def login(self):
        """
        开始进行登录
        """
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
            'name': self.username,
            'pwd': self.password,
            'code': self.code.__str__()
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
                return "登录成功"
            else:
                print(loginResponse.text + "--->登录失败。。。。。")

    # 搜索余量
    def searchPlace(self, sz):
        """
        :param ds:地市名首字母缩写:
        :return:
        """
        # 将汉字转换成首字母
        sz = util.chinaConvetEnglish(sz)

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
            'dsz': self.cxdsztdm[sz],
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


    # 提交报名信息
    def subjectRegExam(self, km, qx, sz):
        """
        :param km: 科目
        :param qx: 区县
        :param sz: 市州
        :return:
        """
        # 设置头
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

        # 初始化变量
        zy_bm, kc_bm, mainIds, qxname, coursejson, qxdm = "", "", "", "", [], []

        # 查询余量
        self.searchPlace(sz=str(sz))

        # 将汉字转换成首字母单词
        Esz = util.chinaConvetEnglish(str(sz))
        qxdm = self.qxdm[Esz]

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
        print("==============开始报考==================")
        print("报考科目为："+coursejson.__str__())
        print("报考人：" + self.username)
        print("报考地区：" + qxname)

        subjectResponse = requests.post(url='https://zk.sceea.cn/RegExam/switchPage?resourceId=reg',
                                        headers=subjectheader, data=subjectData, verify=False)

        if str(subjectResponse.text).__contains__("success"):
            print(str(subjectResponse.text) + "---->报考成功")
            return "报考成功"
        else:
            print(str(subjectResponse.text) + "---->报考失败")
            return "报考失败"




