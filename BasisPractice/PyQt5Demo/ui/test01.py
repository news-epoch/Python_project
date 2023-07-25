import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon


class test01(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def button(self):
        btn1 = QPushButton("登录", self)
        # 绑定函数
        btn1.clicked.connect(lambda: self.example())
        btn1.x(50)
        btn1.y(50)


    def initUI(self):
        # 设置窗口位置  坐标x,坐标y,宽,高
        self.setGeometry(400, 300, 800, 400)
        # 设置窗口标题
        self.setWindowTitle("接口数据发送工具")
        self.button()
        # 显示窗口
        self.show()
    def example(self):
        print("Hello, World")



if __name__ == '__main__':
    print(sys.argv)
    app = QApplication(sys.argv)
    ts = test01()
    sys.exit(app.exec_())