import pandas


def 处理地址():
    xlsx_path = 'C:\\Users\\Administrator\\Desktop\\银鹏燃气原始设备数据_202507031404.xlsx'

    pd = pandas.read_excel(xlsx_path)
    xq_pd = pd.loc[pd['地址'].str.contains('小区')]
    xq_pd.to_excel('银鹏燃气小区地址设备数据.xlsx', index=False)

def 处理地址1():
    pd = pandas.read_excel('银鹏燃气小区地址设备数据.xlsx')
    data = []
    for i in pd.index.values:
        temp = pd.loc[i].to_dict()
        temp['原始地址'] = temp['地址']
        temp['所属区县'] = ''
        temp['所属街道'] = ''
        temp['所属社区'] = ''
        temp['所属小区'] = ''
        if pd.loc[i]['地址'].str.contains('新都区'):
            temp['所属区县'] = '新都区'
            temp['地址'] = str(temp['地址']).replace('新都区', '')

        data.append(temp)


if __name__ == '__main__':
    处理地址()