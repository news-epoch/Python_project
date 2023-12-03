from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import  os

class getStore:

    def __init__(self):
        self.chrome_options = Options()

    def observerChrome(self):
        self.add_experimental_option("debuggerAddress", "127.0.0.1:9527")

        self.chromebro = webdriver.Chrome(
            service=Service(executable_path=os.path.join(self.BASE_DIR, 'utils\\chromedriver.exe')),
            options=self.chrome_options)

