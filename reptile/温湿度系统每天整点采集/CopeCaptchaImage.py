import datetime
import logging
import os.path
import sys

from PIL import Image
import random  # 导入 random(随机数) 模块
import pytesseract  # 导入识别验证码信息包
import time
from selenium.webdriver.common.by import By
import yaml


# 截图，裁剪图片并返回验证码图片名称
# _save_url  ；
# yuansu
def image_cj(driver, _save_url, yuansu):
    """
    :param driver: 浏览器对象
    :param _save_url: 保存路径
    :param yuansu: 验证码元素XPATH
    :return:
    """
    try:
        _file_name = random.randint(0, 100000)
        _file_name_wz = str(_file_name) + '.png'
        _file_url = _save_url + _file_name_wz
        driver.get_screenshot_as_file(_file_url)  # get_screenshot_as_file截屏
        captchaElem = driver.find_element(By.XPATH, yuansu)  ## 获取指定元素（验证码）
        # 因为验证码在没有缩放，直接取验证码图片的绝对坐标;这个坐标是相对于它所属的div的，而不是整个可视区域
        # location_once_scrolled_into_view 拿到的是相对于可视区域的坐标  ;  location 拿到的是相对整个html页面的坐标
        captchaX = int(captchaElem.location['x'])
        captchaY = int(captchaElem.location['y'])
        # 获取验证码宽高
        captchaWidth = captchaElem.size['width']
        captchaHeight = captchaElem.size['height']

        captchaRight = captchaX + captchaWidth
        captchaBottom = captchaY + captchaHeight

        imgObject = Image.open(_file_url)  # 获得截屏的图片
        imgCaptcha = imgObject.crop((captchaX, captchaY, captchaRight, captchaBottom))  # 裁剪
        yanzhengma_file_name = str(_file_name) + 'Captcha.png'
        imgCaptcha.save(_save_url + yanzhengma_file_name)
        os.remove(_file_url)  # 删除整个截图文件
        return yanzhengma_file_name
    except Exception as e:
        print('错误 ：', e)


# 获取验证码图片中信息（保存地址，要识别的图片名称）
def image_text(_save_url, yanzhengma_file_name):
#   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
    image = Image.open(_save_url + yanzhengma_file_name)
    image = binarization(image)  # 二值化处理
    image = cut_noise(image)  # 噪点处理

    text = pytesseract.image_to_string(image, lang='eng')
    try:
        os.remove(_save_url + yanzhengma_file_name)
        # os.rename(_save_url + yanzhengma_file_name, _save_url + "trainingLibrary/" + yanzhengma_file_name)  # 保存验证码
    except Exception:
        pass

    # 去除特殊字符
    exclude_char_list = ' .:\\|\'\"?![],()~@#$%^&*_+-={};<>/¥'
    text = ''.join([x for x in text if x not in exclude_char_list])
    print("验证码图片：" + str(text))
    return text


# 截图并写入验证码（保存地址，验证码元素，验证码输入框元素）
def jietu_xieru(driver, _save_url, yuansu, yanzhma_text):
    # 截图当前屏幕，并裁剪出验证码保存为:_file_name副本.png，并返回名称
    yanzhengma_file_name = image_cj(driver, _save_url, yuansu)  ##对页面进行截图，弹出框宽高（因为是固定大小，暂时直接写死了）
    # 获得验证码图片中的内容
    text = image_text(_save_url, yanzhengma_file_name)
    # 写入验证码
    driver.find_element_by_id('verfieldUserText').send_keys(text)
    time.sleep(2)


# 二值化处理图片
def binarization(image):
    image1 = image.convert('L')  # 转化为灰度图

    threshold = 125  # 设定的二值化阈值
    table = []  # table是设定的一个表，下面的for循环可以理解为一个规则，小于阈值的，就设定为0，大于阈值的，就设定为1
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)

    image1 = image1.point(table, '1')  # 对灰度图进行二值化处理，按照table的规则（也就是上面的for循环）
    return image1


# 去除噪点
def cut_noise(image):
    rows, cols = image.size  # 图片的宽度和高度
    change_pos = []  # 记录噪声点位置

    # 遍历图片中的每个点，除掉边缘
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            # pixel_set用来记录该店附近的黑色像素的数量
            pixel_set = []
            # 取该点的邻域为以该点为中心的九宫格
            for m in range(i - 1, i + 2):
                for n in range(j - 1, j + 2):
                    if image.getpixel((m, n)) != 1:  # 1为白色,0位黑色
                        pixel_set.append(image.getpixel((m, n)))

            # 如果该位置的九宫内的黑色数量小于等于4，则判断为噪声
            if len(pixel_set) <= 4:
                change_pos.append((i, j))

    # 对相应位置进行像素修改，将噪声处的像素置为1（白色）
    for pos in change_pos:
        image.putpixel(pos, 1)

    return image  # 返回修改后的图片


# 以给定time.time()时间戳为基准，后退 day 天得到对应的时间戳
def getBeforeDay(current_timestamp, day):
    '''
    以给定time.time()时间戳为基准，后退 day 天得到对应的时间戳
    @:param current_timestamp: 必须为 time.time()
    @:return: 返回秒级时间戳
    '''
    # 获取当前时间的时间戳，单位为秒

    # 将时间戳转换为毫秒

    # 将毫秒时间戳转换为datetime对象
    current_datetime = datetime.datetime.fromtimestamp(current_timestamp)

    # 创建一个时间间隔对象，表示30天的时间间隔
    delta = datetime.timedelta(days=day)

    # 倒退30天后的时间
    previous_datetime = current_datetime - delta

    # 将倒退30天后的时间转换为时间戳，格式：1703574459.706492
    previous_timestamp = previous_datetime.timestamp()

    return previous_timestamp


# 读取yml文件
def readYml(fileName):
    BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
    with open(os.path.join(BASE_DIR, ('utils/' + fileName)), 'r', encoding='utf-8') as fp:
        data = yaml.load(fp.read(), Loader=yaml.FullLoader)

    return data


class MyLogging:

    def __init__(self):
        timestr = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        filename = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), 'logs/'+str(timestr)+'.log')   # 日志文件的地址

        # print(filename)
        self.logger = logging.getLogger()  # 定义对应的程序模块名name，默认为root
        self.logger.setLevel(logging.INFO)  # 必须设置，这里如果不显示设置，默认过滤掉warning之前的所有级别的信息
        # 设置格式对象
        formatter = logging.Formatter(
            "%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s - %(message)s")  # 定义日志输出格式

        sh = logging.StreamHandler()  # 日志输出到屏幕控制台
        sh.setLevel(logging.INFO)  # 设置日志等级
        sh.setFormatter(formatter)  # 设置handler的格式对象

        fh = logging.FileHandler(filename=filename)  # 向文件filename输出日志信息
        fh.setLevel(logging.INFO)  # 设置日志等级
        fh.setFormatter(formatter)  # 设置handler的格式对象

        # 将handler增加到logger中
        self.logger.addHandler(sh)
