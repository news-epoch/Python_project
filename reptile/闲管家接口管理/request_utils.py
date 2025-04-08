import json
import time

import requests


def 获取订单列表():
    url = 'https://api.goofish.pro/api/order/pager'
    params = {
        "time_type": 1,
        "time[]": "2024-12-17",
        "time[]": "2025-03-17",
        "idx": 1,
        "size": 25,
    }
    headers = {

        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9",
        "authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3NDIxNzQ0MDAsIm5iZiI6MTc0MjE3NDQwMCwiZXhwIjoxNzQyNzc5MjAwLCJzaWQiOjk4Mjk2MTM3MDI2NzcxNywidWlkIjo5ODI5NjEzNzAyNjc3MTgsIm5hbWUiOiJcdTVjMGZcdTk2NDhcdTY3NDJcdThkMjdcdTk0ZmFcdTk1ZjJcdTdiYTFcdTViYjYifQ.Pw6L9-frq8T_qDucnMidrtBj-kD4K25W0snDnZKRQZA",
        "origin": "https://goofish.pro",
        "priority": "u=1, i",
        "referer": "https://goofish.pro/sale/order/all",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "x-content-security": "key=key=MKGtWHTm9Zh1Q5ue0sC6draLzB3bUJon;secret=XLkJ83KLDnyTstte5HYsrUpqSbNrQmM5CRgIv/OwzvhUm5F2KowX/CgXhBX4mOAWjk4Q/mRKaV6OBpueP8S3LZZQpiUBaupHl6QlJAeYjUNMxq0lgDCvfHKUoW5Im/lFFZTcYoVHzhxULlb0B3aPAJF+NgxLkzrEyRLZcOnNeJ4=;signature=fDG/4wfJ2lrV77+NJ9yogwBnn9mUM16g6fgdT3asEEg="
    }
    print(requests.session().get(url, params=params, headers=headers, verify=False).json())


def 小程序登录闲鱼():
    url = "https://passport.goofish.com/mini_program/login.do?_bx-m=1"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "*/*",
        "Referer": "https://servicewechat.com/wx9882f2a891880616/40/page-frame.html",
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c11)XWEB/11581',
        "bx-ua": "304$ssFXasNyaE93HFUptyMGJAbvWxiHTqDEc1yh4Bgu6ficR4qHNwVhGDeUu9f0P8eASa4uRQTpCqy5qpuV0LaVhgCoXFdTFYp2QFXR96OgbWl1srIotqGss6G6EqqRhukWL5McLDxKRAh/iQS58F8RmXjWls0YKMRGeAznUoHKynrYxAXMqWW63BuBjcKnT7CpikpOnUaxoGyNbYH0gTCkEQdPf5JLPlBDMZXYr9+hEEwqsP+D7X/PuKY74ZlqK6xFYDsB8DbE/8lw/48iFS6fi0CjeP+RElFExgcU7ipzHjhGaTCQuatcCUt7R+8nRhInoTiUi3ocuj5B2Q05xxm6bX5KCKSOIV/wVq+sE6cRYeoVs3Y+Ufj9QXmM2O/A822rwp1GMXLsU17MzJr3+UPUr83rGwKrjtt+3VBqZrtJcQqYzr8+BNlgZpngEEHIU2A+yU53q/CkLGxUccHICXOyAqrH6jOEDat3FQz580jBYaWGAq8bFQdq4zKm6BTX8mWIV7FqLXOoOgCPCuuwofvAz4Ox62DZT0FvxBfKY54vLm9d0MVwWOTqApybPqXbGzIP+hAaLigff6SO/UtS/YK7ehEaJswBw5axREEi5O7Aya5FLZcXhYmkf5YG83LVaNMwkWqH9hl9tznlEIKEOWVbhAedDFQIBbY4pvVv3xLaAm0YoEyI4/ocp0FwBfKi4hvjq8C2AJMBZJPHtewWo2bkv5ixqIGLMVQpLSLik6ZNRDrLO3/RRe88sWQb7vzdYyA3DYV4f0/kn7mjwf616FBaZ1cwoTeBwx8n2p3Qz8Gshb5DdU0suHVuT6r5h1cvH30t24vaGfcHWR6M7Gc0suARC7t0Kpv3evvEp9cnpLWOGMbA/Xv9Tfizf5H62rdVz/76vll6uLNxGSDYtoc3hG7dovNY2eu2UfBg9dGU9/JuONv/8SMo2X==",
        "Host": "passport.goofish.com",
        "xweb_xhr": "1",
        "x-ticid": "AQ9g7yKkBDVOuI5T7Z1TMJ2q-HrBr2PXuBIsRP2MQHbiJ_CwKrrihA1Y-sEx7jvOmJG7Qj5n5_YdKK7r37_HHqWQQZJJ",
    }
    data = {
        "type": "weixin_mini_program",
        "appId": "wx9882f2a891880616",
        "appName": "xianyu",
        "appEntrance": "wx_goofish",
        "sellerAppId": "",
        "lang": "zh_CN",
        "isMobile": "true",
        "returnUrl": "",
        "needPassWebViewCookie": "false",
        "authorizationCode": {"authorizationCode": "0f3MHw1007aBVT1F0F300fB3ju4MHw1B",
                              "type": "phone",
                              "encryptedData": "RRrpumXsSr8DMnFIAuYPDqrC258FrDy+9toQ4P3B0klO8uxtRSWFcfSrpncQ+W5UIEWlfkVaAG5K7hgTHI8nddDSnf7lhLdgJBm2/qPWNaMzROwEUMvQI5iXE8VxpYXaDYfSNOLkhiJ4GpXEzXKc+qknLrkGMc3JSs8mBt5w4oa3e9ysGWYFvOVs9SsYYV/mVgJu9hCOJ0ChRko8hMNK2Q==",
                              "iv": "ZguxVUho/5DDiWUtzUNNfw==",
                              "cloudID": "90_ojsWoACUlJRnHqqS_k4slZhWKTE9S0FIdmIn7JDvlQS2tbzqS3jzv60jHwQ",
                              "code": "12e0e1f2afc39bc53c22db3886b0e48d5bba2bca0b5ee1c3914c74ddf3cd64fe"},
        "nativeMp": "true",
        "getUnionIdByPNAuth": "undefined",
        "pageId": "BIND_LOGIN_PAGE",
        "pageTraceId": "821355ae-8cd6-4d45-a64c-44a5c879a959"
    }
    print(requests.session().post(url, data=data, verify=False).json())

