import tkinter


class pop_up_box:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title('配置界面')
        self.root.geometry('400x200')

    def button(self):

        # 设置文本框，读取粉丝数量范围
        ## 配置标签
        label1 = tkinter.Label(self.root, text='粉丝数区间：').grid(row=0, column=0)
        reviewer_max_num = tkinter.IntVar()  # 存放最大粉丝数量
        Entry_reviewer_max = tkinter.Entry(self.root, textvariable=reviewer_max_num,width=10).grid(row=0, column=1)
        label2 = tkinter.Label(self.root, text='~').grid(row=0, column=2)
        reviewer_min_num = tkinter.IntVar()
        Entry_reviewer_min = tkinter.Entry(self.root, textvariable=reviewer_min_num, width=10).grid(row=0, column=3)

        # tkinter.Button(self.root).grid(row=0, column=0)
        self.root.mainloop()


if __name__ == '__main__':
    test = pop_up_box()
    test.button()
