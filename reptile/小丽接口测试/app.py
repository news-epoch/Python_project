import json
import time

import requests

from reptile.小丽接口测试 import tools
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
if __name__ == '__main__':
    corpId = "1748837"
    appId = "124496550402457600"
    appSecret = "slfLDWAMD2sI4PEsNG5"
    timestamp = int(round(time.time() * 1000))
    sign = tools.获取签名(appId,appSecret, timestamp)
    headers = {
        "Content-Type": "application/json",
        "X-Ec-Cid": corpId,
        "X-Ec-Sign": sign,
        "X-Ec-TimeStamp": str(timestamp)
    }
    response = requests.session().get(url="https://open.workec.com/v2/config/getPubicPond", headers=headers, verify=False)
    if response.status_code == requests.codes.ok:
        # print(response.json())
        print(json.dumps(response.json(), ensure_ascii=False))
        print(response.json()['data'][0]['publicPondId'])