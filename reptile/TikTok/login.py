import requests
import tkinter

from PIL import Image, ImageTk
# 创建单机事件
from tkinter import messagebox

# 图片解码
import base64

# 将返回转成json
import json


class login:
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

    def postLogin(self, code):
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            "username": "manage",
            "password": "123456",
            "code": code,
            "uuid": self.picture_uuid
        }
        response = requests.post('http://154.91.228.3:6992/login', json=data, headers=headers)
        response_json = json.loads(response.text)
        print(response_json.get('token'))

        self.token = response_json.get('token')

    def pop_up(self):
        self.getPicture()
        # 创建窗口
        root = tkinter.Tk()

        # 显示标题
        root.title('数据登录窗口')

        # 设置窗口大小
        root.geometry("300x100+400+300")  # (宽度x高度)+(x轴+y轴)

        # 获取图片
        img = Image.open("temp.gif")
        img = ImageTk.PhotoImage(img)
        label_img = tkinter.Label(root, image=img).grid(row=1, column=1)

        # 输入验证码
        code = tkinter.StringVar()  # 用来存放验证码信息
        Entry_text = tkinter.Entry(root, textvariable=code)
        Entry_text.grid(row=2, column=1)
        # label_text.insert("insert", "请输入验证码")

        # 创建按钮
        btn1 = tkinter.Button(root, command=lambda: self.postLogin(code.get()))
        btn1["text"] = "发送验证码"
        btn1.grid(row=2, column=8)  # 按钮在窗口里面的定位
        # 绑定按钮事件

        # 维持窗口
        root.mainloop()  # 加上这一句，就可以看见窗口了

    def sendData(self, username, personNum, fans):
        self.pop_up()

        header = {
            'token': self.token,
            'Content-Type': 'application/json'
        }

        data = {'anchorId': username,
                'area': 'null',
                'source': 'null',
                'personNum': personNum,
                'diamond': 'null',
                'dayRank': 'null',
                'hisRank': 'null',
                'risingStar': 'null',
                'fans': fans
                }
        requests.post('http://154.91.228.3:6992/system/data', json=data, header=header)


if __name__ == '__main__':
    test = login()
    test.pop_up()
