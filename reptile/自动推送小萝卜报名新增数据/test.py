import json
from datetime import datetime

# from reptile.自动推送小萝卜报名新增数据 import QQEmail
import schedule
import time

# from reptile.自动推送小萝卜报名新增数据.xiaoluobo import applicationYml, sendEmail
from xiaoluobo import sendEmail


def job():
    print("I'm working...")
#每隔1秒执行一次job函数
schedule.every(1).seconds.do(job)
#每隔10分钟执行一次job函数
schedule.every(10).minutes.do(job)
#每小时的整点执行job函数
schedule.every().hour.do(job)
#每天的14:30分执行job函数
schedule.every().day.at("14:30").do(job)
#随机地在每5到10分钟之间选择一个时间点执行job函数
schedule.every(5).to(10).minutes.do(job)
#每周一执行job函数
schedule.every().monday.do(job)
#每周三的13:15分执行job函数
schedule.every().wednesday.at("13:15").do(job)
#每个小时的第17分钟执行job函数
schedule.every().minute.at(":17").do(job)

if __name__ == '__main__':
    # s = QQEmail.MailClient(host='smtp.163.com', user='newsepoch@163.com', pwd='MFS33kEx8XwRSuvY')
    # s.send('819730159@qq.com', '测试', '测试邮件 From QQ')

    # s = '"[{\\"name\\": \\"成人国画\\", \\"price\\": \\"480.00\\", \\"unit\\": \\"份\\", \\"filePaths\\": [\\"https://file.xiaobaoming.com/7qgUxjTE6ymUkpUHWYXz9gE6qfa0DHev/file-name.jpg\\"], \\"current\\": 0, \\"limit\\": 12}, {\\"name\\": \\"成人书法\\", \\"price\\": \\"480.00\\", \\"unit\\": \\"份\\", \\"filePaths\\": [\\"https://file.xiaobaoming.com/HcOzwKjbTwN4TH4QXd2i5jgGHWNYSEsJ/file-name.jpg\\"], \\"current\\": 0, \\"limit\\": 12}, {\\"name\\": \\"成人瑜伽\\", \\"price\\": \\"480.00\\", \\"limit\\": 14, \\"unit\\": \\"份\\", \\"filePaths\\": [\\"https://file.xiaobaoming.com/rj0RRfWzL5myYnI90mWpJrFubtHyAGsf/file-name.jpg\\"], \\"current\\": 0}]"'
    # s1 = json.loads(s)
    # s2 = json.loads(s1)
    # print(s2)
    # for i in s2:
    #     print(i)
    #     print(i.get('name'))
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
    # applicationYml()
    sendEmail()