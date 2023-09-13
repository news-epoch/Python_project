import os, sys

import pandas as pd
import openpyxl


class copeExcel:
    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))

    def savefile(self, filename, data):
        BASE_DIR = self.BASE_DIR + "\\输出文件"
        if not os.path.exists(BASE_DIR):
            os.mkdir(BASE_DIR)

        with open(os.path.join(BASE_DIR, filename), 'w', encoding='utf-8') as fp:
            for i in data:
                fp.write(i)
                fp.write('\n')

    def copeExcel(self):

        # wb = openpyxl.load_workbook(os.path.join(BASE_DIR, "1.xlsx"))
        # wa = wb.active()
        # 读取需要处理的文件， 放入文件名就可以了
        BASE_DIR = self.BASE_DIR + "\\处理文件"
        if os.path.exists(BASE_DIR):
            for filename in os.listdir(BASE_DIR):
                names = set()
                pd_data = pd.read_excel(os.path.join(BASE_DIR, filename))
                i = 0
                while True:
                    try:
                        print(pd_data.loc[i])
                        # 判断条件
                        if pd_data.loc[i]['Identity'] >= 60 and pd_data.loc[i]['Align_length'] > 15:
                            self.names.add(pd_data.loc[i]['Query_id'])
                        i += 1
                    except:
                        break

                # 将排查出来的内容保存到txt文件中
                self.savefile(str(filename).replace("xlsx", "txt"), names)


if __name__ == '__main__':

    test = copeExcel()
    test.copeExcel()
