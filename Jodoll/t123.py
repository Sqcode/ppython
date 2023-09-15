import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QVBoxLayout, QWidget
from mulComboBox import CheckableComboBox

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("主窗口")
        self.setGeometry(100, 100, 400, 300)

        # 创建一个 QWidget 作为中心部件
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # 创建一个布局管理器，例如 QVBoxLayout
        layout = QVBoxLayout()

        # 创建 CheckableComboBox 实例
        comboBox1 = CheckableComboBox()
        comunes = ['Ameglia', 'Arcola', 'Bagnone', 'Bolano', 'Carrara']
        comboBox1.addItems(comunes)
        comboBox1.setFixedSize(140, 30)

        # 将 comboBox1 添加到布局中
        layout.addWidget(comboBox1)

        # 设置布局为中心部件的布局
        central_widget.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
