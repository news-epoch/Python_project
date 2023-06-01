import pandas as pd
from openpyxl import load_workbook
import requests
import os
import sys
import tkinter
import re
#filename:文件名
def DownloadPicture(filename):


    ## 获取文件路径
    BASE_DIR = os.path.realpath(sys.argv[0])+'\..'
    filenamepath = os.path.join(BASE_DIR, filename)
    ## 读取excel
    workbook = load_workbook(filenamepath)
    sheet = workbook.active
    values = sheet.values
    df = pd.DataFrame(values)
    ## 将数据转换成数组
    nmp = df.to_numpy()
    ## 将表头删除
    nmp[0] = 'null'
    index = 1
    for i in  nmp:
        ## 跳过表头数据
        if i[0] == 'null':
            continue

        ## 处理数据  输出字段前10位
        temp = re.findall('[\u4e00-\u9fa5]', str(i[4]))
        temp = ''.join(temp)
        if temp.__len__() <= 10:
            pass
        else:
            temp = temp[0:10]

        # 图片
        pictureUrlList = str(i[3]).split(';')
        if pictureUrlList[0] != '':
            print(pictureUrlList)
            pictureFolder = CreateDir(temp+'/'+'评论图片'+str(index))

            # 下载图片
            Download(pictureFolder, temp, pictureUrlList, 'jpg')
        index += 1


#Folder:文件夹路径
#username: 文件名
#Urllist：请求地址列表

def Download(Folder, username, UrlList,format):
    Index = 0
    for i in UrlList:
        if i == '' or i == 'None':
            continue
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',

        }
        r = requests.get(i, headers=headers)
        filename = str(Folder) + '/' + username + '_' + str(Index) + '.' + format
        with open(filename, 'wb') as fp:
            fp.write(r.content)
        Index += 1

def CreateDir(path):
    folder = os.path.realpath(sys.argv[0]) + '\..\\' + path
    if not os.path.exists(folder):  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(folder)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print
        "---  new folder...  ---"
        print
        "---  OK  ---"
        return folder

    else:
        print
        "---  There is this folder!  ---"
        return folder

def find_up_box():
    """
    使用tkinter弹出输入框输入数字, 具有确定输入和清除功能, 可在函数内直接调用num(文本框的值)使用
    """
    root = tkinter.Tk(className='要进行下载的文件EXCEL')  # 弹出框框名
    root.geometry('300x100')  # 设置弹出框的大小 w x h
    # 设置标签信息
    label1 = tkinter.Label(root, text='请输入文件名：')
    label1.grid(row=0, column=0)


    # 创建输入框
    # 存放输入框信息
    filepath = tkinter.StringVar()


    entry1 = tkinter.Entry(root, textvariable=filepath)
    entry1.grid(row=0, column=1, padx=10, pady=5)


    # 创建按钮
    button1 = tkinter.Button(root, text='开始执行', command=lambda :[DownloadPicture(filepath.get())]).grid(row=3, column=0,
                                                              sticky=tkinter.W, padx=30, pady=5)
    button2 = tkinter.Button(root, text='退出', command=root.quit).grid(row=3, column=1,
                                                                 sticky=tkinter.E, padx=30, pady=5)

    # 上述完成之后, 开始真正弹出弹出框
    root.mainloop()

