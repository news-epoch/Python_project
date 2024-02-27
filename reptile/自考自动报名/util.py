import os
import pytesseract
from PIL import Image

def image_text(_save_url, yanzhengma_file_name):
    """
    :param _save_url:   保存地址   /a/v/c/d/
    :param yanzhengma_file_name:   图片名称  cade.png
    :return:
    """
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
    image = Image.open(_save_url + yanzhengma_file_name)
    image = binarization(image)  # 二值化处理
    image = cut_noise(image)  # 噪点处理

    text = pytesseract.image_to_string(image, lang='eng')
    try:
        os.remove(_save_url + yanzhengma_file_name)
    except Exception:
        pass

    # 去除特殊字符
    exclude_char_list = ' .:\\|\'\"?![],()~@#$%^&*_+-={};<>/¥'
    text = ''.join([x for x in text if x not in exclude_char_list])
    print("验证码图片：" + str(text))
    return text

def binarization(image):
    """
    灰度处理+二值化
    :param image: PLI.Image
    :return:
    """
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


def cut_noise(image):
    """
    去除噪点
    :param image: PLI.Image
    :return:
    """
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


def chinaConvetEnglish(character):
    if str(character).__contains__("成都"):
        character = 'cd'
    elif str(character).__contains__("自贡"):
        character = 'zg'
    elif str(character).__contains__("乐山"):
        character = 'ls'
    elif str(character).__contains__("攀枝花"):
        character = 'pzh'
    elif str(character).__contains__("泸州"):
        character = 'lz'
    elif str(character).__contains__("德阳"):
        character = 'dy'
    elif str(character).__contains__("绵阳"):
        character = 'my'
    elif str(character).__contains__("广元"):
        character = 'gy'
    elif str(character).__contains__("遂宁"):
        character = 'sn'
    elif str(character).__contains__("内江"):
        character = 'nj'
    elif str(character).__contains__("南充"):
        character = 'nc'
    elif str(character).__contains__("宜宾"):
        character = 'yb'
    elif str(character).__contains__("广安"):
        character = 'ga'
    elif str(character).__contains__("达州"):
        character = 'dz'
    elif str(character).__contains__("雅安"):
        character = 'ya'
    elif str(character).__contains__("阿坝"):
        character = 'abz'
    elif str(character).__contains__("甘孜"):
        character = 'gz'
    elif str(character).__contains__("凉山"):
        character = 'lcharacter'
    elif str(character).__contains__("巴中"):
        character = 'bz'
    elif str(character).__contains__("眉山"):
        character = 'ms'
    elif str(character).__contains__("资阳"):
        character = 'zy'

    return str(character)