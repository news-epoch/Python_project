import email
import imaplib
import os
import re
import sys
import time
from datetime import datetime
from imaplib import IMAP4_SSL
from operator import itemgetter

from RegisterHome import util


def parse_mail_time(mail_datetime):
    """
    邮件时间解析
    :param bytes:
    :return:
    """
    print(mail_datetime)
    GMT_FORMAT = "%a, %d %b %Y %H:%M:%S"
    GMT_FORMAT2 = "%d %b %Y %H:%M:%S"
    index = mail_datetime.find(' +0')
    if index > 0:
        mail_datetime = mail_datetime[:index] # 去掉+0800

    formats = [GMT_FORMAT, GMT_FORMAT2]
    for ft in formats:
        try:
            mail_datetime = datetime.strptime(mail_datetime, ft)
            return mail_datetime
        except:
            pass

    raise Exception("邮件时间格式解析错误")
def login():

    BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
    data = util.getLocalYmlFile(BASE_DIR, 'conf\emailLogin.yml')
    mail_host = data['mail_host']
    mail_pass = data['mail_pass']
    mail_email = data['mail_email']
    server = IMAP4_SSL(mail_host, port=993)
    emailDataList = dict()
    imaplib.Commands['ID'] = ('NONAUTH', 'AUTH', 'SELECTED')
    args = ("name", "clientname", "contact", "newsepoch@163.com", "version", "1.0.0", "vendor", "myclient")
    typ, dat = server._simple_command('ID', '("' + '" "'.join(args) + '")')

    server.login(mail_email, mail_pass)

    server.select("Inbox")

    type, data = server.search(None,'ALL')
    fetch_data_list = []
    for num in data[0].split():  # 获取到邮箱的的编号 然后对其遍历
        typ, fetch_data = server.fetch(num,'(RFC822)')  # 从邮箱中获取邮箱的数据(编号，'那一部分的数据编号')
        fetch_data_list.append(fetch_data)

    count = 1
    emailDataList = []

    for  fetch_data  in fetch_data_list:
        msg = email.message_from_bytes(fetch_data[0][1])  # 得到邮箱解析后的数据
        # Subject：主体、Date：日期，from：发件人
        emailPage = 'null'
        date1 = time.strptime(msg.get("Date")[0:24], '%a, %d %b %Y %H:%M:%S')  # 格式化收件时间
        date2 = time.strftime("%Y-%m-%d %H:%M:%S", date1)
        import datetime
        dateUTC = datetime.datetime.strptime(date2,"%Y-%m-%d %H:%M:%S")+datetime.timedelta(hours=8)


        for part in msg.walk():    # 通常组成属性结构，对其进行遍历
            # print(part.get_content_type())    # 查看这个主题又哪些内容组成
            if part.get_content_maintype() == 'text':
                body = part.get_payload(decode=True)
                emailPage = body.decode('utf8')
        emailDataList.append({'head':msg['Subject'], 'date':dateUTC,'page':emailPage})
    return  emailDataList


def getNewOracleClode(datadict):
    datadict.sort(key=itemgetter('date'),reverse=True)
    str1 = 'Verify your email to create your Oracle Cloud account'
    re1 = '(?<=<a href=")(.+?)(?="><)'

    for i in datadict:
        if str1 == i['head']:
            print(i['date'])
            result = re.search(re1, i['page'])
            return  result.group()

if __name__ == '__main__':
    msg = login()
    print(getNewOracleClode(msg))