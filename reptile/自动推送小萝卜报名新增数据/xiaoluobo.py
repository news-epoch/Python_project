import datetime
import json

import pymysql
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from reptile.自动推送小萝卜报名新增数据.orm import XiaoluoboInfo

pymysql.install_as_MySQLdb()

def getXiaoLuoBoData():
    url = 'https://api.xiaobaoming.com/1.1/classes/Kevent'
    params = {
        "where": json.dumps({
            "isDeleted": 0,
            "expiredAt": {
                "$gt": {
                    "__type": "Date",
                    "iso": "2025-02-12T07:13:29.823Z"
                }
            },
            "createdAt": {
                "$gt": {
                    "__type": "Date",
                    "iso": "2025-02-07T06:46:45.703Z"
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
        "limit": 200,
        "order": "-attendCount"
    }
    headers = {
        "X-LC-Sign": "674dee286e3de05bd8965db0958e360c,1739344409823",
        "X-LC-Session": "elkwkwh7fo2cydt0d51s46x9p",
        # Referer: https://servicewechat.com/wx7ce5b8ce4b97b06b/1920/page-frame.html
        "X-LC-Id": "6IkiQ1QmPKMayoS8DKVi7067-gzGzoHsz"
        # Host: api.xiaobaoming.com
    }
    response = requests.session().get(url=url, params=params, headers=headers, verify=False)
    data = []
    for result in response.json()['results']:
        # print(json.dumps(result, ensure_ascii=False))
        data.append({
            'id': result['objectId'],   # 唯一id
            "title": result['title'],     # 标题
            # "description": result['description'],     # 描述
            "locationAddress": result['locationAddress'],    # 实际地址
            "locationName": result['locationName'],    # 地址名
            "count": int(result['count']),               # 可报名最大数
            "attendCount": int(result['attendCount']),   # 当前报名数
            # "createdAt": result['createdAt'],
            # "endAt": result['expiredAt']['iso']
            "createdAt": datetime.datetime.strptime(str(result['createdAt']), '%Y-%m-%dT%H:%M:%S.%fZ').strftime("%Y-%m-%d %H:%M:%S"),       # 任务创建时间
            "endAt": datetime.datetime.strptime(result['expiredAt']['iso'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime("%Y-%m-%d %H:%M:%S")    # 任务结束时间
        })

    print(data)
    return data


def save():
    engine = create_engine("mysql://root:123456@10.0.9.20:33062/scene_iot?charset=utf8",
                           echo=True,
                           pool_size=8,
                           # pool_recycle=60 * 30
                           )
    DbSession = sessionmaker(bind=engine)
    session = DbSession()

    data = getXiaoLuoBoData()
    for i in data:
        user = XiaoluoboInfo(id=i['id'], title=i['title'], locationName=i['locationName'], attendCount=i['attendCount'],
                             count=i['count'], createdAt=i['createdAt']
                             , endAt=i['endAt'], locationAddress=i['locationAddress'])
        session.add(user)
        session.commit()

