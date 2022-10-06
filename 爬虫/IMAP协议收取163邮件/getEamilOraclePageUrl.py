import imaplib
import email
from imaplib import IMAP4_SSL
from operator import itemgetter
import re
import time
def login():
    mail_host = 'imap.163.com'
    mail_pass = 'YHGQQMQYHCHBMXQD'
    mail_email = 'newsepoch@163.com'
    server = IMAP4_SSL(mail_host, port=993)
    emailDataList = dict()
    imaplib.Commands['ID'] = ('NONAUTH', 'AUTH', 'SELECTED')
    args = ("name", "clientname", "contact", "newsepoch@163.com", "version", "1.0.0", "vendor", "myclient")
    typ, dat = server._simple_command('ID', '("' + '" "'.join(args) + '")')

    server.login(mail_email,mail_pass)

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
        for part in msg.walk():    # 通常组成属性结构，对其进行遍历
            # print(part.get_content_type())    # 查看这个主题又哪些内容组成
            if part.get_content_maintype() == 'text':
                body = part.get_payload(decode=True)
                emailPage = body.decode('utf8')
        emailDataList.append({'head':msg['Subject'], 'date':date2,'page':emailPage})
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
