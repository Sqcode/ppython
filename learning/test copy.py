import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon

class CreatedWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 设置窗口标题
        self.setWindowTitle("My Window")

        # 设置窗口图标
        self.setWindowIcon(QIcon("E:\Dev\ppython\Jodoll\64tool.ico"))  # 替换为图标文件的路径

        # 其他窗口内容设置
        # ...

def main():
    app = QApplication(sys.argv)
    window = CreatedWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
