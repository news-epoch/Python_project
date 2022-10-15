import os,sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import winreg
import yaml
def getLocalPath():

    return os.path.dirname(os.path.realpath(sys.argv[0]))

def getLocalYmlFile(BASE_DIR, path):
    with open(os.path.join(BASE_DIR,path), 'r', encoding='utf-8') as fp:
        a = fp.read()

        return yaml.load(a, Loader=yaml.FullLoader)

def createdisguisedriver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    # 开启忽略浏览器证书报错
    chrome_options.add_argument('-ignore-certificate-errors')
    chrome_options.add_argument('-ignore -ssl-errors')
    s = Service(executable_path=ChromeDriverManager().install())
    return webdriver.Chrome(service=s, options=chrome_options)
def createDiscloseDriver():
    chrome_options = Options()
    chrome_options.add_experimental_option('useAutomationExtension', False)
    # 开启忽略浏览器证书报错
    chrome_options.add_argument('-ignore-certificate-errors')
    chrome_options.add_argument('-ignore -ssl-errors')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
    s = Service(executable_path=ChromeDriverManager().install())
    return webdriver.Chrome(service=s, options=chrome_options)

def is_element_exist(driver, element):
    flag = True
    try:
        driver.find_element(By.XPATH,element)
        return flag
    except:
        flag = False
        return flag



# 浏览器注册表信息



def get_browser_path(browser):
    """
    获取浏览器的安装路径

    :param browser: 浏览器名称
    """
    _browser_regs = {
        'IE': r"SOFTWARE\Clients\StartMenuInternet\IEXPLORE.EXE\DefaultIcon",
        'chrome': r"SOFTWARE\Clients\StartMenuInternet\Google Chrome\DefaultIcon",
        'edge': r"SOFTWARE\Clients\StartMenuInternet\Microsoft Edge\DefaultIcon",
        'firefox': r"SOFTWARE\Clients\StartMenuInternet\FIREFOX.EXE\DefaultIcon",
        '360': r"SOFTWARE\Clients\StartMenuInternet\360Chrome\DefaultIcon",
    }
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, _browser_regs[browser])
        print(key)
    except FileNotFoundError:
        return None
    value, _type = winreg.QueryValueEx(key, "")
    print(value)
    return value.split(',')[0]