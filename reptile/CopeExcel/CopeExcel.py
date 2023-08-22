import os, sys

import pandas as pd
import openpyxl
class copeExcel:
    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
        self.names = set()

    def savefile(self, filename, data):
        with open(os.path.join(self.BASE_DIR,filename), 'w', encoding='utf-8') as fp:
            for i in data:
                fp.write(i)
                fp.write('\n')


    def copeExcel(self):


        # wb = openpyxl.load_workbook(os.path.join(BASE_DIR, "1.xlsx"))
        # wa = wb.active()
        pd_data = pd.read_excel(os.path.join(self.BASE_DIR, "输入文件.xlsx"))

        i = 0
        while True:
            try:
                print(pd_data.loc[i])
                if pd_data.loc[i]['成绩1'] >= 60 and pd_data.loc[i]['成绩2'] > 15:
                    self.names.add(pd_data.loc[i]['名字'])
                i += 1
            except:
                break

        self.savefile("输出文件.txt", self.names)



if __name__ == '__main__':
    test = copeExcel()
    test.copeExcel()
