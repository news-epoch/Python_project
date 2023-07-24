import sys

from PyQt5.QtCore import Qt

from BasisPractice.PyQt5Demo.ui.test import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow

class myMainWindow(QMainWindow):  # 调用主页面类
    def __init__(self):
        QMainWindow.__init__(self)
        self.main_ui = Ui_MainWindow()
        self.main_ui.setupUi(self)


if __name__ == '__main__':
    # 加上下面这行 就可解决部分分辨率下 控件、文字显示不完整问题
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    myWin = myMainWindow()
    # 显示
    myWin.show()
    sys.exit(app.exec_())
