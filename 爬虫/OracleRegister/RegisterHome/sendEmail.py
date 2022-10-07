from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.chrome.service import Service
# 实现填写基础信息，发送邮件信息
if __name__ == '__main__':
    # 创建输入字典
    dict_list = {
        'lastName': 'epoch',
        'firstName': 'news',
        'country': '中国',
        'email': 'newsepoch@163.com'
    }
    #创建浏览器对象
    chromebro = webdriver.Chrome(service=Service(executable_path="../utils/chromedriver.exe"))
    #浏览器自动前往网址
    chromebro.get('https://www.oracle.com/cn/cloud/free/?source=:ow:o:p:nav:081520OCIHeroCallout_cn&intcmp=:ow:o:p:nav:081520OCIHeroCallout_cn')
    #跳转到注册界面
    search_register_page = chromebro.find_element(By.XPATH,"//div[@class='rh03col1']/div[@class='obttns']/div/a[text()='开始免费试用']")
    search_register_page.click()
    sleep(5)
    #定位名字文本标签
    search_input_lastName = chromebro.find_element(By.XPATH,"//input[@label='名字']")
    search_input_lastName.send_keys(dict_list.get('lastName'))
    #定位姓氏标签
    search_input_firstName = chromebro.find_element(By.XPATH, "//input[@label='姓氏']")
    search_input_firstName.send_keys(dict_list.get('firstName'))
    # 定位姓氏标签
    search_input_email = chromebro.find_element(By.XPATH, "//input[@label='电子邮件']")
    search_input_email.send_keys(dict_list.get('email'))
    # 点击国家地区并选择
    # js = "document.querySelector('#main > div > div.col-md-8.col-xs-12.mainContainer > div > div > div.upperContentContainer > form > fieldset > div:nth-child(2) > label > div > div').click()"
    # chromebro.execute_script(js)
    # ## 设置所有属性可见
    # js2 = "document.querySelectorAll('div')[0].style.display = 'block':"
    # chromebro.execute_script(js2)
    # js3 = "document.getElementsByClassName('.css-26l3qy-menu').style.display = 'block'"
    # chromebro.execute_script(js3)
    ## 获取值
    search_div_contry = chromebro.find_element(By.XPATH,"//div[text()='国家/地区']")
    search_div_contry.click()
    search_input_contry = chromebro.find_element(By.XPATH,"//input[@id='react-select-2-input']")
    search_input_contry.send_keys(dict_list.get('country'))
    search_input_contry.send_keys(Keys.ENTER)
    ## 验证
    search_div_identify = chromebro.find_element(By.XPATH,"//iframe[@title='widget containing checkbox for hCaptcha security challenge']")
    search_div_identify.click()
    print("等待50s")
    sleep(50)
    ### 进入frame
    print("正在进入iframe标签中")
    iframe_elemnt = chromebro.find_element(By.XPATH,"//iframe[@title='Main content of the hCaptcha challenge']")
    chromebro.switch_to.frame(iframe_elemnt)

    image_element = "//div[@class='task-grid']/div[@class='task-image']//div[@class='icon/@style']"
    search_div_identifyPhotoStyle = chromebro.find_element(By.XPATH, image_element)
    print(search_div_identifyPhotoStyle.text)
    # search_div_identifyPhotoStyle = chromebro.find_element(By.XPATH,"///div[@class='task-grid']/div[@class='task-image']//div[@class='icon']/@style")
    # with open("phtot_base64_list.txt",'w',encoding="utf-8") as fp:
    #     fp.write(search_div_identifyPhotoStyle)



    # 推出
    #chromebro.quit()
