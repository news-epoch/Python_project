import  json
import sys, os
import pandas as pd


def export_excel():
    BASEDIR = os.path.dirname(os.path.realpath(sys.argv[0]))

    with open(os.path.join(BASEDIR, "utils\\公司[有].json"), 'r', encoding='utf-8') as fp:
        data = json.loads(fp.read())

    data1 = []
    for i in data:
        if isinstance(i, dict):
            data1.append(i)

    pand = pd.DataFrame(data=data1)
    pand.to_excel(os.path.join(BASEDIR, "公司.xlsx"))


def load_json_name(filename):
    BASEDIR = os.path.dirname(os.path.realpath(sys.argv[0]))

    with open(os.path.join(BASEDIR, str("utils\\"+filename)), 'r', encoding='utf-8') as fp:
        data = json.loads(fp.read())

    return data


def devi_file():
    BASEDIR = os.path.dirname(os.path.realpath(sys.argv[0]))
    data = []
    with open(os.path.join(BASEDIR, str("公司(5).txt")), 'r', encoding='utf-8') as fp:
        data = fp.read()

    for i in range(0, 5):
        pass

    with open(os.path.join(BASEDIR, ("公司"+str(i)+".txt")), 'r', encoding='utf-8') as fp:
        fp.read()




if __name__ == '__main__':
    export_excel()