import tkinter as tk
from tkinter import messagebox as msg
import threading, time, datetime


def init_window():
    window = tk.Tk()
    window.title('窗口')
    window.geometry("300x200+750+280")  # (宽度x高度)+(x轴+y轴)
    return window

def click_btn(e):
    msg.showinfo('提示: ', 'success')

def create_btn(window):
        # btn = tk.Button(window)
    # btn['text'] = '按钮'
    # # btn.pack()
    # btn.grid()
    # print(btn.grid_info())
    # btn.bind("<Button-1>", click_btn)

    # 按钮1
    btn1 = tk.Button(window)
    btn1["text"] = "按钮1"
    btn1.grid(column=0, columnspan=2)

    # 按钮2
    btn2 = tk.Button(window)
    btn2["text"] = "按钮2"
    btn2.grid(column=1, columnspan=1)

class GUI:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('演示窗口')
        self.root.geometry("350x200+700+150")
        self.buttons()

    def buttons(self):
        # 界面编写位置
        self.Button_Start = tk.Button(self.root, text="开始", command=self.start)
        self.Button_Start.grid(row=0, column=0)

        self.warp = tk.Text(self.root, width=50, height=10)
        self.warp.grid(row=1, column=0, columnspan=4)

        # place(relx=0.2, x=100, y=20, relwidth=0.2, relheight=0.5)

        self.Button1 = tk.Button(self.root, text="暂停", command=self.pause)
        self.Button1.grid(row=0, column=1)

        self.Button2 = tk.Button(self.root, text="继续", command=self.conti)
        self.Button2.grid(row=0, column=2)

        self.Button3 = tk.Button(self.root, text="停止", command=self.stop)
        self.Button3.grid(row=0, column=3)

    def count_down(self):
        while True:
            # current_time = time.strftime('%Y-%m-%d %H:%M:%S %p')
            current_thread = threading.current_thread()
            current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            thread_info = str('%s, %s' % (current_thread.getName(), current_time))
            print(thread_info)

            self.warp.insert(1.0, thread_info +'\n')
            time.sleep(1)
            self.event.wait()

    def start(self):

        self.T1 = MyThread(func=self.count_down, daemon=True)  # 子线程
        self.event = self.T1.event
        # self.T1 = threading.Thread(name='t1', target=self.event, daemon=True)  # 子线程
        self.T1.start()  # 启动
        self.event.set()

    def pause(self):
        self.event.clear()
        # self.warp.insert(1.0, '暂停'+'\n')

    def conti(self):
        self.event.set()
        # self.warp.insert(1.0, '继续'+'\n')

    def stop(self):
        self.T1.stop()  # 停止
        # self.T1.join()  # 等待线程结束

class MyThread(threading.Thread):
    def __init__(self, func, **kwargs):
        super().__init__(**kwargs)
        self.event = threading.Event()
        self.func = func

    # def start(self):
    #     self.event.set()
    def stop(self):
        self.event.clear()

    def run(self):
        while not self.event.is_set():
            self.func()
        print("Thread stopped gracefully.")


if __name__ == '__main__':
    # -- 2023-08-21 星期一 ↓
    # window = init_window()
    # window.mainloop()

    win = GUI ()
    win.root.mainloop()

