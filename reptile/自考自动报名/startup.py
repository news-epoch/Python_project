import threading

from education_project import education

if __name__ == '__main__':
    education01 = education()

    education01.login(username="51302919980523555X", password="23555X", zkzh="010818443102")


    while True:
        print("============================报考开始================================")
        text = education01.subjectRegExam(km=["计算机网络原理", "信息资源管理", "管理经济学"], qx="双流区", sz="成都")
        print("============================报考结束================================")
        if text.__contains__("报考成功"):
            break

    # QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    # App = QApplication(sys.argv)  # 创建QApplication对象，作为GUI主程序入口
    # stats = MyWindow()
    # stats.ui.show()  # 显示主窗体
    # sys.exit(App.exec_())