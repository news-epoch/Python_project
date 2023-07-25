import sys

from PyQt5.QtCore import Qt

from sendDataui import Ui_MainWindow

from PyQt5.QtWidgets import QApplication, QMainWindow



if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)

    mainWindow = QMainWindow()

    ui = Ui_MainWindow()

    ui.setupUi(mainWindow)

    mainWindow.show()

    app.exec_()
