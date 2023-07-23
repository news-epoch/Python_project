from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains  # 鼠标事件
from time import sleep


class carryTiktok:
    # 初始化变量
    def __init__(self, reviewer_max_num, reviewer_min_num):
        chrome_options = Options()

        # chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        self.chromebro = webdriver.Chrome(service=Service(executable_path="../utils/chromedriver.exe"),
                                          options=chrome_options)  # 创建网页对象

        self.action = ActionChains(self.chromebro)  # 创建鼠标事件

        # 防止检测
        self.chromebro.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"""})

        with open('./utils/stealth.min.js') as f:
            js = f.read()
        self.chromebro.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": js
        })

        # 存放用户+链接列表
        self.user_urls = []
        self.reviewer_max_num = reviewer_max_num
        self.reviewer_min_num = reviewer_min_num

    def login(self):
        # 进入链接
        self.chromebro.get("https://www.tiktok.com/live")
        # 等待10s
        print("等待10s")
        # self.chromebro.add_cookie(self.dict_cookie)
        sleep(10)

        # # 使用手机 / 电子邮件 / 用户名登录
        # login_emailAndphone_element = self.chromebro.find_element(By.XPATH,
        #                                                    "//p[contains(text(),'使用手机')]")
        # login_emailAndphone_element.click()
        # login_email_element = self.chromebro.find_element(By.XPATH,
        #                                                   "//a[text()='使用电子邮件或用户名登录']")
        # login_email_element.click()
        # sleep(10)
        # # 输入手机号
        # login_input_phone_element = self.chromebro.find_element(By.XPATH,
        #                                                   "//input[@placeholder='电子邮件或用户名']")
        # login_input_phone_element.send_keys(email)

        # 扫码
        try:
            login_emailAndphone_element = self.chromebro.find_element(By.XPATH,
                                                                      "//p[contains(text(),'使用二维码')]")
        except:
            login_emailAndphone_element = self.chromebro.find_element(By.XPATH,
                                                                      "//p[contains(text(),'Use QR code')]")

        login_emailAndphone_element.click()

        print("等待120s")
        sleep(120)

        tiktokCookie = self.chromebro.get_cookies()
        print(tiktokCookie)
        sleep(20)
        self.getData()

    def getData(self):
        # 前往直播数据登录
        self.chromebro.get("https://www.tiktok.com/live")
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

        # 滚动网页
        url = set()
        for j in range(0, 20):
            # 获取直播推荐列表
            live_lists_xpath = "//div[@data-e2e='live-recommended-list']/div[1]/div"
            live_lists_elements = self.chromebro.find_elements(By.XPATH,
                                                               "//div[@data-e2e='live-recommended-list']/div[1]/div")

            #  循环直播推荐列表数据
            print("循环直播推荐列表数据")
            for i in live_lists_elements:
                sleep(0.5)
                while True:
                    try:
                        url.add(i.find_element(By.XPATH,
                                               "div[contains(@class,'DivLiveCard')]/div[@data-e2e='hot-live-recommended-card']/a").get_attribute(
                            'href').replace('/live', ''))
                        self.action.move_to_element(i.find_element(By.XPATH,
                                                                   "div[contains(@class,'DivLiveCard')]/div[contains(@class,'DivLiveInfo')]/div[contains(@class,'DivExtraInfo')]/div[@data-e2e='live-card-author-name']")).perform()
                        break
                    except:
                        print("没有找到url")
                        sleep(5)
                        continue
                print(url)

        print("读取用户数据")
        for i in url:
            data = self.toSwitchPage(i)
            if data != "null":
                print(data)
                self.user_urls.append(data)
        sleep(10)
        print(self.user_urls)

    # 抓取数据
    def toSwitchPage(self, url):

        self.chromebro.execute_script('window.open("","_blank");')  # 新建标签页

        all_handles = self.chromebro.window_handles  # 获取所有句柄
        print('client1_tab_count: ' + str(len(all_handles)))
        sleep(3)
        self.chromebro.switch_to.window(self.chromebro.window_handles[1])  # 切换到标签页2

        self.chromebro.get(url)  # 前往用户列表
        # 等待5s
        sleep(5)
        username = self.chromebro.find_element(By.XPATH, "//h1[@data-e2e='user-title']").text
        following = self.chromebro.find_element(By.XPATH,
                                                "//span[text()='已关注' and @data-e2e='following']/preceding-sibling::strong[@title='已关注']").text
        followers = self.chromebro.find_element(By.XPATH,
                                                "//span[text()='粉丝' and @data-e2e='followers']/preceding-sibling::strong[@title='粉丝']").text.replace(
            'K', '000').replace('.', '')
        likes = self.chromebro.find_element(By.XPATH,
                                            "//span[text()='赞' and @data-e2e='likes']/preceding-sibling::strong[@title='赞']").text.replace(
            'K', '000').replace('.', '')
        # 关闭当前页面
        print({'username': username, 'following': following, 'followers': followers, 'likes': likes})
        self.chromebro.close()  # 关闭标签页2
        self.chromebro.switch_to.window(self.chromebro.window_handles[0])  # 切换到标签页1
        if self.reviewer_max_num >= int(followers) >= self.reviewer_min_num:
            return {'username': username, 'following': following, 'followers': followers, 'likes': likes}
        else:
            return "null"


if __name__ == '__main__':
    test = carryTiktok(reviewer_min_num=1000, reviewer_max_num=900000)
    test.getData()
