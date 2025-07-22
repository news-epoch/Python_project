# encoding: utf-8
import logging
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from datetime import datetime

_logger = logging.getLogger('utils.mailclient')

def 创建日志(fileName):
    # logging.basicConfig(level=logging.INFO,
    #                              format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    #                              datefmt='%Y-%m-%d %H:%M:%S',
    #                              filename= fileName,  # 日志文件
    #                              filemode='a')  # 追加模式
    logger = logging.getLogger('spider')

    logger.setLevel(logging.DEBUG)

    # 输出到文件
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler(fileName, encoding='utf-8')
    file_handler.setFormatter(formatter)

    # 输出到控制台
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # 添加处理器到日志器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

class MailClient(object):
    def __init__(self, host, user, pwd=''):
        self.mail_host = host
        self.mail_user = user
        self.mail_pass = pwd
    def connect(self):
        smtpObj = smtplib.SMTP()
        smtpObj.connect(self.mail_host, 25)
        smtpObj.login(self.mail_user, self.mail_pass)
        return smtpObj
    def _dispose(self):
        if self._smtp_server is not None:
            self._smtp_server.quit()
            self._smtp_server = None

    def send(self, to_email, subject, content):
        _smtp_server = self.connect()

        _msg = MIMEText(content, 'html', 'utf-8')
        _msg['Subject'] = Header(subject, 'utf-8')
        _msg['From'] = self.mail_user
        _msg['To'] = '; '+ to_email
        _msg['Date'] = datetime.now().strftime('%Y-%d-%m %H:%M:%S')
        try:
            _smtp_server.sendmail(self.mail_user, to_email, _msg.as_string())
            print("邮件发送成功")
        except smtplib.SMTPException:
            print("Error: 无法发送邮件")


    def close(self):
        self._dispose()
