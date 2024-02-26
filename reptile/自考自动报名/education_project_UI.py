import json


import os, sys


from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QScrollArea, QVBoxLayout
from PyQt5 import uic
from PyQt5 import QtCore






class MyWindow(QWidget):
    def __init__(self):
        self.ed = education()
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
        self.ui = uic.loadUi(os.path.join(self.BASE_DIR, "zikao.ui"))

        self.usernameLabel = self.ui.usernameLabel
        self.passwordLabel = self.ui.passwordLabel
        self.usernameEdit = self.ui.usernameEdit
        self.passwordEdit = self.ui.passwordEdit
        self.codeLabel = self.ui.codeLabel
        self.codeEdit = self.ui.codeEdit
        self.loginButton = self.ui.loginButton
        self.messagelabel = self.ui.messagelabel
        self.countyBox = self.ui.countyBox
        self.countylabel = self.ui.countylabel
        self.subjectBox = self.ui.subjectBox
        self.disciplinelabel = self.ui.disciplinelabel
        self.disciplineBox = self.ui.disciplineBox
        self.registrationNoLabel = self.ui.registrationNoLabel
        self.registrationNoEdit = self.ui.registrationNoEdit
        self.candidateButton = self.ui.loginButton_2
        self.flushCodeButton = self.ui.flushCodeButton

        self.design()

    def design(self):
        ft = QFont()
        # 配置下拉框
        _translate = QtCore.QCoreApplication.translate
        subjectdata, num = ["操作系统概论",
                            "计算机网络原理",
                            "英语(二)",
                            "管理经济学",
                            "数据库系统原理",
                            "信息资源管理",
                            "运筹学基础"], 0

        with open(os.path.join(self.BASE_DIR, "utils\\cdqxdm.txt"), "r", encoding="utf-8") as fp:
            qxdm = json.load(fp)

        for i in qxdm:
            self.countyBox.addItem("")
            self.countyBox.setItemText(num, _translate("Form", i["QX_MC"]))
            num += 1

        num = 0

        for i in subjectdata:
            self.subjectBox.addItem("")
            self.subjectBox.setItemText(num, _translate("Form", i))
            num += 1

        # 配置消息加载框
        ## 图片加载
        pix = QPixmap(os.path.join(self.BASE_DIR, 'utils\\valcode.gif'))
        width = pix.width()  ##获取图片宽度
        height = pix.height()  ##获取图片高度
        if width / self.messagelabel.width() >= height / self.messagelabel.height():  ##比较图片宽度与label宽度之比和图片高度与label高度之比
            ratio = width / self.messagelabel.width()
        else:
            ratio = height / self.messagelabel.height()

        self.messagelabel.setPixmap(pix.scaled(int(width / ratio), int(height / ratio)))

        ## 配置消息文字
        ft.setPointSize(14)
        ft.setFamily("SimSun")
        self.messagelabel.setFont(ft)

        ## 配置消息滚动
        # self.scroll_msg = QScrollArea(self.ui.MyWindow)
        # self.scroll_msg.setWidget(self.messagelabel)
        # self.scroll_msg.setGeometry(QtCore.QRect(353, 10, 441, 201))
        # self.messagelabel.setAlignment(Qt.AlignTop)
        # v_layout = QVBoxLayout()
        # v_layout.addWidget(self.scroll_msg)

        # 配置触发器绑定
        import threading

        self.loginButton.clicked.connect(self.login)
        self.flushCodeButton.clicked.connect(lambda: self.code())
        self.candidateButton.clicked.connect(lambda: self.subject())

    def login(self):
        try:
            self.ed.login(username=self.usernameEdit.text(), password=self.passwordEdit.text(),
                          zkzh=self.registrationNoEdit.text(), code=self.codeEdit.text())
            self.messagelabel.setText("【" + str(self.usernameEdit.text()) + "】登录成功")
        except Exception as e:
            print(e)
            self.messagelabel.setText("登陆失败")

    def subject(self):
        try:
            self.ed.subjectRegExam(qx=self.countyBox.currentText(), km=self.subjectBox.currentText())
            self.messagelabel.setText("报考\"" + self.subjectBox.currentText() + "\"成功")
        except Exception as e:
            self.messagelabel.setText("报考失败")

    def code(self):
        try:
            self.ed.getCodePng()
        except Exception as e:
            print(e)
            self.messagelabel.setText("获取验证码失败。")
            self.messagelabel.repaint()

        pix = QPixmap(os.path.join(self.BASE_DIR, 'utils\\valcode.gif'))
        width = pix.width()  ##获取图片宽度
        height = pix.height()  ##获取图片高度
        if width / self.messagelabel.width() >= height / self.messagelabel.height():  ##比较图片宽度与label宽度之比和图片高度与label高度之比
            ratio = width / self.messagelabel.width()
        else:
            ratio = height / self.messagelabel.height()

        self.messagelabel.setPixmap(pix.scaled(int(width / ratio), int(height / ratio)))

        self.messagelabel.repaint()
