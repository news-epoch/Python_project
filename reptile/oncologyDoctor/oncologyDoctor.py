import os
import sys
import time
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

import pandas as pd
import requests


class doctorInformationScraping:
    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
        self.test_chrome()
        self.userList = list()
        self.doctorInfoList = list()

    def test_chrome(self):
        chrome_options = uc.ChromeOptions()
        self.chromebro = uc.Chrome(options=chrome_options,
                                   driver_executable_path=os.path.join(self.BASE_DIR, r'utils/chromedriver.exe'))

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

    def obvious_chrome(self):
        chrome_options = Options()
        ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        # chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("user-agent=" + ua)

        self.chromebro = webdriver.Chrome(
            service=Service(executable_path=os.path.join(self.BASE_DIR, r'utils/chromedriver.exe')),
            options=chrome_options)  # 创建网页对象
        self.chromebro.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"""})

        with open(os.path.join(self.BASE_DIR, 'utils/stealth.min.js')) as f:
            js = f.read()
        self.chromebro.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": js
        })

    def experimental_chrome(self):
        # chrome.exe --remote-debugging-port=9527 --user-data-dir="C:\Users\Administrator\Desktop\个人资料\test\Chrome"
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")

        self.chromebro = webdriver.Chrome(
            service=Service(executable_path=os.path.join(self.BASE_DIR, r'utils/chromedriver.exe')),
            options=chrome_options)  # 创建网页对象
        self.chromebro.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"""})

        with open(os.path.join(self.BASE_DIR, 'utils/stealth.min.js')) as f:
            js = f.read()
        self.chromebro.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": js
        })
        self.chromebro.set_page_load_timeout(1800)

    def checkElement(self, element):
        for i in range(0, 10):
            try:
                time.sleep(3)
                return self.chromebro.find_element(By.XPATH, element)
            except:
                if i > 4:
                    self.chromebro.refresh()
                print("没有找到该元素，正在重试:" + element)
                time.sleep(10)
                continue
    def checkParams(self, value):
        try:
            test = value
            return test
        except:
            return '无'

    def loggin(self):
        # self.chromebro.get("https://connect.werally.com/plans/uhc")
        print("开始前往数据页面<=============================")
        self.chromebro.get("https://connect.werally.com/plans/uhc/1")
        # 点击 Medical Directory
        # while True:
        #     try:
        #         time.sleep(15)
        #         print("等待15秒")
        #         self.chromebro.find_element(By.XPATH, "//div[text()='Medical Directory']").click()
        #         break
        #     except:
        #         print("没找到该元素，重新访问页面")
        #         self.chromebro.get("https://connect.werally.com/plans/uhc")
        #         time.sleep(15)
        #
        #
        # 点击 Employer and Individual Plans
        # self.checkElement("//button[@data-ui-element-name='Employer and Individual Plans']").click()
        # time.sleep(4)

        # 点击 Options PPO with Harvard Pilgrim
        time.sleep(20)
        for i in range(0, 10):
            try:
                if self.checkElement("//button[@data-test-id='shopper']"):
                    self.checkElement("//button[@data-test-id='shopper']").click()
                    time.sleep(5)
                    break
            except:
                print("没有该元素，正在重试")
                continue
        sourceUrl = self.chromebro.current_url
        self.checkElement("//button[@data-ui-element-name='Options PPO with Harvard Pilgrim']").click()
        time.sleep(10)
        while True:
            if self.chromebro.current_url == sourceUrl:
                time.sleep(5)
                self.checkElement("//button[@data-ui-element-name='Options PPO with Harvard Pilgrim']").click()
            else:
                break
        time.sleep(6)

        # 点击 current-location-name
        self.checkElement("//p[@data-test-id='current-location-name']").click()
        time.sleep(6)

        # 输入内容 Boston, MA
        self.checkElement("//input[ @ id = 'location']").click()
        time.sleep(6)
        self.checkElement("//input[ @ id = 'location']").send_keys("Boston, MA")
        time.sleep(6)

        # # 选择内容
        self.checkElement("//button[text()='Boston, MA']").click()
        time.sleep(6)

        # 搜索内容
        self.checkElement("//button[text()='Update Location']").click()
        time.sleep(6)

        # 搜索内容oncology
        self.checkElement("//input[@placeholder='Search for providers and services' and @type='text']").click()
        self.checkElement("//input[@placeholder='Search for providers and services' and @type='text']").send_keys("oncology")
        time.sleep(6)

        # 选择内容oncology
        self.checkElement("//span[@data-testid='keyword-oncology']/strong[text()='oncology']").click()
        time.sleep(6)

        # 开始搜索
        self.checkElement("//button[@value='Search' and @type='submit']").click()
        # 选择内容Health Care Professionals
        self.checkElement("//span[contains(text(),'Health Care Professionals')]").click()
        time.sleep(10)

        self.chromebro.get_cookies()
        self.cookies = '; '.join(item for item in [item["name"] + "=" + item["value"] for item in self.chromebro.get_cookies()])

        print("=============================>已到达数据页面")

    def scrapeTheUserNumber(self,pageStart, pageEnd):
        print("1.开始抓取页数据列表<<==========================")
        # 1. 开始抓取数据
        for page_num in range(pageStart, (pageEnd+1)):  # 页数
            print("==============="+"开始抓取第 {} 页用户数据ID：".format(str(page_num))+"===============")

            self.chromebro.get("https://connect.werally.com/searchResults/02108/page-{}?term=oncology&searchType=person&lat=42.360253&long=-71.058291&propFlow=true".format(page_num))
            # 判断页面是否正确
            while True:
                try:
                    time.sleep(15)
                    self.chromebro.find_element(By.XPATH, "//div[contains(@class,'sc-dMOLTJ')]/div[1]")
                    break
                except Exception:
                    print("Error: 数据列表页面不正确")
                    self.chromebro.get("https://connect.werally.com/searchResults/02108/page-{}?term=oncology&searchType=person&lat=42.360253&long=-71.058291&propFlow=true".format(page_num))

            for i in range(1, 11):
                element = "//div[contains(@class,'search-result-in-panel')][{}]/div[@data-ui-section='enhanced-location-result']/div[1]/div[1]/div[2]/div[1]/h2[contains(@class,'providerName')]/a".format(i)
                self.userList.append(self.chromebro.find_element(By.XPATH, element).get_attribute("href"))

            print("===============" + "结束抓取第 {} 页用户数据ID：".format(str(page_num)) + "===============")

        print("==========================>>1.结束抓取页数据列表")


    def scrapeUserInformation(self):
        for userUrl in self.userList:
            self.chromebro.get(userUrl)
            infoDic = dict()
            while True:
                try:
                    time.sleep(15)
                    infoDic['title'] = self.chromebro.find_element(By.XPATH, "//div[@class='identity']/h2[@data-test-id='provider-name']").text
                    print("=======================0. 开始抓取 {} 的数据=======================".format(infoDic['title']))
                    break
                except Exception:
                    self.chromebro.get(userUrl)

            for providerDetail in ['Overview', 'Locations']:
                # 1.2 抓取基础数据
                if providerDetail == 'Overview':
                    print("----------------------------------->1. 抓取基础数据")
                    # 1.3 点击基础数据列表
                    # self.checkElement("//div[@class='navBar']/ul[1]/li[1]/a[@data-ui-element-name='Overview']").click()
                    time.sleep(4)
                    # 地址
                    try:
                        infoDic['location'] = self.chromebro.find_element(By.XPATH, "//div[@data-test-id='location-section']/div[1]/div[@data-test-id='address']").text.replace("Location", "")
                    except Exception:
                        infoDic['location'] = '无'
                    # 电话
                    try:
                        infoDic['phone'] = self.chromebro.find_element(By.XPATH, "//div[@data-test-id='location-section']/div[1]/div[@data-test-id='contact']//a[@data-test-id='phone-number']").text.replace("Phone", "")
                    except Exception:
                        infoDic['phone'] = '无'
                    # 网站
                    try:
                        infoDic['website'] = self.chromebro.find_element(By.XPATH,
                                                                         "//div[@data-test-id='location-section']/div[1]/div[@data-test-id='contact']//div[text()='Website']/following-sibling::ul[1]").text
                    except Exception:
                        infoDic['website'] = '无'
                        # 邮箱
                    try:
                        infoDic['email'] = self.chromebro.find_element(By.XPATH,
                                                                       "//div[@data-test-id='location-section']/div[1]/div[@data-test-id='contact']//div[text()='Email']/following-sibling::ul[1]").text
                    except Exception:
                        infoDic['email'] = '无'
                    # 患者年龄和性别要求
                    try:
                        infoDic['pagr'] = self.chromebro.find_element(By.XPATH,
                                                                      "//div[@data-test-id='location-section']/div[1]/div[@data-test-id='amenities']//div[text()='Patient Age & Gender Requirements']/following-sibling::p[1]").text
                    except Exception:
                        infoDic['pagr'] = '无'

                    # 附加信息
                    try:
                        infoDic['additionalInformation'] = self.chromebro.find_element(By.XPATH,
                                                                                       "//div[@data-test-id='location-section']/div[1]/div[@data-test-id='badges']//div[text()='Additional Information']/following-sibling::div[1]").text
                    except Exception:
                        infoDic['additionalInformation'] = '无'

                    # 提供者ID
                    try:
                        infoDic['providerID'] = self.chromebro.find_element(By.XPATH,
                                                                            "//div[@data-test-id='location-section']/div[1]/div[@data-test-id='badges']//h3[text()='Provider ID']/following-sibling::div[1]").text.replace(
                            "Provider ID", "").replace("Copy", "")
                    except Exception:
                        infoDic['providerID'] = '无'

                    # specialties
                    try:
                        infoDic['specialties'] = self.chromebro.find_element(By.XPATH,
                                                                             "//div[@data-test-id='provider-specialties']").text.replace(
                            "Specialties", "")
                    except Exception:
                        infoDic['specialties'] = '无'

                    # Gender
                    try:
                        infoDic['Gender'] = self.chromebro.find_element(By.XPATH,
                                                                        "//div[@data-test-id='provider-gender']").text.replace(
                            "Gender", "")
                    except Exception:
                        infoDic['Gender'] = '无'

                    # 语言
                    try:
                        infoDic['languages'] = self.chromebro.find_element(By.XPATH,
                                                                           "//div[@data-test-id='provider-languages']").text.replace(
                            "Languages Spoken", "")
                    except Exception:
                        infoDic['languages'] = '无'

                    # 工作人员使用的语言
                    try:
                        infoDic['staff-languages'] = self.chromebro.find_element(By.XPATH,
                                                                                 "//div[@data-test-id='staff-languages']").text.replace(
                            "Languages Spoken By Staff", "")
                    except Exception:
                        infoDic['staff-languages'] = '无'

                    # NPI
                    try:
                        infoDic['NPI'] = self.chromebro.find_element(By.XPATH,
                                                                     "//div[@data-test-id='npi']").text.replace("NPI",
                                                                                                                "")
                    except Exception:
                        infoDic['NPI'] = '无'
                    # 官方认证
                    try:
                        infoDic['board_certifications'] = self.chromebro.find_element(By.XPATH,
                                                                                      "//div[@data-test-id='board-certifications']/ul[1]").text
                    except Exception:
                        infoDic['board_certifications'] = '无'
                    # 文化竞争力
                    try:
                        infoDic['cultural_competence'] = self.chromebro.find_element(By.XPATH,
                                                                                     "//div[@data-test-id='cultural-competence-section']").text.replace(
                            "Cultural Competence", "")
                    except Exception:
                        infoDic['cultural_competence'] = '无'
                    # 医院从属关系
                    try:
                        infoDic['Hospital_Affiliations'] = self.chromebro.find_element(By.XPATH,
                                                                                       "//div[@data-test-id='hospital-affiliations']").text.replace(
                            "Hospital Affiliations", "")
                    except Exception:
                        infoDic['Hospital_Affiliations'] = '无'
                    # 提供商组织
                    try:
                        infoDic['Provider_Group'] = self.chromebro.find_element(By.XPATH,
                                                                                "//div[@data-test-id='provider-groups']").text.replace(
                            "Provider Group", "")
                    except Exception:
                        infoDic['Provider_Group'] = '无'
                    # 许可证
                    try:
                        infoDic['License'] = self.chromebro.find_element(By.XPATH,
                                                                         "//div[@data-test-id='license-numbers']").text.replace(
                            "License", "")
                    except Exception:
                        infoDic['License'] = '无'

                    print("1. 抓取基础数据结束<-----------------------------------")

                # 1.4抓取二级数据
                elif providerDetail == 'Locations':
                    print("------------------>2. 开始抓取locations数据")
                    while True:
                        try:
                            self.chromebro.find_element(By.XPATH, "//div[@class='navBar']/ul[1]/li[3]/a[@data-ui-element-name='Locations']").click()
                            break
                        except Exception:
                            self.chromebro.get(userUrl)
                            time.sleep(10)

                    time.sleep(5)
                    for singLocation in range(1, 6):
                        try:
                            # 地址联系方式
                            infoDic['contactInfo' + str(singLocation)] = self.chromebro.find_element(By.XPATH, "//tbody[@class='table-body locations']/tr[{}]/td[1]".format(singLocation)).text
                        except:
                            infoDic['contactInfo' + str(singLocation)] = '无'
                        try:
                            # 可用性和可访问性
                            infoDic['availabilityAccessibility' + str(singLocation)] = self.chromebro.find_element(
                                By.XPATH,
                                "//tbody[@class='table-body locations']/tr[{}]/td[contains(@ng-if,'AvailabilityAccessibility')]".format(
                                    singLocation)).text
                        except:
                            infoDic['availabilityAccessibility' + str(singLocation)] = '无'
                        try:
                            # 可用性和可访问性
                            infoDic['preferredProvider' + str(singLocation)] = self.chromebro.find_element(By.XPATH, "//tbody[@class='table-body locations']/tr[{}]/td[contains(@ng-if,'PreferredProvider')]".format(singLocation)).text
                        except:
                            infoDic['preferredProvider' + str(singLocation)] = '无'
                        try:
                            # 口语
                            infoDic['Languagesspoken' + str(singLocation)] = self.chromebro.find_element(By.XPATH, "//tbody[@class='table-body locations']/tr[{}]/td[4]".format(singLocation)).text
                        except:
                            infoDic['Languagesspoken' + str(singLocation)] = '无'
                    print("2. 抓取locations数据结束<------------------")

            print("抓取的数据为：{}".format(infoDic))
            print("=======================0. 结束抓取 {} 的数据=======================".format(infoDic['title']))
            self.doctorInfoList.append(infoDic)


    # def scrapeInformation(self):
    #     print("1.开始抓取数据<===========================")
    #     # 1. 开始抓取数据
    #     for page_num in range(1, 2):
    #         print("==============="+"开始抓取第 {} 页数据：".format(str(page_num))+"===============")
    #         # 判断页面是否正确
    #         try:
    #             time.sleep(15)
    #             self.chromebro.find_element(By.XPATH, "//div[contains(@class,'sc-dMOLTJ')]/div[1]")
    #         except Exception:
    #             print("数据列表页面不正确")
    #             self.chromebro.get("https://connect.werally.com/searchResults/02108/page-{}?term=oncology&searchType=person&lat=42.360253&long=-71.058291&propFlow=true".format(page_num))
    #
    #
    #
    #         # 1.1 循环单个doctor
    #         for i in range(1, 11):
    #             infoDic = dict()
    #             while True:
    #                 try:
    #                     print("-------------------->>>>开始进入单独数据页面")
    #                     element = "//div[contains(@class,'search-result-in-panel')][{}]/div[@data-ui-section='enhanced-location-result']/div[1]/div[1]/div[2]/div[1]/h2[contains(@class,'providerName')]/a".format(i)
    #                     sourceUrl = self.chromebro.current_url
    #                     self.chromebro.find_element(By.XPATH, element).click()
    #                     while True:
    #                         if self.chromebro.current_url == sourceUrl:
    #                             self.chromebro.find_element(By.XPATH, element).click()
    #                         else:
    #                             break
    #                     break
    #             # 进入页面数据
    #                 except Exception:
    #                     self.chromebro.get("https://connect.werally.com/searchResults/02108/page-{}?term=oncology&searchType=person&lat=42.360253&long=-71.058291&propFlow=true".format(page_num))
    #                     time.sleep(10)
    #
    #             for k in range(1, 6):
    #                 # 判断页面是否正确
    #                 try:
    #                     self.checkElement("//div[@class='identity']/h2[@data-test-id='provider-name']")
    #                     break
    #                 except Exception:
    #                     try:
    #                         self.chromebro.find_element(By.XPATH, "//div[contains(@class,'sc-dMOLTJ')]/div[1]")
    #                         self.chromebro.find_element(By.XPATH, element).click()
    #                     except Exception:
    #                         self.chromebro.get("https://connect.werally.com/searchResults/02108/page-{}?term=oncology&searchType=person&lat=42.360253&long=-71.058291&propFlow=true".format(page_num))
    #             # 开始抓取数据
    #             for providerDetail in ['Overview', 'Locations']:
    #                 # 1.2 抓取基础数据
    #                 if providerDetail == 'Overview':
    #                     print("------------->抓取基础数据<-----------------------------------")
    #                     # 1.3 点击基础数据列表
    #                     # self.checkElement("//div[@class='navBar']/ul[1]/li[1]/a[@data-ui-element-name='Overview']").click()
    #                     time.sleep(4)
    #                     # 文件头
    #                     try:
    #                         infoDic['title'] = self.chromebro.find_element("//div[@class='identity']/h2[@data-test-id='provider-name']").text
    #                     except Exception:
    #                         infoDic['title'] = '无'
    #
    #                     print("-------------开始抓取 {} 的数据-------------".format(infoDic['title']))
    #                     # 地址
    #                     try:
    #                         infoDic['location'] = self.chromebro.find_element(By.XPATH, "//div[@data-test-id='location-section']/div[1]/div[@data-test-id='address']").text.replace("Location", "")
    #                     except Exception:
    #                         infoDic['location'] = '无'
    #                     # 电话
    #                     try:
    #                         infoDic['phone'] = self.chromebro.find_element(By.XPATH,
    #                             "//div[@data-test-id='location-section']/div[1]/div[@data-test-id='contact']//a[@data-test-id='phone-number']").text
    #                     except Exception:
    #                         infoDic['phone'] = '无'
    #                     # 网站
    #                     try:
    #                         infoDic['website'] = self.chromebro.find_element(By.XPATH,
    #                             "//div[@data-test-id='location-section']/div[1]/div[@data-test-id='contact']//div[text()='Website']/following-sibling::ul[1]").text
    #                     except Exception:
    #                         infoDic['website'] = '无'
    #                         # 邮箱
    #                     try:
    #                         infoDic['email'] = self.chromebro.find_element(By.XPATH,
    #                             "//div[@data-test-id='location-section']/div[1]/div[@data-test-id='contact']//div[text()='Email']/following-sibling::ul[1]").text
    #                     except Exception:
    #                         infoDic['email'] = '无'
    #                     # 患者年龄和性别要求
    #                     try:
    #                         infoDic['pagr'] = self.chromebro.find_element(By.XPATH,
    #                             "//div[@data-test-id='location-section']/div[1]/div[@data-test-id='amenities']//div[text()='Patient Age & Gender Requirements']/following-sibling::p[1]").text
    #                     except Exception:
    #                         infoDic['pagr'] = '无'
    #
    #                     # 附加信息
    #                     try:
    #                         infoDic['additionalInformation'] = self.chromebro.find_element(By.XPATH,
    #                             "//div[@data-test-id='location-section']/div[1]/div[@data-test-id='badges']//div[text()='Additional Information']/following-sibling::div[1]").text
    #                     except Exception:
    #                         infoDic['additionalInformation'] = '无'
    #
    #                     # 提供者ID
    #                     try:
    #                         infoDic['providerID'] = self.chromebro.find_element(By.XPATH,
    #                             "//div[@data-test-id='location-section']/div[1]/div[@data-test-id='badges']//h3[text()='Provider ID']/following-sibling::div[1]").text.replace("Provider ID", "").replace("Copy", "")
    #                     except Exception:
    #                         infoDic['providerID'] = '无'
    #
    #                     # specialties
    #                     try:
    #                         infoDic['specialties'] = self.chromebro.find_element(By.XPATH, "//div[@data-test-id='provider-specialties']").text.replace("Specialties", "")
    #                     except Exception:
    #                         infoDic['specialties'] = '无'
    #
    #                     # Gender
    #                     try:
    #                         infoDic['Gender'] = self.chromebro.find_element(By.XPATH, "//div[@data-test-id='provider-gender']").text.replace("Gender", "")
    #                     except Exception:
    #                         infoDic['Gender'] = '无'
    #
    #                     # 语言
    #                     try:
    #                         infoDic['languages'] = self.chromebro.find_element(By.XPATH, "//div[@data-test-id='provider-languages']").text.replace("Languages Spoken", "")
    #                     except Exception:
    #                         infoDic['languages'] = '无'
    #
    #                     # 工作人员使用的语言
    #                     try:
    #                         infoDic['staff-languages'] = self.chromebro.find_element(By.XPATH, "//div[@data-test-id='staff-languages']").text.replace("Languages Spoken By Staff", "")
    #                     except Exception:
    #                         infoDic['staff-languages'] = '无'
    #
    #                     # NPI
    #                     try:
    #                         infoDic['NPI'] = self.chromebro.find_element(By.XPATH, "//div[@data-test-id='npi']").text.replace("NPI", "")
    #                     except Exception:
    #                         infoDic['NPI'] = '无'
    #                     # 官方认证
    #                     try:
    #                         infoDic['board_certifications'] = self.chromebro.find_element(By.XPATH, "//div[@data-test-id='board-certifications']/ul[1]").text
    #                     except Exception:
    #                         infoDic['board_certifications'] = '无'
    #                     # 文化竞争力
    #                     try:
    #                         infoDic['cultural_competence'] = self.chromebro.find_element(By.XPATH, "//div[@data-test-id='cultural-competence-section']").text.replace("Cultural Competence", "")
    #                     except Exception:
    #                         infoDic['cultural_competence'] = '无'
    #                     # 医院从属关系
    #                     try:
    #                         infoDic['Hospital_Affiliations'] = self.chromebro.find_element(By.XPATH, "//div[@data-test-id='hospital-affiliations']").text.replace("Hospital Affiliations", "")
    #                     except Exception:
    #                         infoDic['Hospital_Affiliations'] = '无'
    #                     # 提供商组织
    #                     try:
    #                         infoDic['Provider_Group'] = self.chromebro.find_element(By.XPATH, "//div[@data-test-id='provider-groups']").text.replace("Provider Group", "")
    #                     except Exception:
    #                         infoDic['Provider_Group'] = '无'
    #                     # 许可证
    #                     try:
    #                         infoDic['License'] = self.chromebro.find_element(By.XPATH, "//div[@data-test-id='license-numbers']").text.replace("License", "")
    #                     except Exception:
    #                         infoDic['License'] = '无'
    #
    #                 # 1.4抓取二级数据
    #                 elif providerDetail == 'Locations':
    #                     print("------------>开始抓取locations数据<------------------")
    #                     self.checkElement("//div[@class='navBar']/ul[1]/li[3]/a[@data-ui-element-name='Locations']").click()
    #                     time.sleep(5)
    #                     for singLocation in range(1, 6):
    #                         try:
    #                             # 地址联系方式
    #                             infoDic['contactInfo' + str(singLocation)] = self.chromebro.find_element(By.XPATH, "//tbody[@class='table-body locations']/tr[{}]/td[1]".format(singLocation)).text
    #                         except:
    #                             infoDic['contactInfo' + str(singLocation)] = '无'
    #                         try:
    #                             # 可用性和可访问性
    #                             infoDic['availabilityAccessibility' + str(singLocation)] = self.chromebro.find_element(
    #                                 By.XPATH,
    #                                 "//tbody[@class='table-body locations']/tr[{}]/td[contains(@ng-if,'AvailabilityAccessibility')]".format(
    #                                     singLocation)).text
    #                         except:
    #                             infoDic['availabilityAccessibility' + str(singLocation)] = '无'
    #                         try:
    #                             # 可用性和可访问性
    #                             infoDic['preferredProvider' + str(singLocation)] = self.chromebro.find_element(By.XPATH,
    #                                                                                                            "//tbody[@class='table-body locations']/tr[{}]/td[contains(@ng-if,'PreferredProvider')]".format(
    #                                                                                                                singLocation)).text
    #                         except:
    #                             infoDic['preferredProvider' + str(singLocation)] = '无'
    #                         try:
    #                             # 口语
    #                             infoDic['Languagesspoken' + str(singLocation)] = self.chromebro.find_element(By.XPATH,
    #                                                                                                          "//tbody[@class='table-body locations']/tr[{}]/td[4]".format(
    #                                                                                                              singLocation)).text
    #                         except:
    #                             infoDic['Languagesspoken' + str(singLocation)] = '无'
    #
    #             # 返回上一页
    #             time.sleep(3)
    #             self.doctorList.append(infoDic)
    #             print(self.doctorList)
    #             self.checkElement("//div[@tabindex='0']/button[@class='backButton' and @aria-label='Back Button']").click()
    #             time.sleep(4)
    #
    #         # try:
    #         #     # 点击下一页
    #         #     self.chromebro.find_element(By.XPATH, "//button[@data-ui-element-name='next-page' and @aria-disabled='true']").click()
    #         #     time.sleep(5)
    #         # except:
    #         #     break

    def export_excel(self, fileName):
        pf = pd.DataFrame(self.doctorInfoList)
        pf.to_excel(fileName, index=False)

if __name__ == '__main__':
    doctor = doctorInformationScraping()
    doctor.loggin()

    # doctor.scrapeTheUserNumber(1, 10)  表示抓取1，10页的数据
    doctor.scrapeTheUserNumber(pageStart=1, pageEnd=10)
    print(doctor.userList)
    doctor.scrapeUserInformation()
    print(doctor.doctorInfoList)
    doctor.export_excel(fileName="doctor.xlsx")
