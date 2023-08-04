import requests
import tkinter
import sys, os

from  time import sleep
from PIL import Image, ImageTk
# 创建单机事件
from tkinter import messagebox

# 图片解码
import base64

# 将返回转成json
import json

# 读取数据文件
import pickle


def getPicture():

    BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
    picture_get = requests.get("http://154.91.228.3:6992/captchaImage")
    picture_json = picture_get.content
    test = picture_get.json()
    picture = base64.b64decode(test['img'])


    with open(os.path.join(BASE_DIR,"utils\\temp.gif"), 'wb') as fp:
        fp.write(picture)

    print(picture)
    picture_uuid = test['uuid']
    print(picture_uuid)

    if test['code'] == 200:
        return [picture_uuid, "验证码发送成功"]
    else:
        return ["null", "验证码发送失败，重新打开程序"]


def postLogin(picture_uuid, code, username, password):
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "username": username,
        "password": password,
        "code": code,
        "uuid": picture_uuid
    }
    response = requests.post('http://154.91.228.3:6992/login', json=data, headers=headers)
    response_json = json.loads(response.text)
    print(response_json.get('token'))

    token = response_json.get('token')
    if response_json.get('code') == 200:
        return [token, ">>>>>【" + username + "】登录成功<<<<<<"]
    else:
        return ["null", ">>>>>【" + username +"】"+ response_json.get('msg')+"<<<<<<"]


    # def pop_up(self):
    #
    #     self.getPicture()
    #     # 创建窗口
    #     root = tkinter.Tk()
    #
    #     # 显示标题
    #     root.title('数据登录窗口')
    #
    #     # 设置窗口大小
    #     # root.geometry("600x300+400+300")  # (宽度x高度)+(x轴+y轴)
    #
    #     # 输入账户密码
    #     label_username = tkinter.Label(root,text="用户名：").grid(row=0,column=0)
    #     username = tkinter.StringVar()
    #     Entry_username = tkinter.Entry(root, textvariable=username).grid(row=0, column=1)
    #     label_password = tkinter.Label(root, text="密码：").grid(row=1, column=0)
    #     password = tkinter.StringVar()
    #     Entry_password = tkinter.Entry(root, textvariable=password).grid(row=1, column=1)
    #
    #     # 输入验证码
    #
    #     label_code = tkinter.Label(root, text="请输入验证码：").grid(row=2, column=0)
    #     code = tkinter.StringVar()  # 用来存放验证码信息
    #     Entry_text = tkinter.Entry(root, textvariable=code)
    #     Entry_text.grid(row=2, column=1,ipady=10)
    #     # 获取图片
    #     img = Image.open("temp.gif")
    #     img = ImageTk.PhotoImage(img)
    #     label_img = tkinter.Label(root, image=img).grid(row=2, column=3, columnspan=3)
    #
    #
    #
    #     # label_text.insert("insert", "请输入验证码")
    #
    #     # 创建按钮
    #     btn1 = tkinter.Button(root, command=lambda: self.postLogin(code=code.get(), username=username.get(), password=password.get()))
    #     btn1["text"] = "登录账户"
    #     btn1.grid(row=4, column=1, ipadx=50)  # 按钮在窗口里面的定位
    #     # 绑定按钮事件
    #
    #     btn2 = tkinter.Button(root, command=lambda: self.sendData())
    #     btn2["text"] = "发送数据"
    #     btn2.grid(row=6, column=1, ipadx=50)  # 按钮在窗口里面的定位
    #
    #     # 维持窗口
    #     root.mainloop()  # 加上这一句，就可以看见窗口了

def sendData(token):
    # 创建基础路径
    BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
    # 获取数据
    filePath = os.path.join(BASE_DIR, 'utils\\data.pickle')
    data = []
    data_history = list()
    for i in pickle.load(open(filePath, "rb")):
        if isinstance(i, dict):
            data.append(i)

    header = {
        'Authorization': "Bearer " + token,
        'Content-Type': 'application/json'
    }
    # 发送数据
    for i in data:
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

            response = requests.post('http://154.91.228.3:6992/system/data', json=data_json, headers=header)
            if response.json()['code'] == 200:
                # data_history.append("<br>".join(data_json['anchorId']+">>>>>发送成功"))
                data_history.append(data_json['anchorId']+">>>发送成功")
            else:
                data_history.append(data_json['anchorId'] + ">>>" + response.json()['msg'] + ">>>发送失败")
                # data_history.append(data_json['anchorId']+">>>>>>发送失败")
        except (Exception, BaseException) as e:
            data_history.append("<br>".join(data_json['anchorId'] + ">>>>>"+ e +">>>>>发送失败"))
            print(e)
            print("-----------------------")
            print(repr(e))

    data_history.append("总共发送：" + str(data_history.__len__()) + "条")
    return data_history




