import requests
import tkinter
import sys, os

from PIL import Image, ImageTk
# 创建单机事件
from tkinter import messagebox

# 图片解码
import base64

# 将返回转成json
import json

# 读取数据文件
import pickle

class sendData:
    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))

    def getPicture(self):
        picture_get = requests.get("http://154.91.228.3:6992/captchaImage")
        picture_json = picture_get.content
        test = picture_get.json()
        picture = base64.b64decode(test['img'])

        with open("temp.gif", 'wb') as fp:
            fp.write(picture)

        print(picture)
        self.picture_uuid = test['uuid']
        print(self.picture_uuid)
        print("-------------------------发送成功-----------------------------------------")

    def postLogin(self, code, username, password):
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            "username": username,
            "password": password,
            "code": code,
            "uuid": self.picture_uuid
        }
        response = requests.post('http://154.91.228.3:6992/login', json=data, headers=headers)
        response_json = json.loads(response.text)
        print(response_json.get('token'))

        self.token = response_json.get('token')
        print("------------------登录成功-----------------------------")

    def pop_up(self):

        self.getPicture()
        # 创建窗口
        root = tkinter.Tk()

        # 显示标题
        root.title('数据登录窗口')

        # 设置窗口大小
        # root.geometry("600x300+400+300")  # (宽度x高度)+(x轴+y轴)

        # 输入账户密码
        label_username = tkinter.Label(root,text="用户名：").grid(row=0,column=0)
        username = tkinter.StringVar()
        Entry_username = tkinter.Entry(root, textvariable=username).grid(row=0, column=1)
        label_password = tkinter.Label(root, text="密码：").grid(row=1, column=0)
        password = tkinter.StringVar()
        Entry_password = tkinter.Entry(root, textvariable=password).grid(row=1, column=1)

        # 输入验证码

        label_code = tkinter.Label(root, text="请输入验证码：").grid(row=2, column=0)
        code = tkinter.StringVar()  # 用来存放验证码信息
        Entry_text = tkinter.Entry(root, textvariable=code)
        Entry_text.grid(row=2, column=1,ipady=10)
        # 获取图片
        img = Image.open("temp.gif")
        img = ImageTk.PhotoImage(img)
        label_img = tkinter.Label(root, image=img).grid(row=2, column=3, columnspan=3)



        # label_text.insert("insert", "请输入验证码")

        # 创建按钮
        btn1 = tkinter.Button(root, command=lambda: self.postLogin(code=code.get(), username=username.get(), password=password.get()))
        btn1["text"] = "登录账户"
        btn1.grid(row=4, column=1, ipadx=50)  # 按钮在窗口里面的定位
        # 绑定按钮事件

        btn2 = tkinter.Button(root, command=lambda: self.sendData())
        btn2["text"] = "发送数据"
        btn2.grid(row=6, column=1, ipadx=50)  # 按钮在窗口里面的定位

        # 维持窗口
        root.mainloop()  # 加上这一句，就可以看见窗口了

    def sendData(self):
        filePath = os.path.join(self.BASE_DIR, 'data.pickle')
        data = []
        for i in pickle.load(open(filePath, "rb")):
            if isinstance(i, dict):
                data.append(i)

        header = {
            'token': self.token,
            'Content-Type': 'application/json'
        }
        # 发送数据
        for i in data:
            print(i)
            try:
                data_json = {
                        'anchorId': i['anchorId'],
                        'area': 'null',
                        'source': 'null',
                        'personNum': int(i['personNum']),
                        'diamond': 0,
                        'dayRank': 0,
                        'hisRank': 0,
                        'risingStar': 0,
                        'fans': int(i['fans'])
                        }
                requests.post('http://154.91.228.3:6992/system/data', json=data_json, headers=header)
            except (Exception, BaseException) as e:
                print(e)
                print("-----------------------")
                print(repr(e))







