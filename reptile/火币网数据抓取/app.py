import concurrent.futures
import datetime
from concurrent.futures import ThreadPoolExecutor

import pandas

import htx

if __name__ == '__main__':
    application = htx.load_yaml()
    hbg = htx.hbg(application['rank_type'])

    history_data = []
    today_data = []
    ohlcv = None
    if application['reptile_type'] == 1:
        user_signs = []

        page = 1
        while True:
            results = hbg.get_rank(page)
            page += 1
            if len(results['data']['itemList']) == 0:
                break
            for result in results['data']['itemList']:
                user_signs.append({'userSign': result['userSign'],
                                   'nickName': result['nickName'],
                                   'copyUserNum': f"{str(result['copyUserNum'])}/{str(result['fullUserNum'])}"})

        thread_pool = ThreadPoolExecutor(max_workers=application['max_workers'])

        futures = [thread_pool.submit(hbg.create_driver, user_sign) for user_sign in user_signs]

        concurrent.futures.wait(futures)
        for future in futures:
            print(future.result())
            # print(future.result())
            history_data.extend(future.result().get("历史带单"))
            today_data.extend(future.result().get("当前带单"))
        # for user_sign in user_signs:
        #     result = hbg.create_driver(user_sign)
        #     history_data.extend(result.get("历史带单"))
        #     today_data.extend(result.get("当前带单"))
    elif application['reptile_type'] == 2:
        user_signs = []

        page = 1
        while True:
            results = hbg.get_rank(page)
            page += 1
            if len(results['data']['itemList']) == 0:
                break
            for result in results['data']['itemList']:
                user_signs.append({'userSign': result['userSign'],
                                   'nickName': result['nickName'],
                                   'copyUserNum': f"{result['copyUserNum']}/{result['fullUserNum']}"})
        thread_pool = ThreadPoolExecutor(max_workers=application['max_workers'])

        futures = [thread_pool.submit(hbg.startup, user_sign) for user_sign in user_signs]

        concurrent.futures.wait(futures)
        for future in futures:
            # print(future.result())
            history_data.extend(future.result().get("历史带单"))
            today_data.extend(future.result().get("当前带单"))
    elif application['reptile_type'] ==3:
        ohlcv = hbg.k_link(application['proxies_type'], application['proxies_http_port'], application['proxies_https_port'], application['symbol'], application['timeframe'], application['limit'])

    now_time = datetime.datetime.now().strftime("%Y%m%d%H")
    if ohlcv !=None:
        df = pandas.DataFrame(ohlcv, columns=["时间", "开盘价", "最高价", "最低价", "收盘价", "成交量"])
        # 时间戳转换为 UTC 时间
        df["时间"] = pandas.to_datetime(df["时间"], unit="ms")
        df.to_excel(f"{now_time}{str(application['symbol']).replace('/', '_')}_{application['timeframe']}_K线图.xlsx",index=False)
    else:
        pandas.DataFrame(history_data).to_excel(now_time + "历史带单数据.xlsx", index=False)
        pandas.DataFrame(today_data).to_excel(now_time + "当前带单数据.xlsx", index=False)