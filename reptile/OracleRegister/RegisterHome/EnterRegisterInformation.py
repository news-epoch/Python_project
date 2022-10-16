from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

def is_element_exist(driver, element):
    flag = True
    try:
        driver.find_element(By.XPATH,element)
        return flag
    except:
        flag = False
        return flag

def page1(driver,data):
    inputData = data
    # 输入别名
    while True:
        sleep(10)
        test = is_element_exist(driver=driver,element="//input[@id='alternateName']")
        if test:
            break
        else:
            print("未找到资源，请稍等。。。")

    print("输入基础信息中")
    alternateName_driver = driver.find_element(By.XPATH, "//input[@id='alternateName']")
    alternateName_driver.send_keys(inputData['alternateName'])

    # 输入密码
    password_driver = driver.find_element(By.XPATH, "//input[@name='password']")
    password_driver.send_keys(inputData['Password'])
    ## 确认密码
    newPassword_driver = driver.find_element(By.XPATH, "//input[@name='matchPassword']")
    newPassword_driver.send_keys(inputData['Password'])
    # 单击个人按钮
    radio_driver = driver.find_element(By.XPATH, "//input[@id='individual-customer-radio']")
    radio_driver.click()

    # 选择主区域
    print("选择主区域："+inputData['area'])
    area_driver = driver.find_element(By.XPATH, "//input[@id='react-select-3-input']")
    area_driver.send_keys(inputData['area'])
    area_driver.send_keys(Keys.ENTER)

    # 点击确认
    print("检测页面加载按钮是否正常中...")
    for  i in range(0,4):
        sleep(10)
        test = is_element_exist(driver=driver,element="//div[@class='termsComponent']/button[@class='solid']/@disabled")
        if test:
            print("网络不好导致，页面不正常，正在等待加载，等待30s，自动关闭程序")
        else:
            break
    print("点击下一页")
    button_driver = driver.find_element(By.XPATH, "//div[@class='termsComponent']/button[@class='solid']")
    button_driver.click()

def page2(driver,data):
    inputData = data
    print("检测页面是否加载成功")
    while True:
        sleep(10)
        test = is_element_exist(driver=driver, element="//input[@id='address1']")
        if test:
            print("页面加载成功")
            break
        else:
            print("网络不好，等待10s")

    print("输入地址信息中")
    address_driver = driver.find_element(By.XPATH, "//input[@id='address1']")
    address_driver.send_keys(inputData['address'])

    # 填写城市
    city_driver = driver.find_element(By.XPATH, "//input[@id='city']")
    city_driver.send_keys(inputData['city'])

    # 填写省份
    province_driver = driver.find_element(By.XPATH, "//input[@id='province']")
    province_driver.send_keys(inputData['province'])

    # 填写邮政编码

    postalcode_driver = driver.find_element(By.XPATH, "//input[@id='postalcode']")
    postalcode_driver.send_keys(inputData['code'])

    # 填写电话号码
    phoneNumber_driver = driver.find_element(By.XPATH, "//input[@id='phoneNumber']")
    phoneNumber_driver.send_keys(inputData['phoneNumber'])
    sleep(5)
    print("检查按钮是否正常")
    while True:
        test = is_element_exist(driver=driver, element="//form[@autocomplete='off']/button[@class='solid']/@disabled")
        if test:
            sleep(10)
            print("网络不好，等待10s")

        else:
            break
    # 点击继续
    button_driver = driver.find_element(By.XPATH, "//form[@autocomplete='off']/button[@class='solid']")
    button_driver.click()

def page3(driver,paydata):
    payData0 = paydata
    print("开始加载添加银行卡界面")
    button_driver = driver.find_element(By.XPATH, "//div[@class='accordionSection']/div/button[@class='solid']")
    button_driver.click()
