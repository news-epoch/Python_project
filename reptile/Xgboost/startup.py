import sys, os
import threading

from PyQt5 import uic, QtGui
from PyQt5.QtCore import QThread, Qt
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow


class MyThread(QThread):
    def __init__(self, featuresOne, featuresTwo, featuresThree, featuresFour, featuresFive, featuresSix,message):
        super().__init__()
        self.featuresOne = featuresOne
        self.featuresTwo = featuresTwo
        self.featuresThree = featuresThree
        self.featuresFour = featuresFour
        self.featuresFive = featuresFive
        self.featuresSix = featuresSix
        self.message = message
    def run(self):
        return self.xgbThread()

    def xgbThread(self):
        from xgbModel import xgbModel
        xgb = xgbModel()
        msg = xgb.predict(feature1=self.featuresOne,
                    feature2=self.featuresTwo,
                    feature3=self.featuresThree,
                    feature4=self.featuresFour,
                    feature5=self.featuresFive,
                    feature6=self.featuresSix,
                    )
        # 开始渲染结果
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(18)
        self.message.setText(msg)


class Mywindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
        print(self.BASE_DIR)
        self.ui = uic.loadUi(os.path.join(self.BASE_DIR, "XGboost2.0.ui"))

        # 提取要操作的控件
        self.featuresOne_edit = self.ui.featuresOne_edit
        self.featuresTwo_edit = self.ui.featuresTwo_edit
        self.featuresThree_edit = self.ui.featuresThree_edit
        self.featuresFour_edit = self.ui.featuresFour_edit
        self.featuresFive_edit = self.ui.featuresFive_edit
        self.featuresSix_edit = self.ui.featuresSix_edit

        self.forecasting_button = self.ui.forecasting_button

        self.message = self.ui.message

        # 绑定信号与槽函数
        self.forecasting_button.clicked.connect(self.XGVRegressor())

    def XGVRegressor(self):
        # 获取参数
        featuresOne = self.featuresOne_edit.text()
        featuresTwo = self.featuresTwo_edit.text()
        featuresThree = self.featuresThree_edit.text()
        featuresFour = self.featuresFour_edit.text()
        featuresFive = self.featuresFive_edit.text()
        featuresSix = self.featuresSix_edit.text()

        # 开始预测
        predict = MyThread(featuresOne=featuresOne,
                           featuresTwo=featuresTwo,
                           featuresThree=featuresThree,
                           featuresFour=featuresFour,
                           featuresFive=featuresFive,
                           featuresSix=featuresSix,
                           message=self.message)
        predict.start()




if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    w = Mywindow()
    w.show()
    sys.exit(app.exec_())
