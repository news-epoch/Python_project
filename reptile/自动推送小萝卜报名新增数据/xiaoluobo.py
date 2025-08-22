import datetime
import json
import logging
import time

import pymysql
import requests
import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import QQEmail
import dingding_utils
from orm import XiaoluoboInfo
import traceback
pymysql.install_as_MySQLdb()


# def 创建日志(fileName):
    # logging.basicConfig(level=logging.INFO,
    #                              format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    #                              datefmt='%Y-%m-%d %H:%M:%S',
    #                              filename= fileName,  # 日志文件
    #                              filemode='a')  # 追加模式
logger = logging.getLogger('spider')

logger.setLevel(logging.DEBUG)

# 输出到文件
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('app.log', encoding='utf-8')
file_handler.setFormatter(formatter)

# 输出到控制台
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# 添加处理器到日志器
logger.addHandler(file_handler)
logger.addHandler(console_handler)

    # return logger

def applicationYml():
    with open('./conf/application.yaml', 'r', encoding='utf-8') as f:
        result = yaml.load(f.read(), Loader=yaml.FullLoader)
    return result

def getXiaoLuoBoData(xLCSign, xLCSession, xLCId):
    now = datetime.datetime.now()
    old = now - datetime.timedelta(days=7)
    url = 'https://api.xiaobaoming.com/1.1/classes/Kevent'
    params = {
        "where": json.dumps({
            "isDeleted": 0,
            "expiredAt": {
                "$gt": {
                    "__type": "Date",
                    "iso": str(now.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
                }
            },
            "createdAt": {
                "$gt": {
                    "__type": "Date",
                    "iso": str(old.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
                }
            },
            "risky": {
                "$ne": True
            },
            "isLBS": True,
            "locLongitude": {
                "$lt": 105.15801239013672,
                "$gt": 103.15801239013672
            },
            "locLatitude": {
                "$lt": 32.824039459228516,
                "$gt": 28.824039459228516
            },
            "status": {
                "$nin": [
                    "CANCEL",
                    "TO_BE_CANCELLED",
                    "INIT",
                    "SUCCESS"
                ]
            },
            "distribType": {
                "$nin": [
                    "TEMPLETE",
                    "templete"
                ]
            },
            "isPublicEvent": True
        }),
        "include": "user,targetOrg",
        "limit": 500,
        "order": "-attendCount"
    }
    headers = {
        "X-LC-Sign": xLCSign,
        "X-LC-Session": xLCSession,
        # Referer: https://servicewechat.com/wx7ce5b8ce4b97b06b/1920/page-frame.html
        "X-LC-Id": xLCId
        # Host: api.xiaobaoming.com
    }
    response = None
    for i in range(1,10):
        try:
            response = requests.session().get(url=url, params=params, headers=headers, verify=False)
            break
        except Exception as e:
            print(e)
            time.sleep(10)
    data = []
    if response.status_code == requests.codes.ok and response.json() != '' and isinstance(response.json(), dict):
        print("数据正常")
        for result in response.json()['results']:
            try:
                data.append({
                    'id': result['objectId'],  # 唯一id
                    "title": result['title'],  # 标题
                    # "description": result['description'],     # 描述
                    "locationAddress": result.get('locationAddress'),  # 实际地址
                    "locationName": result['locationName'],  # 地址名
                    "count": int(result['count']),  # 可报名最大数
                    "attendCount": int(result['attendCount']),  # 当前报名数
                    # "createdAt": result['createdAt'],
                    # "endAt": result['expiredAt']['iso']
                    "createdAt": datetime.datetime.strptime(str(result['createdAt']), '%Y-%m-%dT%H:%M:%S.%fZ').strftime("%Y-%m-%d %H:%M:%S"),  # 任务创建时间
                    "endAt": datetime.datetime.strptime(result['expiredAt']['iso'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime("%Y-%m-%d %H:%M:%S"),  # 任务结束时间
                    'priceItems': json.dumps(result.get('additionalItems'), ensure_ascii=False),   # 价格
                    'targetOrgName': result.get('user').get('nickName') if result.get('targetOrg') == None else result.get('targetOrg').get('name')
                })
            except Exception as e:
                logging.error(f"解析json格式出现异常：{e}")

                logging.error(f"异常所在行数{traceback.format_exc()}")
                logging.error(json.dumps(result, ensure_ascii=False))
    return data


def save(url, headers):
    engine = create_engine(url=url,
                           echo=True,
                           pool_size=8,
                           )
    DbSession = sessionmaker(bind=engine)
    session = DbSession()
    saveData = list()
    data = getXiaoLuoBoData(headers.get('X-LC-Sign'), headers.get('X-LC-Session'), headers.get('X-LC-Id'))
    for i in data:
        print(i)
        xiaoluoboInfo = XiaoluoboInfo(id=i['id'], title=i['title'], locationName=i['locationName'],
                                      attendCount=i['attendCount'],
                                      count=i['count'], createdAt=i['createdAt']
                                      , endAt=i['endAt'], locationAddress=i['locationAddress'], priceItems=i.get('priceItems'), targetOrgName=i.get('targetOrgName'))
        # session.query(XiaoluoboInfo).filter(and_(XiaoluoboInfo.title == xiaoluoboInfo.title,
        #                                          XiaoluoboInfo.locationName == xiaoluoboInfo.locationName,
        #                                          XiaoluoboInfo.locationAddress == xiaoluoboInfo.locationAddress,
        #                                          XiaoluoboInfo.createdAt == xiaoluoboInfo.createdAt,
        #                                          XiaoluoboInfo.endAt == xiaoluoboInfo.endAt)).count() != 0
        if session.query(XiaoluoboInfo).filter(XiaoluoboInfo.id == xiaoluoboInfo.id).count() != 0:
            continue
        else:
            saveData.append(xiaoluoboInfo.to_dict())
            session.add(xiaoluoboInfo)
            session.commit()
    session.close()
    return saveData


def sendEmail():
    logger.info(f"=================当前运行开始时间{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}=====================")
    application = applicationYml()
    new_activity_list = None
    qq_email_client = None
    for i in range(1,10):
        try:
            new_activity_list = save(application.get('mysql').get('url'), application.get('headers'))
            qq_email_client = QQEmail.MailClient(host=application.get('email').get('sendHost'), user=application.get('email').get('sendEmail'), pwd=application.get('email').get('sendPass'))
            break
        except Exception as e:
            logger.info(f"获取数据异常：{e}")
            logging.info(f"异常所在行数：{traceback.format_exc()}")
    # print(new_activity_list)
    if len(new_activity_list) != 0:
        message = ''
        logger.info("构建准备数据----------->")
        for activity in new_activity_list:
            logger.info(activity)
            prices = ''
            if len(json.loads(activity.get('priceItems'))) != 0:
                for i in json.loads(activity.get('priceItems')):
                    # print(i)
                    price = f'&nbsp;&nbsp;&nbsp;&nbsp;选项名：{str(i.get("name"))}<br>&nbsp;&nbsp;&nbsp;&nbsp;价格：{str(i.get("price"))}<br>&nbsp;&nbsp;&nbsp;&nbsp;--<br>'
                    prices += price
            msg = f"id：{activity.get('id')}<br>标题：{activity.get('title')}<br>地址：{activity.get('locationName')}<br>当前报名数：{activity.get('attendCount')}/{activity.get('count')}<br>创建时间：{activity.get('createdAt')}<br>结束时间：{activity.get('endAt')}<br>发起人：{activity.get('targetOrgName')}<br>详细地址：{activity.get('locationAddress')}<br>价格表：<br>{prices}<br><br>-------------<br><br>"
            dingding_utils.给钉钉推送消息(application.get('dingding').get('url'), '小萝卜活动数据新增', msg)
            if msg.__contains__('免费') or msg.__contains__('放鸽费'):
                try:
                    qq_email_client.send(application.get('email').get('acceptEmail'), '小萝卜活动数据新增', msg)
                except Exception as e:
                    logger.info(f"消息发送异常：{e}")
            message += msg
        logger.info(message)
    logger.info(f"=================当前运行结束时间{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}=====================\n\n")


if __name__ == '__main__':
    # 测试消息请求
    application = applicationYml()
    headers = application.get('headers')
    print(len(getXiaoLuoBoData(headers.get('X-LC-Sign'), headers.get('X-LC-Session'), headers.get('X-LC-Id'))))