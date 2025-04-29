import ccxt
import pandas as pd
from datetime import datetime

# 初始化交易所（以币安为例）
exchange = ccxt.binance({
    'enableRateLimit': True,  # 遵守速率限制
    'options': {
        'adjustForTimeDifference': True,  # 自动调整时间差
    }
})

# 定义时间戳和参数
timestamps = [1745757000000, 1745759296000]  # 你的时间戳（毫秒级）
symbol = 'ETH/USDT'
timeframe = '1m'  # K线周期：1分钟、5分钟等
proxies = {
            'http': f'socks5://127.0.0.1:10809',  # SOCKS5 代理
            'https': f'socks5://127.0.0.1:10808',
        }

def get_kline_data(timestamp):
    """获取指定时间戳的K线数据"""
    try:
        # 获取K线（最多重试3次）
        exchange = getattr(ccxt, 'binance')({
            'enableRateLimit': True,  # 启用请求频率限制
            "proxies": proxies
        })
        ohlcv = exchange.fetch_ohlcv(
            symbol=symbol,
            timeframe=timeframe,
            since=timestamp,
            limit=1
        )

        if not ohlcv:
            print(f"未找到 {timestamp} 的K线数据")
            return None

        return ohlcv[0]  # 返回第一条数据

    except Exception as e:
        print(f"获取数据失败: {str(e)}")
        return None


# 转换为北京时间并格式化
def convert_to_beijing(timestamp_ms):
    utc_time = pd.to_datetime(timestamp_ms, unit='ms')
    beijing_time = utc_time.tz_localize('UTC').tz_convert('Asia/Shanghai').tz_localize(None)
    return beijing_time.strftime('%Y-%m-%d %H:%M:%S')


# 主程序
results = []
for ts in timestamps:
    kline = get_kline_data(ts)
    if kline:
        data = {
            'timestamp': ts,
            'datetime': convert_to_beijing(ts),
            'open': kline[1],
            'high': kline[2],
            'low': kline[3],
            'close': kline[4],
            'volume': kline[5]
        }
        results.append(data)

# 创建DataFrame
df = pd.DataFrame(results)
print(df)