def 验证登录2(session):
    url = 'https://passport.goofish.com/skip_sessionfilter/login_token_login.htm?token=idc_1FN4H3bfBkhWEvQAgvcIdSQ&subFlow=MINIPROGRAM_TRUST_URL&nextCode=0009&bizScene=apply_trust_login_url&unionId=o2FAH6USh8jipVct8IZ5h7DCwqrQ&openId=ozQTw4rCv_B39vRrwTXwx0TDdXrA'
    response = session.get(url,verify=False)
    # print(response.cookies)
    return response.cookies
def 获取小程序闲鱼订单():

    url = 'https://h5api.m.goofish.com/h5/mtop.taobao.idle.trade.sold.get/5.0/'
    t = int(time.time())*1000
    params = {
        "jsv": '2.7.2',
        "appKey": '12574478',
        # "t": "1742295979793",
        # "t": "1742316893617",
        "t": str(t),
        # "sign": '339bc9d8abd2e9f14c7a299262dd28e1',
        "sign": '68972f1018db039a0baaeb9f332e9e22',
        "api": 'mtop.taobao.idle.trade.sold.get',
        'v': '5.0',
        'dataType': 'json',
        'valueType': 'original',
        'accountSite': 'xianyu',
        'dangerouslySetWindvaneParams': '[object Object]',
        'type': 'originaljson',
        'data': '{"pageNumber":1,"orderStatus":"ALL","offsetRow":0}'
    }

    # headers = {
    #     "cookie": "munb=2107783797; cookie2=1e20f84b1cb7a90a3e6b578676d7489b;
    #     csg=3aeaad9b;
    #     t=a562c6a9e4a47d6216f1621beeb6a2ff;
    #     _tb_token_=35bee6d391733;
    #     unb=2107783797; xlly_s=1; mtop_partitioned_detect=1;
    #     _m_h5_tk=898731b310e6f2970fcd717ce357ec81_1742209794535;
    #     _m_h5_tk_enc=cf0f2fa7c59dbb34fd70d3db50d419ed;
    #     sgcookie=M100zP4wkCTA2mbeuFUuc4EXDlLuYjF8fMz9Cr5+NMXi2aSfgxbvJvAscdUFcyDLc+RrkHYzNyjTSo2rlGM2+txa09/LslBrOnHo9YHqsqxnRZkP3LVZQOJ8iPcm9gWyhPsP;
    #     cna=281eID9cuBYCAavUZa5tr5nj;
    #     tfstk=g_-q2lMmEmn27JtqsTjaz3x9HqgAficIsh11IdvGhsfDftYyb_RdGsM9l12NaCCfliqX_5fkaswfhixw_K9Fo1_1cVrwspf0Gl9cINA6NoMxM1iw_Q5R1xKwBlWMICHA1x35DKIOjXGB_D9vHpwjkZh5jAvlfOoG9sEWHKITe8NiRUvY_yVZDCjMsgjlK9sgjtAGrafRBOVcIoDyE_ClnPf0jaVlC9WgjCjiULfRIGfiZPsGv7W1oAzvT0udyt7VtKfkhKtl3W1Hn_rgjGBVut9calqM2UZ7HffmJ81OcspA3CnLDibwSnskmbmGxedybwjE5xIHDdYpSLFqQsvWMHSDYjrfFN52rnbzIlvV2Ebk7Il4ksYXawBlrRodFB1kHnYrB7vDOsScEainLLbMPnQpcbqVxepfcFAnNr1D8Ojy65BlarxMjcUNoTBPOYkPwymdG7S8ThzTWZeRU6McoPUOoLWPOYH7WPQACT5IE1C..;
    #     isg=BLGxbQiEcpfemd6D3K6_64JNyz1LniUQAxFWMZPGrHiXut"
    # }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c11)XWEB/11581",
        "Host": "h5api.m.goofish.com",
        "Content-type": "application/x-www-form-urlencoded",
        "Origin": "https://h5.m.goofish.com",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer":"https://h5.m.goofish.com/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "cookie":
            "munb=2107783797; "
            "unb=2107783797; "
            "cna=lyNgIKwHDlACAavUZa4nV8J4; "
            "xlly_s=1; "
            "mtop_partitioned_detect=1; "
            f"_m_h5_tk=0bd1598c724d4adb730eb62735aaafb9_1742304621764; " 
            "_m_h5_tk_enc=032720e8eb3f44328608980fc99fcaac; "
              # "sgcookie=M100aqS6Esb/2BmmHN/pZUOtTn5dzoek7iXbAyrSVfBoTMJ5If3BwAA8/NYwP7kIVChet8KUGebREyaxGiXDNYF2DyDK4UicD+fhVjg39/aCfQ4ZXtg3U1iIi7JMbEdQDgOB; "
              # "isg=BCwse6zzZya7enMU6YVKhK-m9gpe5dCPHop7RoZtOld6kcybrvWsHhqzt1kpAgjn; "
              "cookie2=1d3bfbd757e7b7fed1daff781ddd70a8; "
              # "csg=98b693cc; "
              # "t=acafec71f53212e5d0c15e41da52bbc1; "
              # "_tb_token_=7ef635355373e; "
              # "tfstk=gPeq0OjcqtBVsIwVS0DwayAr9ICxBxbCSRgsjlqicq0mCs3iSlU-fdZghPza8rJb5lbY7RuuXxZjCt3MQlqTcqZ1XOSavyosoPMX7OzzwdgbliFaPzU8lowaXdogjPIx5iCSHoHtIw_Q79ZYDbFJXEQSIGqoCcz-Me9aDoH92w_Cd9Zv7IizR5DgSYDovDDiSPmG44mZvCY0SAjP4cmMndvDiT0ojcDiSPDG4u0-jb-ZIvLrfjjwsMcstsnjg2qmzpr8UmDDMo0y_Cyzvju374JMI8oYV3f4Ip5s-W3jO2UlFKkaqczrOS7e3Prgv5czQEjb-l4YUxHF1ihUZ7NIg77DQ4wjbXDiahvg4Yu88RDhKUo8ZoNgHr-wImebdfuKaGvt1Y2ItW42XMEonc4t9R_pHqqgvJFILt8K07qEUgyMW00yiR2GBClm20uC4guJt93by0strCdtM3nrRicD6Ch040uC2gO96j3o42sos"
    }
    with requests.Session() as session:
        for num in range(1, 3):
            response = session.get(url, params=params, headers=headers, verify=False)
            data = response.json()
            if data['ret'][0] == "FAIL_SYS_TOKEN_EXOIRED::令牌过期":
                print("令牌过期了")
                headers['cookies'] = "munb=2107783797; unb=2107783797; cna=lyNgIKwHDlACAavUZa4nV8J4; xlly_s=1; mtop_partitioned_detect=1; cookie2=19ab34bf87c7b24f7ba3941f2d9cd5e7;"
                for i in response.cookies.items():
                    headers['cookies'] += i[0]+"="+i[1]+";"

    print(json.dumps(data, ensure_ascii=False))


if __name__ == '__main__':
    # 验证登录2()
    # 小程序登录闲鱼()
    获取小程序闲鱼订单()
