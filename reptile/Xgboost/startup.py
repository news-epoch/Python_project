import sys, os
import threading

from PyQt5 import uic, QtGui
from PyQt5.QtCore import QThread, Qt, pyqtSignal
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow

from XGboostUI import Ui_Form


class predictThread(QThread):
    sinOut = pyqtSignal(str)

    def __init__(self):
        super(predictThread, self).__init__()


    def run(self):
        from xgbModel import xgbModel
        xgb = xgbModel()
        msg = xgb.predict(feature1=self.featuresOne,
                          feature2=self.featuresTwo,
                          feature3=self.featuresThree,
                          feature4=self.featuresFour,
                          feature5=self.featuresFive,
                          feature6=self.featuresSix,
                          )
        self.sinOut.emit(str(msg))

    def init(self, featuresOne, featuresTwo, featuresThree, featuresFour, featuresFive, featuresSix):
        self.featuresOne = featuresOne
        self.featuresTwo = featuresTwo
        self.featuresThree = featuresThree
        self.featuresFour = featuresFour
        self.featuresFive = featuresFive
        self.featuresSix = featuresSix


class Mywindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
        print(self.BASE_DIR)

        # self.ui = uic.loadUi(os.path.join(self.BASE_DIR, "XGboost2.0.ui"))
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        # 提取要操作的控件
        self.featuresOne_edit = self.ui.featuresOne_edit
        self.featuresTwo_edit = self.ui.featuresTwo_edit
        self.featuresThree_edit = self.ui.featuresThree_edit
        self.featuresFour_edit = self.ui.featuresFour_edit
        self.featuresFive_edit = self.ui.featuresFive_edit
        self.featuresSix_edit = self.ui.featuresSix_edit

        self.forecasting_button = self.ui.forecasting_button

        self.message = self.ui.message



        # 获取参数
        # featuresOne = float(self.featuresOne_edit.text().format('\t', '').format('\n', ''))
        # featuresTwo = float(self.featuresTwo_edit.text().format('\t', '').format('\n', ''))
        # featuresThree = float(self.featuresThree_edit.text().format('\t', '').format('\n', ''))
        # featuresFour = float(self.featuresFour_edit.text().format('\t', '').format('\n', ''))
        # featuresFive = float(self.featuresFive_edit.text().format('\t', '').format('\n', ''))
        # featuresSix = float(self.featuresSix_edit.text().format('\t', '').format('\n', ''))

        # 绑定信号与槽函数
        self.predict = predictThread()

        self.predict.sinOut.connect(self.XgbRegressor)

        self.forecasting_button.clicked.connect(self.XgbStrart)

    def XgbRegressor(self, msg):
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(18)
        self.message.setFont(font)
        self.message.setText(msg)

    def XgbStrart(self):
        # # 获取参数
        featuresOne = self.featuresOne_edit.text()
        featuresTwo = self.featuresTwo_edit.text()
        featuresThree = self.featuresThree_edit.text()
        featuresFour = self.featuresFour_edit.text()
        featuresFive = self.featuresFive_edit.text()
        featuresSix = self.featuresSix_edit.text()

        featuresOne = float(featuresOne)

        print(isinstance(featuresOne, float))
        self.predict.init(featuresOne=float(featuresOne),
        featuresTwo=float(featuresTwo),
        featuresThree=float(featuresThree),
        featuresFour=float(featuresFour),
        featuresFive=float(featuresFive),
        featuresSix=float(featuresSix))

        self.predict.start()




if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    w = Mywindow()
    w.show()
    sys.exit(app.exec_())
