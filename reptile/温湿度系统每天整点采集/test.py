import datetime
import os
import sys
import time
from collections import defaultdict

import cv2
import pymysql
import pytesseract  # 导入识别验证码信息包
from PIL import Image
import numpy as np

# def erode_dilate(im, threshold=2):
#     im = cv2.imread('xxx.jpg', 0)
#     cv2.imshow('xxx.jpg', im)
#
#     # (threshold, threshold) 腐蚀矩阵大小
#     kernel = np.ones((threshold, threshold), np.uint8)
#     # 膨胀
#     erosion = cv2.erode(im, kernel, iterations=1)
#     cv2.imwrite('imgCode_erosion.jpg', erosion)
#     Image.open('imgCode_erosion.jpg').show()
#     # # 腐蚀
#     eroded = cv2.dilate(erosion, kernel, iterations=1)
#     cv2.imwrite('imgCode_eroded.jpg', eroded)
#     Image.open('imgCode_eroded.jpg').show()
import CopeCaptchaImage


def getBeforeDay(current_timestamp):
    '''
    以给定时间戳为基准，后退 days 天得到对应的时间戳
    '''
    # 获取当前时间的时间戳，单位为秒

    # 将时间戳转换为毫秒

    # 将毫秒时间戳转换为datetime对象
    current_datetime = datetime.datetime.fromtimestamp(current_timestamp)

    # 创建一个时间间隔对象，表示30天的时间间隔
    delta = datetime.timedelta(days=30)

    # 倒退30天后的时间
    previous_datetime = current_datetime - delta

    # 将倒退30天后的时间转换为时间戳，格式：1703574459.706492
    previous_timestamp = previous_datetime.timestamp()

    return previous_timestamp


# 二值化处理
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


if __name__ == '__main__':
    # dateList = ['1703601977',
    #             '1703603275',
    #             '1703604242',
    #             '1703604357',
    #             '1703605577',
    #             '1703606875',
    #             '1703607842',
    #             '1703607957', #
    #             '1703609177',
    #             '1703610475',
    #             '1703611442',
    #             '1703611557',   #
    #             '1703611958',
    #             '1703614075',
    #             '1703615042',
    #             '1703615157']
    # 1703691158 2509-11-17 19:26:20

    # for i in range(len(dateList)-1,-1,-1):
    #     if dateList[i] == '1703607957':
    #         dateList.pop(i)
    #     if dateList[i] == '1703611557':
    #         dateList.pop(i)

    mysql_config = CopeCaptchaImage.readYml("config.yml")['mysql']
    mysql_config['cursorclass'] = pymysql.cursors.DictCursor
    conn = pymysql.connect(**mysql_config)
    cursor = conn.cursor()
    select_sql = "select * from temperatureTest where device_number='24251128' and device_temperature='25.0' and device_humidity='0' and create_time=1;"
    cursor.execute(select_sql)
    print(len(cursor.fetchall()))
    cursor.close()
    conn.close()

    # path = r"C:\Users\Administrator\Documents\Code\Python_project\reptile\温湿度系统每天整点采集\trainingLibrary"
    # path2 = r"C:\Users\Administrator\Documents\Code\Python_project\reptile\温湿度系统每天整点采集\trainingLibrary2"
    # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
    # for i in os.listdir(path):
    #     image = Image.open(os.path.join(path, i))
    #     image = binarization(image)  # 二值化处理
    #     image = cut_noise(image)  # 噪点处理
    #     # image.save(os.path.join(path2, i.replace('.png', '.tif')), quality=95)
    #     image.save(os.path.join(path2, i), quality=95)
