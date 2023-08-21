import threading
import time

class MyThread(threading.Thread):
    def __init__(self, func):
        super().__init__()
        self._stop_event = threading.Event()
        self.func = func

    def stop(self):
        self._stop_event.set()

    def run(self):
        while not self._stop_event.is_set():
            self.func()
            time.sleep(1)


    
# 创建并启动线程
thread = MyThread()
thread.start()

# 主线程等待一段时间后停止子线程
time.sleep(5)
thread.stop()
thread.join()  # 等待线程结束
print("Main thread stopped.")



class MyThread(threading.Thread):
    def __init__(self, custom_statement):
        super().__init__()
        self.custom_statement = custom_statement

    def run(self):
        print("Custom statement inside run method:", self.custom_statement)

# 创建并启动线程，传入自定义语句
custom_statement = "Hello, from custom statement!"
thread = MyThread(custom_statement)
thread.start()

# 等待线程结束
thread.join()

print("Main thread stopped.")
