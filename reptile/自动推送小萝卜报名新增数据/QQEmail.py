# encoding: utf-8
import logging
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from datetime import datetime

_logger = logging.getLogger('utils.mailclient')


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
        _msg['To'] = '; '.join(to_email)
        _msg['Date'] = datetime.now().strftime('%Y-%d-%m %H:%M:%S')
        try:
            _smtp_server.sendmail(self.mail_user, to_email, _msg.as_string())
            print("邮件发送成功")
        except smtplib.SMTPException:
            print("Error: 无法发送邮件")


    def close(self):
        self._dispose()
