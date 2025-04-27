import concurrent.futures
import datetime
import logging
import logging.config as log_config
from concurrent.futures import ThreadPoolExecutor
from os import system

import pandas

import htx
# 基础配置（只需在程序入口配置一次）
application = htx.load_yaml()
log_config.dictConfig(application['logging'])
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    hbg = htx.hbg(application['rank_type'])
    history_data = []
    today_data = []
    ohlcv = None
    now_time = datetime.datetime.now().strftime("%Y%m%d%H")

    if application['reptile_type'] == 1:
        pass
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
            logger.info(future.result())
            # logger.info(future.result())
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
            logging.info(f"爬取{page}页")
            results = hbg.get_rank(page)
            page += 1
            try:
                if len(results['data']['itemList']) == 0:
                    break
            except Exception as e:
                continue
            for result in results['data']['itemList']:
                user_signs.append({'userSign': result['userSign'],
                                   'nickName': result['nickName'],
                                   'copyUserNum': f"{result['copyUserNum']}/{result['fullUserNum']}"})
        logger.info(f"当前获取带单人数{len(user_signs)}")
        thread_pool = ThreadPoolExecutor(max_workers=application['max_workers'])
        futures = [thread_pool.submit(hbg.startup, user_sign) for user_sign in user_signs]

        concurrent.futures.wait(futures)
        for future in futures:
            # logger.info(future.result())
            history_data.extend(future.result().get("历史带单"))
            today_data.extend(future.result().get("当前带单"))

        df1 = pandas.DataFrame(history_data)
        df1.to_excel(now_time + "历史带单数据.xlsx", index=False)
        pandas.DataFrame(today_data).to_excel(now_time + "当前带单数据.xlsx", index=False)
    elif application['reptile_type'] == 3:
        ohlcv = hbg.k_link(application['proxies_type'],
                           application['proxies_http_port'],
                           application['proxies_https_port'],
                           application['symbol'],
                           application['timeframe'],
                           application['start_time'],
                           application['end_time'],
                           application['exchange_name'])
        if ohlcv != None:
            df = pandas.DataFrame(ohlcv, columns=["时间", "开盘价", "最高价", "最低价", "收盘价", "成交量"])
            # 时间戳转换为 UTC 时间
            df["时间"] = pandas.to_datetime(df["时间"], unit="ms").dt.tz_convert('Asia/Shanghai')
            df.to_excel(f"_{str(application['symbol']).replace('/', '_')}_{application['timeframe']}_K线图.xlsx", index=False)

    elif application['reptile_type'] == 4:
        data = hbg.comouter_yield(
            historical_leads_file_path=application['compute_yield']['historical_leads_file_path'],
            start_time=application['compute_yield']['start_time'],
            end_time=application['compute_yield']['end_time'],
            timeframe=application['compute_yield']['timeframe'],
            proxie_type=application['proxies_type'],
            proxies_http_port=application['proxies_http_port'],
            proxies_https_port=application['proxies_https_port'],
            exchange_name=application['exchange_name'],
            max_workers=application['compute_yield']['max_workers']
        )
        pd = pandas.DataFrame(data)
        pd.to_excel(str(application['compute_yield']['historical_leads_file_path']).replace(".xlsx", "（计算收益版）.xlsx"), index=False)
