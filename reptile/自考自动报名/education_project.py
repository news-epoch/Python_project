import requests, os, sys, json
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service




class education:
    def __init__(self):
        self.BasePath = os.path.dirname(os.path.realpath(sys.argv[0]))
        self.username = '51302919980523555X'
        self.password = '23555X'
        self.subjectheader = {

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
        print(self.homereponse_Cookie)

        homereponse.close()
    def getCodePng(self):
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

        self.imgheader['Cookie'] = self.homereponse_Cookie

        # 请求验证码
        regExamCheck = requests.get(url="https://zk.sceea.cn/c/login/hwadee/captcha?t=0.4835653767208279",
                                    headers=self.imgheader, verify=False)
        ## 保存图片

        codePngpath = os.path.join(self.BasePath, "utils\\valcode.png")
        with open(codePngpath, 'wb') as fp:
            fp.write(regExamCheck.content)

        self.regExamCheck_Cookie =  self.getCookie(regExamCheck)

        regExamCheck.close()

    def login(self):
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

        loginheader['Cookie'] = self.regExamCheck_Cookie + self.imgheader['Cookie'].__str__()

        code = input("请输入验证码")

        userforms = {
            'name': self.username,
            'pwd': self.password,
            'code': code.__str__()
        }
        flag = True
        # 重复发送登录请求
        while flag:
            loginResponse = requests.post(url="https://zk.sceea.cn/RegExam/elogin?resourceId=login",
                                          headers=loginheader, data=userforms, verify=False)
            print('登录是否成功', loginResponse.text)
            if loginResponse.text != '7':
                flag = False
                ## 保存登录的cookie
                self.subjectheader['Cookie'] = self.getCookie(loginResponse) + loginheader['Cookie'].__str__()
                print("登录成功")
                print(self.subjectheader['Cookie'])
            else:
                print("登录失败。。。。。")



    # 提交报考科目
    def subjectheader(self):
        # 进行科目报考
        coursejson = [{"zy_bm": "xxx", "kc_bm": "xxxx"}]
        ## 读取配置文件

        ## 创建请求参数
        subjectData = {
            # 身份证件号
            'sfzh': 'xxxxx',
            # 准考证号
            'zkzh': 'xxxxx',
            # 考生类别 默认为1
            'kslb': '1',
            # 报考区县代码
            'mainIds': '0131',
            # 报考区县名称
            'qxname': '蒲江县',
            # 准考证号前4位
            'xx_bm': 'xxx',
            # 报考科目
            'courseJson': coursejson.__str__()
        }

        subjectResponse = requests.post(url='https://zk.sceea.cn/RegExam/switchPage?resourceId=reg',
                                        headers=self.subjectheader, data=subjectData, verify=False)
        print(subjectResponse.text)



    def obvious_chrome(self):

        chrome_options = Options()
        # chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        self.chromebro = webdriver.Chrome(
            service=Service(executable_path=os.path.join(self.BasePath, 'utils\\chromedriver.exe')),
            options=chrome_options)  # 创建网页对象


        # 防止检测
        self.chromebro.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"""})

        # with open(os.path.join(self.BASE_DIR, 'utils\stealth.min.js'), 'r') as f:
        #     js = f.read()

        self.chromebro.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": ""
        })

    def openChrome(self):
        self.obvious_chrome()
        self.chromebro.get("https://www.baidu.com/")
        Cookie_array = self.subjectheader['Cookie'].split(";")
        Cookies = {}
        for i in Cookie_array:
            arry = i.split("=")
            print(arry)
            try:
                Cookies[arry[0]] = arry[1]
            except:
                print("报错")


        info_json = json.dumps(Cookies,sort_keys=False, indent=4, separators=(',', ': '))
        print(info_json)
        for cookie in info_json:
            self.chromebro.add_cookie(cookie)


        self.chromebro.get("https://zk.sceea.cn/group/ks")
        sleep(360)
        self.chromebro.close()






if __name__ == '__main__':
    education01 = education()
    education01.getHomeCookie()
    education01.getCodePng()
    education01.login()


