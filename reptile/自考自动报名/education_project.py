import json

from requests import request
import requests
import os,sys
# import yaml
# from selenium.webdriver.common.by import  By
# from time import sleep
# def readYamlFile():
#     with open("../lib/subjectdata.yml",'r',encoding='utf-8') as fp:
#         a = fp.read()
#         yaml.load(a, loader=yaml.FullLoader)

def getPath():
    return os.path.dirname(os.path.realpath(sys.argv[0]))
def gerCookie(response):
    cookie_value = ''
    for key, value in response.cookies.items():
        cookie_value += key + '=' + value + ';'
    return cookie_value


def request_info():
    fiddler_proxies = {'http': 'http://127.0.0.1:8888', 'https': 'http://127.0.0.1:8888'}
    s = requests.session()
    #请求头设置
    imgheader = {
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

    AllCookie = {}
    # 请求主页cookie
    homereponse = requests.get(url="https://zk.sceea.cn/", headers=homeheader, verify=False,  proxies=fiddler_proxies)

    ## 转换cookie
    imgheader['Cookie'] = gerCookie(homereponse)

    # 请求验证码
    regExamCheck = requests.get(proxies=fiddler_proxies, url="https://zk.sceea.cn/RegExam/login/AuthImageServlet", headers=imgheader, verify=False)

    ## 保存图片
    BasisPath  = getPath()
    codePng = os.path.join(BasisPath,"utils\\valcode.png")
    with open("../utils/valcode.png", 'wb') as fp:
        fp.write(regExamCheck.content)
    print("等待10s")
    # 保存cookie
    # regExamCheckCookies = {i.split("=")[1]: i.split("=")[1] for i in regExamCheck.cookies.__str__().split("; ")}
    loginheader['Cookie'] = gerCookie(regExamCheck) + imgheader['Cookie'].__str__()
    print(loginheader['Cookie'])
    # 发送登录请求
    code = input("请输入验证码：")

    # userData = readYamlFile('user.yml')
    userforms = {
        'name': 'xxxxx',
        'pwd': 'xxxxx',
        'code': code.__str__()
    }
    flag = True


    # 重复发送登录请求
    while flag:
        loginResponse = requests.post(proxies=fiddler_proxies, url="https://zk.sceea.cn/RegExam/elogin?resourceId=login", headers=loginheader, data=userforms, verify=False)
        print('登录是否成功', loginResponse.text)
        if loginResponse.text != '7':
            flag = False
            ## 保存登录的cookie
            subjectheader['Cookie'] = gerCookie(loginResponse)+loginheader['Cookie'].__str__()
            print(subjectheader['Cookie'])
        else:
            flag = True


    # 进行科目报考
    ## 读取配置文件
    coursejson = [{"zy_bm": "xxx", "kc_bm": "xxxx"}]
    ## 创建请求参数
    subjectData1 = 'sfzh=xxxxxx&zkzh=xxxxxxx&kslb=1&mainIds=0131&qxname=%E8%92%B2%E6%B1%9F%E5%8E%BF&xx_bm=0108&courseJson=%5B%7B%22zy_bm%22%3A+%22Y082208%22%2C%22kc_bm%22%3A+%2202628%22%7D%5D'
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

    subjectResponse = requests.post(proxies=fiddler_proxies, url='https://zk.sceea.cn/RegExam/switchPage?resourceId=reg', headers=subjectheader, data=subjectData, verify=False)
    print(subjectResponse.text)



if __name__ == '__main__':
    BasisPath = getPath()
    codePng = os.path.join(BasisPath, "utils\\valcode.png")
    print(codePng)
