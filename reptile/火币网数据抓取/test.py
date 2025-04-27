import datetime
import time

if __name__ == '__main__':
    t = 1743436800000
    # local_time = time.localtime(t)
    # print(time.strftime("%Y-%m-%d %H:%M:%s", local_time))
    date = datetime.datetime.utcfromtimestamp(t/1000) + datetime.timedelta(hours=8)
    print(date.timestamp())
    print(date.strftime("%Y-%m-%d %H:%M:%S"))