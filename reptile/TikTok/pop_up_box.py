import tkinter
from reptileTikTok import carryTiktok

class pop_up_box:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title('配置界面')
        self.root.geometry('400x200')

        self.ct = carryTiktok()
        self.tiktok_login = carryTiktok()


    def set_fans(self):
        #
        # 设置文本框，读取粉丝数量范围
        ## 配置标签
        label1 = tkinter.Label(self.root, text='粉丝数区间(小~大)：').grid(row=0, column=0)
        reviewer_max_num = tkinter.IntVar()  # 存放最大粉丝数量

        Entry_reviewer_max = tkinter.Entry(self.root, textvariable=reviewer_max_num,width=10).grid(row=0, column=3)
        label2 = tkinter.Label(self.root, text='~').grid(row=0, column=2)
        reviewer_min_num = tkinter.IntVar()
        Entry_reviewer_min = tkinter.Entry(self.root, textvariable=reviewer_min_num, width=10).grid(row=0, column=1)

        btn = tkinter.Button(self.root, text="确定粉丝区间", command=lambda: self.ct.getData(reviewer_max_num=reviewer_max_num.get(), reviewer_min_num=reviewer_min_num.get())).grid(row=0, column=4)

    def set_login(self):
        # 配置登录按钮
        # button_login = tkinter.Button(self.root, text="登录tiktok", command=lambda: self.button_click())
        button_login = tkinter.Button(self.root, text="登录TikTok", command=lambda: self.tiktok_login.login())
        button_login.grid(row=1, column=0)

    def export_data(self):
        button_export = tkinter.Button(self.root, text="导出数据文件", command=lambda: self.ct.export_excel())
        button_export.grid(row=1, column=1)

    def start(self):
        self.set_fans()
        self.set_login()
        self.export_data()
        self.root.mainloop()


