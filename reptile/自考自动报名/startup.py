from reptile.自考自动报名.education_project import education

if __name__ == '__main__':
    education01 = education()
    # education01.getHomeCookie()
    # education01.getCodePng()
    education01.login(username="51302919980523555X", password="23555X", zkzh="010818443102")
    # education01.login(username="510411199904011426", password="011426", zkzh="010818443068")
    # education01.chrome()
    # while True:
    #     json = education01.searchPlace()
    #     for i in json["data"]:
    #         if i['QX_MC'] == '自流井区' and i['REST_D'] != 0:
    #             text = education01.subjectRegExam(["管理经济学"], "自流井区")
    #             if text != '5' or text == 'success':
    #                 break
    #             elif text == '5' or text == 5:
    #                 continue
    #             break

    while True:
        text = education01.subjectRegExam(["管理经济学"], "双流区", "成都")
        if text.__contains__("报考成功"):
            break

    # QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    # App = QApplication(sys.argv)  # 创建QApplication对象，作为GUI主程序入口
    # stats = MyWindow()
    # stats.ui.show()  # 显示主窗体
    # sys.exit(App.exec_())