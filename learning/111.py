import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QProgressDialog, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QThread

from PyQt5.QtCore import pyqtSignal

class WorkerThread(QThread):
    update_progress = pyqtSignal(int)
    finished = pyqtSignal()

    def run(self):
        # 模拟耗时任务
        for i in range(1, 101):
            time.sleep(0.1)  # 模拟耗时操作
            self.update_progress.emit(i)  # 发送进度信号
        self.finished.emit()

        
class ProgressDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("等待进度对话框")
        
        self.progress_dialog = QProgressDialog(self)
        self.progress_dialog.setLabelText("请等待...")
        self.progress_dialog.setRange(0, 100)
        self.progress_dialog.setModal(True)  # 设置为模态对话框
        
        layout = QVBoxLayout()
        layout.addWidget(self.progress_dialog)
        self.setLayout(layout)
        
    def set_progress(self, value):
        self.progress_dialog.setValue(value)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("主窗口")
        
        self.button = QPushButton("执行任务", self)
        self.button.clicked.connect(self.execute_task)
        
    def execute_task(self):
        self.progress_dialog = ProgressDialog(self)
        self.progress_dialog.show()
        
        self.worker_thread = WorkerThread()
        self.worker_thread.update_progress.connect(self.progress_dialog.set_progress)
        self.worker_thread.finished.connect(self.close_progress_dialog)
        
        self.worker_thread.start()
        
    def close_progress_dialog(self):
        self.progress_dialog.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
