import json
import time

import requests


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
    url = 'https://oapi.dingtalk.com/robot/send?access_token=684d6cb7bc2cca28d8637656dbed6f0e67f4e3811b3a2b4dc5de3c2de0c1e37e'

    给钉钉推送消息(url, '闲鱼发货', '发货')