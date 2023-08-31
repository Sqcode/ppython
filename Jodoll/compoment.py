import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox

class PopupWindow(QMessageBox):
    def __init__(self, window, icon_type, title, message):
        super().__init__(window)
        self.setWindowTitle(title)
        self.setText(message)

        if icon_type == "e":
            self.setIcon(QMessageBox.Critical)
        elif icon_type == "w":
            self.setIcon(QMessageBox.Warning)
        elif icon_type == "i":
            self.setIcon(QMessageBox.Information)
        elif icon_type == "q":
            self.setIcon(QMessageBox.Question)
        else:
            self.setIcon(QMessageBox.NoIcon)

def confirm(title, message, yes_text='确认', no_text='取消'):
        confirm_dialog = QMessageBox()
        confirm_dialog.setWindowTitle(title)
        confirm_dialog.setText(message)
        confirm_dialog.setIcon(QMessageBox.Question)
        confirm_dialog.addButton(yes_text, QMessageBox.YesRole)
        confirm_dialog.addButton(no_text, QMessageBox.NoRole)
        reply = confirm_dialog.exec_()
        # return reply == QMessageBox.Yes
        clicked_button = confirm_dialog.clickedButton()
        return clicked_button.text() == yes_text

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.initUI()

#     def initUI(self):
#         self.setWindowTitle("Custom Close Event Example")
#         self.setGeometry(100, 100, 400, 300)

#         self.button = QPushButton('Button', self)
#         self.button.clicked.connect(self.show_confirm)

#     def show_confirm(self):
#         confirmed = confirm('自定义确认操作', '您确定要执行操作吗？', '执行', '取消')
#         if confirmed:
#             print("执行操作")
#         else:
#             print("取消操作")

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     mainWindow = MainWindow()
#     mainWindow.show()
#     sys.exit(app.exec_())
