import requests
import pandas as pd


class Doctor_reptile_request:
    def __init__(self):
        self.listdata = list()

    def getDataList(self, page):
        params = {
            'geoLocation': '42.32439478409065,-71.08756313798686',
            'limit': '20',
            'page': page,
            'radius': '100',
            'networkId': '311005033',
            'searchType': 'specialty',
            'teleHealthIncluded': 'undefined',
            'specialtyId': '311000124'
        }
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'bcbsma-prod.apigee.net',
            'Origin': 'https://member.bluecrossma.com',
            'Referer': 'https://member.bluecrossma.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'X-ClientName': 'MyBlueWeb',
            'X-ClientSessionId': 'e01f5a4d-9d79-495c-bc4c-7b93b8b20cc9',
            'X-ClientVersion': '24.1.0.28',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows"
        }
        response = requests.session().get("https://bcbsma-prod.apigee.net/digital/find-a-doctor/v1/providers",
                                          params=params,
                                          headers=headers, verify=False)

        return response.json()

    def getDataPage(self, providertype, providerId, LocaltionId):
        params = {
            'networkId': '311005033',
            'geoLocation': '42.32439478409065,-71.08756313798686',
            'locationId': LocaltionId,
            'providerId': str(providertype).lower() + str(providerId),
            'searchForTH': 'false'
        }
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'bcbsma-prod.apigee.net',
            'Origin': 'https://member.bluecrossma.com',
            'Referer': 'https://member.bluecrossma.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'X-ClientName': 'MyBlueWeb',
            'X-ClientSessionId': 'e01f5a4d-9d79-495c-bc4c-7b93b8b20cc9',
            'X-ClientVersion': '24.1.0.28',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows"
        }
        response = requests.session().get("https://bcbsma-prod.apigee.net/digital/find-a-doctor/v1/providers/profile",
                                          params=params, headers=headers, verify=False)
        return response.json()

    def copePageData(self, Data):
        print(Data)
        excelData = dict()
        # 名字
        excelData['title'] = Data['name']
        # 学校数据
        educations = Data['education']
        for i in range(0, 4):
            try:
                if len(educations[i]['name']) != 0 and len(educations[i]['type']) != 0:
                    excelData['education' + str(i)] = educations[i]['name'] + '\n' + educations[i]['type']
            except Exception:
                excelData['education' + str(i)] = '无'
                continue
        # gender
        gender = Data['gender']
        if len(gender) != 0:
            excelData['gender'] = gender
        else:
            excelData['gender'] = '无'

        # locations
        locations = Data['locations']
        for i in range(0, 6):
            try:
                test = locations[i]
            except Exception:
                excelData['location' + str(i)] = '无'
                continue
            address = test['address']
            name = test['name']
            phone = test['phone']
            locationDetails = test['amenities']
            strData = 'name: ' + str(name) + '\n' + 'address: ' + str(address) + '\n' + 'phone: ' + str(
                phone) + '\n' + 'locationDetails: ' + str(locationDetails)
            excelData['location' + str(i)] = strData

        # specialty
        specialty = Data['specialty']
        if len(specialty) != 0:
            excelData['specialty'] = specialty
        else:
            excelData['specialty'] = '无'

        # Identifiers
        identifiers = Data['locations'][0]['identifiers']
        identifiersText = ''
        for i in identifiers:
            identifiersText += str(i['typeCode']) + ": " + str(i['value']) + '\n'

        excelData['identifiers'] = identifiersText
        # Board Certification
        BoardCertifications = Data['locations'][0]['specializations']
        for i in range(0, 4):
            try:
                excelData['BoardCertification' + str(i)] = BoardCertifications[i]['isCertified'] + '\n' + \
                                                           BoardCertifications[i]['name']
            except:
                excelData['BoardCertification' + str(i)] = '无'

        # Affiliations
        Affiliations = Data['locations'][0]['hospitalAffiliations']
        Affiliationsstr = ''
        for affiliation in Affiliations:
            Affiliationsstr += '\n' + affiliation['name']

        excelData['Affiliations'] = Affiliationsstr
        # groupAffiliations
        groupAffiliations = Data['locations'][0]['groupAffiliations']
        for i in range(0, 4):
            try:
                test = groupAffiliations[i]
                excelData['groupAffiliations' + str(i)] = test['name']
            except:
                excelData['groupAffiliations' + str(i)] = '无'

        self.listdata.append(excelData)

    def exportExcel(self):
        pf = pd.DataFrame(self.listdata)
        pf.to_excel("test.xlsx", index=False)


if __name__ == '__main__':
    doctor = Doctor_reptile_request()

    # 输入要抓取的页数
    for i in range(1, 60):
        print("开始抓取第" + str(i) + "页")
        while True:
            try:
                listData = doctor.getDataList(i)['providers']
                if (listData.__len__() == 0):
                    print("请求第" + str(i) + "页出现异常，正在重新请求发送")
                    continue
                break
            except Exception:
                print("请求第" + str(i) + "页出现异常，正在重新请求发送")

        for j in listData:
            providerId = j['id']
            providertype = j['type']
            LocaltionId = j['locations'][0]['id']
            data = doctor.getDataPage(providertype=providertype, providerId=providerId, LocaltionId=LocaltionId)
            doctor.copePageData(Data=data)

    doctor.exportExcel()


# 比较两个数的大小     --------------> 这个就是函数
def test(a, b):
    if a - b > 0:
        print(str(a) + " 大")
    elif (a - b < 0):
        print(str(b) + " 大")
    elif (a - b == 0):
        print(str(a) + "和" + str(b) + "一样大")


class listData:
    # 这个就是方法
    def listDatatest(self, a, b):
        if a - b > 0:
            print(str(a) + " 大")
        elif (a - b < 0):
            print(str(b) + " 大")
        elif (a - b == 0):
            print(str(a) + "和" + str(b) + "一样大")


if __name__ == '__main__':
    ld = listData()
    ld.listDatatest(1, 2)

    listData().listDatatest(1, 2)

    test(1, 2)
