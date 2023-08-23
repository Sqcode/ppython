
import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import uic
from functools import partial

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
sys.path.append(os.path.abspath(os.path.join(__dir__, './QtDesigner')))
from Ui_once import Ui_Form

class CenteredWindow(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        # 加载设计的UI文件
        # ui = uic.loadUi("GUI\QtDesigner\once.ui", self) 
        # 采用编译后的py文件 载入UI
        self.setupUi(self)  # 使用编译后的 setupUi 方法

        self.btn.clicked.connect(self.btn_clicked)  # 连接按钮的clicked信号与槽函数
        # self.alert.clicked.connect(alert)  # 连接按钮的clicked信号与槽函数

        # partial_func = partial(alert, arg='test')
        # self.alert.clicked.connect(partial_func)
        self.alert.clicked.connect(lambda checked, arg=1: self.show_msg(arg))  


    def btn_clicked(self):
        # 在按钮被点击时执行的操作
        print("按钮被点击了！")

    def show_msg(self, arg):
        message = f"Button clicked! Argument: {arg}"
        QMessageBox.information(self, "提示", message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CenteredWindow()
    # 展示窗口
    window.show()
    app.exec()

