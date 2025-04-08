import hashlib
import logging
import time


def 获取签名(app_id, app_secret, timestamp):
    params = f"appId={app_id}&appSecret={app_secret}&timeStamp={timestamp}"

    hl = hashlib.md5()
    hl.update(params.encode(encoding='utf-8'))
    return hl.hexdigest().upper()

def 创建日志(fileName):
    # logging.basicConfig(level=logging.INFO,
    #                              format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    #                              datefmt='%Y-%m-%d %H:%M:%S',
    #                              filename= fileName,  # 日志文件
    #                              filemode='a')  # 追加模式
    logger = logging.getLogger('spider')

    logger.setLevel(logging.DEBUG)

    # 输出到文件
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler(fileName, encoding='utf-8')
    file_handler.setFormatter(formatter)

    # 输出到控制台
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # 添加处理器到日志器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# def 获取签名(app_id, app_secret, timestamp):
#
#     sign = get_sign(app_id, app_secret, str(timestamp))
#     print(sign)
#     return sign