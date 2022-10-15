from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import util
from time import sleep
import subprocess


class checkHcaptcha(object):
    def __init__(self):
        self.BASE_DIR = util.getLocalPath()
        self.localChromePath = util.get_browser_path('chrome')
        print(self.localChromePath)
        self.cmd = self.localChromePath+'chrome.exe --remote-debugging-port=9222 --user-data-dir='+self.BASE_DIR+"\\selenium\\ChromeProfile"

        self.url = 'https://dashboard.hcaptcha.com/signup?type=accessibility&r=524ad0a33287'
        self.email = '1651602236@qq.com'


    def getUrl(self):
        # driver = self.disCloseDriver(type = 'disclose')
        subprocess.run(self.cmd)
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        driver = webdriver.Chrome(options=chrome_options)
        driver = util.createDiscloseDriver()
        with open('../conf/stealth.min.js', 'r') as f:
            js = f.read()
        # driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': js})
        sleep(5)
        driver.get(self.url)

        while True:
            sleep(5)
            flag = util.is_element_exist(driver, "//input[@id='email']")
            if flag:
                break
            else:
                print("网页正在加载，请稍等。。。")
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': js})
        sleep(5)
        print("填写email")
        sendEamil = driver.find_element(By.XPATH, "//input[@id='email']")
        sendEamil.send_keys(self.email)
        sleep(5)
        print("发送邮件")
        buttonCommit = driver.find_element(By.XPATH, "//button[@aria-label='注册']/span[text()='提交']")
        buttonCommit.click()
        while True:
            sleep(10)
            flag = util.is_element_exist(driver, "//button[@aria-label='注册']/span[text()='提交中...']")
            if flag:
                print("网页正在提交中，请稍等。。。")
            else:
                sleep(30)
                break


if __name__ == '__main__':
    checkHcaptcha().getUrl()