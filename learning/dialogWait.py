import sys, time, random
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from progress_dialog import ProgressDialog
# from worker_thread import WorkerThread

from PyQt5.QtCore import QThread, pyqtSignal, QTimer

# class WorkerThread(QThread):
#     update_progress = pyqtSignal(int)
#     finished = pyqtSignal()

#     def run(self):
#         # 在这里执行你的任务
#         for i in range(1, 101):
#             self.update_progress.emit(i)  # 发送进度信号
#         self.finished.emit()  # 发送任务完成信号

# class WorkerThread(QThread):
#     update_progress = pyqtSignal(int)
#     finished = pyqtSignal()

#     def run(self):
#         # 模拟耗时任务
#         current_progress = 0
#         for i in range(1, 101):
#             time.sleep(0.1)  # 模拟耗时操作
#             increment = random.randint(1, 5)  # 生成随机增量
#             current_progress += increment  # 更新当前进度
#             self.update_progress.emit(current_progress)  # 发送更新后的进度信号

#         self.finished.emit()


class WorkerThread(QThread):
    update_progress = pyqtSignal(int)
    finished = pyqtSignal()

    def run(self):
        current_progress = 0
        while current_progress < 100:
            increment = random.randint(1, 5)
            current_progress += increment
            if current_progress > 100:
                current_progress = 100  # 确保不超过100
            self.update_progress.emit(current_progress)
            time.sleep(0.1)  # 模拟耗时操作
        self.finished.emit()

        # 在这里执行其他任务，例如模拟一个耗时的操作
        total_sleep_time = 3  # 总共休眠3秒
        current_sleep_time = 0
        while current_sleep_time < total_sleep_time:
            time.sleep(0.1)  # 每次休眠0.1秒
            current_sleep_time += 0.1
            # 计算休眠期间的进度
            sleep_progress = int((current_sleep_time / total_sleep_time) * 100)
            self.update_progress.emit(sleep_progress)

        self.finished.emit()

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
