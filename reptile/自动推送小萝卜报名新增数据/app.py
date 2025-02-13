import time

from xiaoluobo import sendEmail
import schedule

if __name__ == '__main__':
    # schedule.every(30).to(60).minutes.do(sendEmail)
    schedule.every().hour.do(sendEmail)
    while True:
        schedule.run_pending()
        time.sleep(1)