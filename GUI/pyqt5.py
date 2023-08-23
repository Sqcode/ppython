import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QDesktopWidget
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from functools import partial

class CenteredWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.btn()

    def initUI(self):
        self.setWindowTitle('Window')
        self.setGeometry(0, 0, 300, 200)  # Set initial size

        # 调用父类中的menuBar，从而对菜单栏进行操作
        menu = self.menuBar()
        # 如果是Mac的话，菜单栏不会在Window中显示而是屏幕顶部系统菜单栏位置
        # 下面这一行代码使得Mac也按照Windows的那种方式在Window中显示Menu
        menu.setNativeMenuBar(False)

        file_menu = menu.addMenu("文件")
        file_menu.addAction("新建")
        file_menu.addAction("打开")
        file_menu.addAction("保存")

        edit_menu = menu.addMenu("编辑")
        edit_menu.addAction("复制")
        edit_menu.addAction("粘贴")
        edit_menu.addAction("剪切")

        # 设置中心内容显示
        #self.setCentralWidget(label)
        
        self.center()  # Center the window on the screen

    def center(self):
        # Get the screen's geometry
        screen_geometry = QDesktopWidget().screenGeometry()

        # Calculate the center point of the screen
        screen_center = screen_geometry.center()

        # Calculate the top-left position for the window to be centered
        window_position = self.frameGeometry()
        window_position.moveCenter(screen_center)

        # Move the window slightly upwards
        window_position.moveTop(window_position.top() - 100)  # Adjust the value as needed


        self.move(window_position.topLeft())

    def btn(self):
        btn = QPushButton('button', self)
        #btn.setGeometry(200, 200, 100, 30)
        btn.setParent(self)

        # Create a centered button outside the class
        btn.move((self.width() - btn.width()) // 2, (self.height() - btn.height()) // 2)

        # 将按钮被点击时触发的信号与我们定义的函数（方法）进行绑定
        # 注意：这里没有()，即写函数的名字，而不是名字()
        # btn.clicked.connect(self.click)

        # Create a function with the custom argument using functools.partial
        # partial_func = partial(click, arg=1)
        # btn.clicked.connect(partial_func)  # Connect button click event to the partial function

        # lambda offer extra arg
        btn.clicked.connect(lambda checked, arg=1: self.click(arg))  

    def click(self, arg):
        # Get cursor position relative to the window
        cursor = self.mapFromGlobal(self.cursor().pos())  
        print(f"Mouse clicked at position: ({cursor.x()}, {cursor.y()}), extra arg: {arg}")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:  # Check if left mouse button is clicked
            x = event.x()
            y = event.y()
            print(f"Mouse LeftButton clicked at position: ({x}, {y})")

def main():
    app = QApplication(sys.argv)
    mainWindow = CenteredWindow()
    mainWindow.show()
    sys.exit(app.exec_())

# def click(self, arg):
#     # cursor = self.mapFromGlobal(self.cursor().pos()) 
#     cursor_position = self.mapFromGlobal(self.button.mapToGlobal(self.button.pos()))
#     print(f"Mouse clicked at position: ({cursor_position.x()}, {cursor_position.y()}), arg: {arg}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CenteredWindow()
    # btn(window)

    window.show()
    sys.exit(app.exec_())

    # main()

