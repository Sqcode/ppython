import sys
import re
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Fuzzy Matching ComboBox Example")
        self.setGeometry(100, 100, 400, 300)

        self.combo_box = QComboBox(self)
        self.combo_box.setEditable(True)  # 设置为可编辑状态
        self.combo_box.addItem("Pcs")
        self.combo_box.addItem("件")
        self.combo_box.addItem("条")
        self.combo_box.addItem("米")
        self.combo_box.addItem("千米")

        layout = QVBoxLayout()
        layout.addWidget(self.combo_box)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.combo_box.lineEdit().textEdited.connect(self.onComboBoxEdited)

    def onComboBoxEdited(self, text):
        pattern = re.compile(text, re.IGNORECASE)
        print("User input:", text)

        for index in range(self.combo_box.count()):
            item_text = self.combo_box.itemText(index)
            if re.search(pattern, item_text):
                print(f"Matched {index} item: {item_text}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
