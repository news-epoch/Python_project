import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLineEdit,
                             QComboBox, QPushButton, QMessageBox, QMainWindow)


class HomeForm(QMainWindow):
    pass

class InputForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口属性
        self.setWindowTitle('数据输入表单')
        self.setGeometry(300, 300, 300, 200)

        # 创建布局
        layout = QVBoxLayout()

        # 创建文本框
        self.text_input = QLineEdit(self)
        self.text_input.setPlaceholderText("请输入文本...")
        layout.addWidget(self.text_input)

        # 创建下拉框
        self.combo_box = QComboBox(self)
        self.combo_box.addItems(["选项1", "选项2", "选项3"])
        layout.addWidget(self.combo_box)

        # 创建确认按钮
        self.submit_btn = QPushButton("确定", self)
        self.submit_btn.clicked.connect(self.get_data)
        layout.addWidget(self.submit_btn)

        self.setLayout(layout)

    def get_data(self):
        """获取并处理数据"""
        # 获取文本框内容
        text_value = self.text_input.text()

        # 获取下拉框内容
        combo_value = self.combo_box.currentText()
        combo_index = self.combo_box.currentIndex()

        # 显示获取结果（这里使用消息框展示）
        result = f"文本内容: {text_value}\n下拉选项: {combo_value} (索引: {combo_index})"
        QMessageBox.information(self, "输入结果", result)

        # 也可以直接处理数据（比如打印到控制台）
        print("获取到数据：")
        print(f"文本：{text_value}")
        print(f"选择项：{combo_value} (索引：{combo_index})")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = InputForm()
    window.show()
    sys.exit(app.exec_())