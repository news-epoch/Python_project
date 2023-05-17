from lxml import etree
import pandas as pd
import re
def countchn(string):
    pattern = re.compile(u'[\u1100-\uFFFDh]+?')
    result = pattern.findall(string)
    chnnum = len(result)            #list的长度即是中文的字数
    possible = chnnum/len(str(string))         #possible = 中文字数/总字数
    return (chnnum, possible)
def findtext(part):
    length = 50000000
    l = []
    for paragraph in part:
        chnstatus = countchn(str(paragraph))
        possible = chnstatus[1]
        if possible > 0.15:
            l.append(paragraph)
    l_t = l[:]
    #这里需要复制一下表，在新表中再次筛选，要不然会出问题，跟Python的内存机制有关
    for elements in l_t:
        chnstatus = countchn(str(elements))
        chnnum2 = chnstatus[0]
        if chnnum2 < 100:
        #最终测试结果表明300字是一个比较靠谱的标准，低于300字的正文咱也不想要了对不
            l.remove(elements)
        elif len(str(elements))<length:
            length = len(str(elements))
            paragraph_f = elements
def copeData(data,xpath):
    html = etree.HTML(data)
    rst1 = html.xpath(xpath)
    return rst1
    #
if __name__ == '__main__':
    data = []
    head_row = pd.read_csv('C:\\Users\\Administrator\\Documents\\BaiduNetdiskDownload\\百度资讯搜索_井冈山红色研学v2.csv',nrows=0)
    head_row_list = list(head_row)
    print(head_row_list)
    csv_result = pd.read_csv('C:\\Users\\Administrator\\Documents\\BaiduNetdiskDownload\\百度资讯搜索_井冈山红色研学v2.csv')
    x= 1
    for i in  csv_result.values.tolist():
        test = i[2].replace('...','').replace(',','，')[:30]
        i.append('null')
        xpath = "//*[contains(text(),'"+test + "')]/parent::*/parent::*/descendant-or-self::text()"
        i[4] = copeData(i[3].replace("\"",""), xpath)
        data.append(i)
        x +=1
    print(x)
    head_row_list.append('cope')
    df1 = pd.DataFrame(data,columns=head_row_list)
    df1.to_csv('./copeData.csv')





