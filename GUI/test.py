import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QVBoxLayout, QWidget, QLineEdit

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Searchable ComboBox Example")
        self.setGeometry(100, 100, 400, 300)

        self.combo_box = QComboBox(self)
        self.combo_box.setEditable(True)  # 设置为可编辑状态
        self.combo_box.addItem("Option 1")
        self.combo_box.addItem("Option 2")
        self.combo_box.addItem("Option 3")

        self.search_line_edit = QLineEdit(self)
        self.search_line_edit.setPlaceholderText("Search...")  # 设置占位文本

        self.search_line_edit.textChanged.connect(self.filterComboBox)  # 连接信号和槽
        self.search_line_edit.editingFinished.connect(self.clearFocus)  # 连接失去焦点槽

        layout = QVBoxLayout()
        layout.addWidget(self.search_line_edit)
        layout.addWidget(self.combo_box)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def filterComboBox(self, text):
        self.combo_box.clear()  # 清空下拉列表

        for item in ["Option 1", "Option 2", "Option 3"]:
            if text.lower() in item.lower():
                self.combo_box.addItem(item)  # 添加匹配的选项

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
