import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("QLineEdit示例")
        self.setGeometry(100, 100, 400, 300)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # 创建两个QLineEdit
        self.textLineEdit1 = QLineEdit(self)
        self.textLineEdit1.setPlaceholderText("文本框1")
        layout.addWidget(self.textLineEdit1)

        self.textLineEdit2 = QLineEdit(self)
        self.textLineEdit2.setPlaceholderText("文本框2")
        layout.addWidget(self.textLineEdit2)

        central_widget.setLayout(layout)

        # 连接焦点事件
        self.textLineEdit1.installEventFilter(self)
        self.textLineEdit2.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == event.FocusIn:
            # 如果焦点进入一个组件，清除其他组件的焦点
            if obj == self.textLineEdit1:
                self.textLineEdit2.clearFocus()
            elif obj == self.textLineEdit2:
                self.textLineEdit1.clearFocus()
        return super().eventFilter(obj, event)

    def mousePressEvent(self, event):
        # 获取当前拥有焦点的部件
        current_focus_widget = QApplication.focusWidget()

        # 如果有焦点的部件，并且点击的部件不是当前焦点的部件，清除焦点
        if current_focus_widget and current_focus_widget != self.textLineEdit1 and current_focus_widget != self.textLineEdit2:
            current_focus_widget.clearFocus()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
