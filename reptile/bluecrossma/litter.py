from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
class Doctor_reptile:
    # 配置无头浏览器
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
        s = Service(executable_path="./utils/chromedriver.exe")
        self.bro = Chrome(service=s, options=chrome_options)
        self.util = utils()

    # 前往数据页面
    def ToDateList(self):
        ## 访问初始化页面
        self.bro.get("https://www.bluecrossma.org/")

        ## 点击个人元素

        self.check_ByXPATH("//a[@title='Find in-network doctors']").click()
        ## 点击Doctor
        self.check_ByXPATH("//input[@id='provider-input']").click()
        ## 点击All Specialties
        self.check_ByXPATH("//a[contains(text(),'All Specialties')]").click()
        ## 点击M
        self.check_ByXPATH("//div[text()='M']").click()
        ## 点击Medical Oncology
        self.check_ByXPATH("//div[text()='Medical Oncology']").click()
        ## 点击Network下拉框元素
        self.check_ByXPATH("//div[@class='mat-form-field-suffix ng-tns-c2794762957-7 ng-star-inserted']").click()
        ## 选择Network元素数据
        self.check_ByXPATH("//span[contains(text(),' PREFERRED BLUE PPO OPTIONS V.5 ')]").click()
        ## 输入城市
        self.check_ByXPATH("//input[@id='zipcode-input']").send_keys("02108 - Boston, MA")
        ## 点击Search
        self.check_ByXPATH("//span[@class='slot primary'and contains(text(),'Search')]").click()

        ## 当页面有问题时
        utils().printtime(num_time=2)
        if (self.bro.find_element(By.XPATH, "//span[contains(text(),'Try again')]/parent::button")):
            ### 点击×元素
            self.bro.find_element(By.XPATH, "//a[@class='black-text modal-close cursor-pointer']").click()
            ### 点击Search
            self.bro.find_element(By.XPATH, "//span[@class='slot primary'and contains(text(),'Search')]").click()

    def check_ByXPATH(self, element):
        while True:
            time.sleep(2)
            try:
                findElement = self.bro.find_element(By.XPATH, element)
                return findElement
            except Exception:
                print("等待2s" + element)
                continue


class utils:
    def printtime(self, num_time):
        print("等待" + str(num_time) + "秒")
        time.sleep(int(num_time))