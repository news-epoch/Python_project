from selenium import webdriver
from RegisterHome import getEmailUrl
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep


def main():
    # 登录163邮件
    url = getEmailUrl.getNewOracleClode(getEmailUrl.login())
    # 打开浏览器
    driver = webdriver.Chrome("../utils/chromedriver.exe")
    driver.get(url)

    inputData = {
        'alternateName' : 'newsepoch',
        'Password':'Cwg819730159@',
        'area' :'South Korea North (Chuncheon)',
        'address':'ming ren feng jing',
        'city':'Chengdu',
        'province':'Sichuan',
        'code':'610043',
        'phoneNumber':'8615760657744'
    }
    payData0 = {
        'lastName' : 'weiguo',
        'firstName': 'chen',
        'cardNumber':'4041178990751650',
        'month':'07',
        'year':'2027',
        'cvn':'742'
    }
    payData1 = {
        'lastName' : 'Weiguo',
        'firstName': 'Chen',
        'cardNumber':'4691460027898552',
        'month':'07',
        'year':'2030',
        'cvn':'964'
    }
    # 输入别名
    sleep(30)
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
    area_driver = driver.find_element(By.XPATH, "//input[@id='react-select-3-input']")
    area_driver.send_keys(inputData['area'])
    area_driver.send_keys(Keys.ENTER)

    # 点击确认
    button_driver = driver.find_element(By.XPATH, "//button[text()='继续']")
    button_driver.click()
    sleep(20)

    # 填写地址
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

    # 点击继续
    button_driver = driver.find_element(By.XPATH, "//button[text()='继续']")
    button_driver.click()

    # 添加银行卡

    button_driver = driver.find_element(By.XPATH, "//button[text()='添加付款验证方式']")
    button_driver.click()

    sleep(15)

    # 进入iframe页面
    driver.switch_to(driver.find_element(By.XPATH, "//iframe[@id='opayifrm']"))
    ## 点击添加银行卡
    addPayDiv_driver = driver.find_element(By.XPATH, "//div[text()='Credit Card']")
    addPayDiv_driver.click()
    sleep(10)
    ## 填写银行卡数据
    ### 切换主页面
    driver.switch_to.default_content()
    ### 跳转到内嵌iframe
    driver.switch_to(driver.find_element(By.XPATH, "//iframe[@id='opayifrm']"))
    driver.switch_to(driver.find_element(By.XPATH, "//iframe[@data-testid='paymentGateway']"))
    ### 填写数据
    bill_to_forename_driver = driver.find_element(By.XPATH, "//input[@id='bill_to_forename']")
    bill_to_forename_driver.send_keys(payData0['lastName'])

    bill_to_surname_driver = driver.find_element(By.XPATH, "//input[@id='bill_to_surname']")
    bill_to_surname_driver.send_keys(payData0['firstName'])

    cardNumber_driver = driver.find_element(By.XPATH, "//input[@id='card_number']")
    cardNumber_driver.send_keys(payData0['cardNumber'])

    card_cvn_driver = driver.find_element(By.XPATH, "//input[@id='card_cvn']")
    card_cvn_driver.send_keys(payData0['cvn'])

    ### 选择卡类型
    addPayDiv_driver = driver.find_element(By.XPATH, "//input[@id='card_type_001']")
    addPayDiv_driver.click()

    ### 选择年月
    month_element = "//select[@id='card_expiry_month']/option[@value='"+payData0['month']+"']"
    year_element = "//select[@id='card_expiry_month']/option[@value='" + payData0['year'] + "']"
    month_driver = driver.find_element(By.XPATH, month_element)
    month_driver.click()
    year_driver = driver.find_element(By.XPATH, year_element)
    year_driver.click()

    ### 确认完成
    Finish_driver = driver.find_element(By.XPATH,"//input[@value='Finish']")
    Finish_driver.click()

    sleep(5)

    ## 关闭界面
    payClose_driver = driver.find_element(By.XPATH,"//div[@id='ps-error-close-button']/span[text()='Close']")
    payClose_driver.click()

    # 确认协议
    sterm_driver = driver.find_element(By.XPATH, "//label[@class='rw-checkbox']/div[@class='checkmark']")
    sterm_driver.click()

    sleep(10)
    # 开始试用
    start_driver = driver.find_element(By.XPATH, "//button[text()='开始我的免费试用']")
    start_driver.click()





