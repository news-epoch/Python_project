import logging
import os, sys, yaml
import time

import pytesseract
import pywinauto
import pywinauto.keyboard
import requests
from PIL import Image, ImageEnhance
from pywinauto import Desktop, Application
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import easytrader
from easytrader import refresh_strategies

logger = logging.getLogger('spider')
logger.setLevel(logging.INFO)
# 输出到文件
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('app.log', encoding='utf-8')
file_handler.setFormatter(formatter)
# 输出到控制台
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
# 添加处理器到日志器
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def 识别验证码(file_path):
    pytesseract.pytesseract.tesseract_cmd = r'D:\software\Tesseract-OCR\tesseract.exe'
    # file_path = [r'C:\Users\work_epoch\Pictures\test03.png', r'C:\Users\work_epoch\Pictures\test02.png', r'C:\Users\work_epoch\Pictures\test04.png']

    image = Image.open(file_path)
    # 增强对比度（提升识别率）. 在将图片灰度转换，二值化
    img = image.convert('L')
    pixels = img.load()
    for x in range(img.width):
        for y in range(img.height):
            if pixels[x, y] > 205:
                pixels[x, y] = 255
            else:
                pixels[x, y] = 0
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)  # 对比度翻倍
    text = pytesseract.image_to_string(image,
                                       config=r'--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')

    return text
    # print("识别结果:", text.strip())


def 判断验证码控件是否存在():
    app = Application(backend="uia").connect(title="网上股票交易系统5.0")
    main_win = app.window(title="网上股票交易系统5.0", control_type="Window")
    time.sleep(1)
    while True:
        time.sleep(1)
        if main_win.window(class_name='#32770', title="").exists(timeout=1):
            captcha_main = main_win.window(class_name='#32770', title="")
            if (
                    captcha_main.window(control_id=0x959, control_type="Image",title="检测到您正在拷贝数据，为保护您的账号数据安全，请").exists(timeout=1)
                    or captcha_main.window(control_id=0x964, class_name="Edit").exists(timeout=1)
                    or captcha_main.window(control_id=0x965, class_name="Static").exists(timeout=1)
            ):
                logger.info("==========识别到需要输入验证码，正在处理==========>")
                file_path = r"tmp.png"

                captcha_main.window(
                    control_id=0x965, class_name="Static"
                ).capture_as_image().save(
                    file_path
                )  # 保存验证码
                captcha_num = 识别验证码(file_path).strip()  # 识别验证码
                captcha_num = "".join(captcha_num.split())
                # print("验证码识别结果-->" + captcha_num)
                if len(captcha_num) == 4:
                    logger.info("输入验证码-->" + captcha_num)
                    app.set_focus()
                    captcha_main.window(control_id=0x964, class_name="Edit").click_input()
                    captcha_main.window(control_id=0x964, class_name="Edit").type_keys(captcha_num)  # 模拟输入验证码
                    time.sleep(1)
                    captcha_main.window(control_id=0x964, class_name="Edit").click_input()
                    captcha_main.window(control_id=0x964, class_name="Edit").type_keys("^a{ENTER}")
                    # pywinauto.keyboard.send_keys("{ENTER}")  # 模拟发送enter，点击确定
                    try:
                        logger.info("判断窗体是否消失，或者验证码是否错误")
                        if app.window(control_id=0x966, class_name="Static").window_text() == '验证码错误!!' or app.window(class_name='#32770', title="").exists(timeout=1) or captcha_main.window(control_id=0x964, class_name="Edit").exists(timeout=1):
                            captcha_main.window(control_id=0x964, class_name="Edit").click_input()
                            captcha_main.window(control_id=0x964, class_name="Edit").type_keys("^a{DELETE}")
                            captcha_main.window(control_id=0x964, class_name="Edit").set_text("")
                        else:
                            logger.info("验证码对话框消失")
                            continue
                    except Exception as ex:  # 窗体消失
                        logger.error("验证码对话框消失")
                        break
                    logger.info("刷新验证码")
                    captcha_main.window(control_id=0x965, class_name="Static", visible_only=True).click_input()
            else:
                break
        else:
            break

def 读取配置文件():
    path = 获取本地绝对路径()
    with open(os.path.join(path, 'config/application.yml'), 'r', encoding='utf-8') as fp:
        file_content = fp.read()
        return yaml.load(file_content, yaml.FullLoader)


def 获取本地绝对路径():
    ### 获取这个文件的目录的绝对路径
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def 转换数据格式(df)->dict:
    data_map = dict()
    for i in df.index.values:
        data_map[str(df.loc[i]['委托序号'])] = df.loc[i].to_dict()
    return data_map


def 创建数据库连接并且返回操作字段(url='sqlite:///sqlite/scene.db'):
    engine = create_engine(url, echo=False)

    return sessionmaker(bind=engine)()


def 同花顺刷新():
    app = Application(backend="uia").connect(title="网上股票交易系统5.0")
    main_win = app.window(title="网上股票交易系统5.0", control_type="Window")
    if main_win.window(class_name='ToolbarWindow32', title="").exists(timeout=1):
        toolbar = main_win.window(class_name='ToolbarWindow32', title="")
        toolbar.window(title=" 刷新当前页面 ").click_input()




def 给钉钉推送消息(url, title, message):
    header = {
        "Content-Type": "application/json;charset=UTF-8"
    }
    message_body = {
        "msgtype": "markdown",
        "markdown": {
            "title": title,
            "text": message
        },
        "at": {
            "atMobiles": [],
            "isAtAll": False
        }
    }
    # send_data = json.dumps(message_body)  # 将字典类型数据转化为json格式
    for i in range(0, 3):
        try:
            ChatBot = requests.post(url=url, json=message_body, headers=header, verify=False)

            opener = ChatBot.json()
            if opener["errmsg"] == "ok":
                print(u"%s 通知消息发送成功！" % opener)
                break
            else:
                print(u"通知消息发送失败，原因：{}<br>等待10s再次发送".format(opener))
                time.sleep(10)
        except Exception as e:
            print(f"通知消息发送失败，原因：{e}<br>等待10s再次发送")
            time.sleep(10)


if __name__ == '__main__':
    pass
    # 定位控件()
    # 识别验证码(r'C:\Users\work_epoch\Pictures\test03.png')
    # 判断验证码控件是否存在()

