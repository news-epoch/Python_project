import concurrent.futures
import datetime
from concurrent.futures import ThreadPoolExecutor

import pandas

from reptile.火币网数据抓取 import htx

if __name__ == '__main__':
    hbg = htx.hbg("综合排名")
    user_signs = []
    history_data = []
    today_data = []
    page = 1
    while True:
        results = hbg.get_rank(page)
        page += 1
        if len(results['data']['itemList']) == 0:
            break
        for result in results['data']['itemList']:
            user_signs.append(result['userSign'])

    thread_pool = ThreadPoolExecutor(max_workers=6)

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
    now_time = datetime.datetime.now().strftime("%Y%m%d")
    pandas.DataFrame(history_data).to_excel(now_time+"历史带单数据.xlsx", index=False)
    pandas.DataFrame(today_data).to_excel(now_time+"当前带单数据.xlsx", index=False)