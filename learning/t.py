import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QProgressBar
from PyQt5.QtCore import QThread, pyqtSignal

class WaitingThread(QThread):
    progress = pyqtSignal(int)

    def run(self):
        for i in range(101):
            self.progress.emit(i)
            self.msleep(50)  # 模拟耗时操作

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.button = QPushButton('Start')
        self.progress_bar = QProgressBar()

        self.layout.addWidget(self.button)
        self.layout.addWidget(self.progress_bar)

        self.button.clicked.connect(self.startWaiting)
        self.progress_bar.setValue(0)

        self.setLayout(self.layout)

        self.waiting_thread = WaitingThread()
        self.waiting_thread.progress.connect(self.updateProgressBar)

    def startWaiting(self):
        self.button.setDisabled(True)  # 禁用按钮
        self.waiting_thread.start()

    def updateProgressBar(self, value):
        self.progress_bar.setValue(value)
        if value == 100:
            self.button.setDisabled(False)  # 启用按钮

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
