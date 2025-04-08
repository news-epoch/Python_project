import json
import logging
import uuid

import requests
from requests_toolbelt import MultipartEncoder


class SanMaoAPIs:
    def PlaceOrder(self, product_id: str=None, phone: str=None):
        placeOrderUrl = 'http://sm.cykjwl.top/inside/uploadOrderRg'
        boundary = "------WebKitFormBoundary" + str(uuid.uuid1())
        headers = {
            "cookie": "frontUserInfo=7001b7d8b5cb3e94b3a91a7cf45b5351578b61f4841f09d08593fa4c622ad9c97b0992da2f03f50b31f296f32e819065c0b9d0397b8f3b9975388f4935255258b415953ee5631981430da5e48bf5b3a60190928a949df1ea0c58cb1d32386347a37c6b53188bd906fbf69c6a26f9e93db554f6399681ec01103379acae2640c6f404f03b8bca85c5849bfb1c3086c8f085384c277f93cba7819376883562cb84fc88db2a6e782277c8633e5630bb358e43193e42b221ab36288903ead2b46ffc92c2c1ac35b67793e411b55113aab73e97fef8791c203c8cc92d6cc887dcc35d9ac9e31eb90e94d5685fd85cc8ffc27e1297c8fb34b463b6a0b80d13b0176075ac8bfd5ed8892c4a13b6a9ecbe7dc503af35e10ede17874e71756f6e8b665a69124dd4b00f8923dbc005e7fd18c61f8149928de270b71bbd7fe262da526f590bf75acb03f70f0446d7c99c24b27f4a64a72d02b8b5a5532e7de948cce3a4198c0d466efcd5906529c007591f76f6a367605196110e5472f1308425b878bf5b8d4096a477b3b5224bde9878cfd3172f5cb16daeea64d831014a9393e6cfd66247a0bf22d3f7af5f31802c60c11af64ced636244e79178cba36a8e7c614d18a7aff6bcc39ae50a91e87c48eaf618803fce8d0fc47f86dd4844e64d897aea219b48e8eb897d9b2426b1bdce35ca98e8aaa5a9aa908012106ed981c4711fccaff9fc81c29cf90c36e8fe18e4f49763c2898324d5adc9b295652ed3eeabed333ba0a1708e9aa68f67aedda45152851cb9d78a76a2e910841f77be84e4e73b525eb40b7c717cb78c7d52d9f7a574b5598a024f9ca88edf94fce23bcbaac91bbf234583fdb664b92a3422c157fd97ffd30c7a2d104339b38f33b62177e6e39f4c48bb8af4e2676019c0f8c91f2d42f5fb887c5f5b5f2c431a2c58b4ea53b9ff7c3f255ec4aaf79dc47825ddc9c1702ea50da5981d3e8957c5d457e31d7e060d74ec768e65b9b8d1789634adf3fbbb0db5032f178cedd9b234485464a735de8895c660e466474cbe45b8c074306292cee4d63051d43e18d0be47a33be0ea7d2c8b33ddb32af5996223df4c86be8cb5842f76c7b88d10d063bbed759e",
            "accept": "application/json, text/plain, */*",
            "authorization": "1f5f792471d648a0cd1c2d8791f124de",
            "host": "sm.cykjwl.top",
            "content-type": f"multipart/form-data; boundary={boundary}"
        }
        fields = {
            'goodsId': f'{product_id}',   # 购买商品编码
            'sumprice': '1',   # 商品数量
            'paytype': '0',
            'payId': '0',
            "thisrate": '0',
            "thisratemin": '0',
            "thisratetop": '0',
            'iswho': 1,
        }
        if phone is not None:
            fields['textAccountName'] = phone # 输入手机号
        encoder = MultipartEncoder(fields=fields, boundary=boundary)

        response = requests.post(url=placeOrderUrl, headers=headers,  data=encoder, verify=False)
        if response.status_code == requests.codes.ok:
            logging.info(json.dumps(response.json(), ensure_ascii=False))
# select xpi.xianyu_product_name,xpi.sanmao_product_id,spi.sale_price ,dti.device_type_name
# from xianyu_product_info xpi
# 	left join sanmao_product_info spi on xpi.sanmao_product_id=spi.id
# 	LEFT JOIN device_type_info dti on xpi.dev_type_code=dti.id;
if __name__ == '__main__':
    productName = "优酷"
    device_id = "安卓手机"
    sanMaoAPIs = SanMaoAPIs()
    data = [
        {"productName": "芒果", "deviceId": "安卓手机", "productId": "5067"},
        {"productName": "芒果", "deviceId": "安卓平板", "productId": "286"},
        {"productName": "芒果", "deviceId": "苹果平板", "productId": "286"},
        {"productName": "芒果", "deviceId": "普通电脑", "productId": "287"},
        {"productName": "优酷", "deviceId": "安卓手机", "productId": "3422"},
        {"productName": "优酷", "deviceId": "苹果手机", "productId": "3422"},
        {"productName": "优酷", "deviceId": "安卓平板", "productId": "3485"},
        {"productName": "优酷", "deviceId": "苹果平板", "productId": "3485"},
    ]
    for i in data:
        if i['productName'] == productName and i['deviceId'] == device_id:
            sanMaoAPIs.PlaceOrder(i['productId'])