#//div[@class='accordionSection']/div[@class='accordionSectionHeader']/div[@class='accordionArrow']/div[1]
    sleep(5)
    # 进入iframe页面
    # 判断是否正在加载
    for i in range(0, 5):
        sleep(10)
        test = is_element_exist(driver=driver, element="//iframe[@id='opayifrm']")
        if test:
            break
        else:
            print("填写银行卡界面加载不出来，等待30s")
            if i == 3:
                print("返回上一页")
                returntwoPage = driver.find_element(By.XPATH,"//div[@class='accordionSection']/div[@class='accordionSectionHeader']/div[@class='accordionArrow']/div[1]")
                returntwoPage.click()
                print("等待2s，重回下一页")
                sleep(2)
                reclassbutton_driver = driver.find_element(By.XPATH, "//form[@autocomplete='off']/button[@class='solid']")
                reclassbutton_driver.click()
                button_driver = driver.find_element(By.XPATH, "//div[@class='accordionSection']/div/button[@class='solid']")
                button_driver.click()
                print("再次加载添加银行卡界面中，等待10s，若不存在，则关闭重新注册")

    driver.switch_to.frame(driver.find_element(By.XPATH, "//iframe[@id='opayifrm']"))
    ## 点击添加银行卡
    for i in range(0,4):
        sleep(10)
        test = is_element_exist(driver=driver, element="//div[text()='Credit Card']")
        if test:
            break
        else:
            print("等待页面加载成功，等待10s")
            if i == 3:
                closePay = driver.find_element(By.XPATH,"//a[@id='ps-close-button']//use")
                closePay.click()
                driver.switch_to.default_content()
                print("返回上一页")
                returntwoPage = driver.find_element(By.XPATH,"//div[@class='accordionSection']/div[@class='accordionSectionHeader']/div[@class='accordionArrow']/div[1]")
                returntwoPage.click()
                print("等待2s，重回下一页")
                sleep(2)
                reclassbutton_driver = driver.find_element(By.XPATH, "//form[@autocomplete='off']/button[@class='solid']")
                reclassbutton_driver.click()
                button_driver = driver.find_element(By.XPATH, "//div[@class='accordionSection']/div/button[@class='solid']")
                button_driver.click()
                print("再次加载添加银行卡界面中，等待10s，若不存在，则关闭重新注册")
                sleep(20)
                driver.switch_to.frame(driver.find_element(By.XPATH, "//iframe[@id='opayifrm']"))

    addPayDiv_driver = driver.find_element(By.XPATH, "//div[text()='Credit Card']")
    addPayDiv_driver.click()
    sleep(10)
    ## 填写银行卡数据
    ### 切换主页面
    driver.switch_to.default_content()
    ### 跳转到内嵌iframe
    driver.switch_to.frame(driver.find_element(By.XPATH, "//iframe[@id='opayifrm']"))
    for i in range(0,3):
        sleep(10)
        test = is_element_exist(driver=driver, element="//iframe[@data-testid='paymentGateway']")
        if test:
            break
        else:
            print("等待页面加载成功，等待30s")

    driver.switch_to.frame(driver.find_element(By.XPATH, "//iframe[@data-testid='paymentGateway']"))
    ### 填写数据
    print("填写银行卡数据中...")
    bill_to_forename_driver = driver.find_element(By.XPATH, "//input[@id='bill_to_forename']")
    bill_to_forename_driver.send_keys(Keys.RIGHT)  # 光标向右移方便删除
    bill_to_forename_driver.send_keys(Keys.BACKSPACE)  # 删除键
    bill_to_forename_driver.send_keys(payData0['lastName'])

    bill_to_surname_driver = driver.find_element(By.XPATH, "//input[@id='bill_to_surname']")
    bill_to_surname_driver.send_keys(Keys.RIGHT)  # 光标向右移方便删除
    bill_to_surname_driver.send_keys(Keys.BACKSPACE)  # 删除键
    bill_to_surname_driver.send_keys(payData0['firstName'])

    cardNumber_driver = driver.find_element(By.XPATH, "//input[@id='card_number']")
    cardNumber_driver.send_keys(Keys.RIGHT)  # 光标向右移方便删除
    cardNumber_driver.send_keys(Keys.BACKSPACE)  # 删除键
    cardNumber_driver.send_keys(payData0['cardNumber'])

    card_cvn_driver = driver.find_element(By.XPATH, "//input[@id='card_cvn']")
    card_cvn_driver.send_keys(Keys.RIGHT)  # 光标向右移方便删除
    card_cvn_driver.send_keys(Keys.BACKSPACE)  # 删除键
    card_cvn_driver.send_keys(payData0['cvn'])

    ### 选择卡类型
    sleep(2)
    addPayDiv_driver = driver.find_element(By.XPATH, "//input[@id='card_type_001']")
    addPayDiv_driver.click()

    ### 选择年月
    month_element = "//select[@id='card_expiry_month']/option[@value='" + payData0['month'] + "']"
    year_element = "//select[@id='card_expiry_year']/option[@value='" + payData0['year'] + "']"
    month_driver = driver.find_element(By.XPATH, month_element)
    month_driver.click()
    year_driver = driver.find_element(By.XPATH, year_element)
    year_driver.click()
    sleep(5)

    ### 确认完成
    Finish_driver = driver.find_element(By.XPATH, "//input[@value='Finish']")
    Finish_driver.click()

    sleep(10)

    ## 关闭界面
    ### 切换主页面
    driver.switch_to.default_content()
    ### 跳转到内嵌iframe
    print("添加银行卡成功，关闭添加页面")
    driver.switch_to.frame(driver.find_element(By.XPATH, "//iframe[@id='opayifrm']"))
    while True:
        sleep(10)
        test = is_element_exist(driver=driver, element="//div[@data-testid='paymentConfirmation']//span[text()='Close']")
        if test:
            break
        else:
            print("正在加载中，等待10s")
    payClose_driver = driver.find_element(By.XPATH, "//div[@data-testid='paymentConfirmation']//span[text()='Close']")
    payClose_driver.click()
    sleep(5)

    # 确认协议
    ### 切换主页面
    driver.switch_to.default_content()
    sterm_driver = driver.find_element(By.XPATH, "//label[@class='rw-checkbox']/div[@class='checkmark']")
    sterm_driver.click()

    sleep(10)
    # 开始试用
    start_driver = driver.find_element(By.XPATH, "//button[@id='startMyTrialBtn']")
    start_driver.click()

    for i in range(1,5):
        test = is_element_exist(driver, element="//div[@class='notifierContainer']//h4")
        if test:
            break
        else:
            sleep(5)
    end_driver = driver.find_element(By.XPATH,"//div[@class='notifierContainer']//h4")
    print("返回注册结果中")
    for i in range(1,10):
        if end_driver.text =='处理交易时出错' or end_driver.text == 'Error processing transaction':
            print(end_driver.text)
            print("注册失败")
            break
        else:
            print("注册成功")
            sleep(90)