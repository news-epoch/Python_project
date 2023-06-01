import pandas as pd
from openpyxl import load_workbook
from openpyxl.drawing.image import Image
import requests, re
import os, sys, tkinter
from time import sleep
# 抖音热点宝_完全版_01.xlsx
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
        ## 处理数据  输出字段前10位 temp用来存储处理之后图片数据
        temp = re.findall('[\u4e00-\u9fa5]', str(i[2]))
        temp = ''.join(temp)
        if temp.__len__() <= 10:
            pass
        else:
            temp = temp[0:10]
        videotemp2 = re.findall('[\u4e00-\u9fa5]', str(i[2]))
        videotemp2 = ''.join(videotemp2)
        videotemp1 = re.findall('[\u4e00-\u9fa5]', str(i[1]))
        videotemp1 = ''.join(videotemp1)
        videotemp = videotemp1 +'_' + videotemp2
        if videotemp.__len__() <= 200:
            pass
        else:
            videotemp = videotemp[0:500]
        # 下载示例图片
        examplesPictureUrl = [str(i[0])]
        videoUrlList = [str(i[11])]

        if examplesPictureUrl[0] != '' and videoUrlList[0] != '' :
            print(examplesPictureUrl)

            videoFolder = CreateDir(filename.replace('.xlsx', '') + '\\' + '视频' + str(index))
            pictureFolder = CreateDir(filename.replace('.xlsx', '')+'\\'+'示例图片'+str(index))


            # 下载图片和视频
            videoPath = Download(videoFolder, videotemp, videoUrlList, 'mp4')
            examplesPicturePath = Download(pictureFolder, temp, examplesPictureUrl, 'jpg')
            ## 判断文件是否存在，存在择进行下一步，不存在则等待
            ## 将图片存放Excel中
            for i in range(0,15):
                if os.path.exists(examplesPicturePath):
                    imgsize = (50, 80)
                    picture_cell = 'M' + str(index + 1)
                    video_cell = 'N' +str(index+1)
                    sheet.column_dimensions['M'].width = imgsize[0]*0.14 # 修改列M的宽
                    sheet.column_dimensions['N'].width = imgsize[0]*0.14 # 修改列N的宽
                    sheet.row_dimensions[index+1].height = imgsize[1]*0.8 # 修改行高
                    img = Image(examplesPicturePath)  # 缩放图片
                    img.width, img.height = imgsize
                    # video_file = open(videoPath, 'rb').read() #插入视频
                    # video = Image(video_file)
                    # video.width, video.height = imgsize
                    sheet.add_image(img, picture_cell)  # 图片 插入 L1 的位置上
                    # sheet.add_image(video_file, video_cell)  # 视频 插入 M1 的位置上

                    break
                else:
                    sleep(10)

        index += 1

    workbook.save(os.path.join(BASE_DIR, ('已处理_'+ str(filename))))


#Folder:文件夹路径
#username: 文件名
#Urllist：请求地址列表
#layout: 文件后缀格式
def Download(Folder, filename, UrlList, layout):
    Index = 0
    for i in UrlList:
        if i == '' or i == 'None':
            continue
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',

        }
        r = requests.get(i, headers=headers)
        filepath = str(Folder) + '\\' + filename + '_' + str(Index) + '.' + layout
        with open(filepath, 'wb') as fp:
            fp.write(r.content)
        Index += 1


        return filepath

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


