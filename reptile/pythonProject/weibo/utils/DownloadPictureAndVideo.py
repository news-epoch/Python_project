import pandas as pd
from openpyxl import load_workbook
import requests
import os

def DownloadPicture():
    # 读取excel
    workbook = load_workbook(filename="./微博评论02.xlsx")
    sheet = workbook.active
    values = sheet.values
    df = pd.DataFrame(values)
    ## 将数据转换成数组
    nmp = df.to_numpy()
    ## 将表头删除
    nmp[0] = 'null'
    for i in  nmp:
        ## 跳过表头数据
        if i[0] == 'null':
            continue

        ## 处理数据
        temp = str(i[1]).replace('https://weibo.com/', '')
        temp = temp.replace('/','_')
        # 图片
        pictureUrlList = str(i[5]).replace('_x000d_\n','').split(';')
        pictureFolder = CreateDir(i[0]+'/'+temp+'/'+'图片')
        # 视频
        try:
            videoUrlList = str(i[6]).split(';')
        except:
            print("无视频")
        videoFolder = CreateDir(i[0] + '/' + temp + '/' + '视频')
        ## 循环下载图片并且重命名
        Download(pictureFolder,temp,pictureUrlList,'jpg')
        # pictureIndex = 0
        # for i in pictureUrlList:
        #     if i == '':
        #         continue
        #     headers = {
        #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        #         'Referer': 'https://weibo.com/'
        #     }
        #     r = requests.get(i, headers=headers)
        #     filename = str(pictureFolder)+'/'+temp+'_'+str(pictureIndex)+'.jpg'
        #     with open(filename,'wb') as fp:
        #         fp.write(r.content)
        #     pictureIndex +=1

        ## 循环下载视频并且重命名
        Download(videoFolder, temp, videoUrlList,'mp4')
        # videoIndex = 0
        # for i in videoUrlList:
        #     if i == '' or i == 'None':
        #         continue
        #     headers = {
        #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        #         'Referer': 'https://weibo.com/'
        #     }
        #     r = requests.get(i, headers=headers)
        #     filename = str(videoFolder) + '/' + temp + '_' + str(videoIndex) + '.mp4'
        #     with open(filename, 'wb') as fp:
        #         fp.write(r.content)
        #     videoIndex += 1

def Download(Folder, username, UrlList,format):
    Index = 0
    for i in UrlList:
        if i == '' or i == 'None':
            continue
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
            'Referer': 'https://weibo.com/'
        }
        r = requests.get(i, headers=headers)
        filename = str(Folder) + '/' + username + '_' + str(Index) + '.' + format
        with open(filename, 'wb') as fp:
            fp.write(r.content)
        Index += 1

def CreateDir(path):
    folder = os.getcwd()[:-4] + path
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

if __name__ == '__main__':
    DownloadPicture()
