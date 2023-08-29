
import sys, os, logging, re
logging.basicConfig(filename="log.txt",level=logging.INFO,format= "%(asctime)s %(levelname)s -- %(message)s")
logging.basicConfig(filename="log.txt",level=logging.DEBUG,format= "%(asctime)s %(levelname)s -- %(message)s")
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import uic
from functools import partial

__dir__ = os.path.dirname(os.path.abspath(__file__))
# 将多个路径添加到 sys.path
parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_directory)
sys.path.append(os.path.abspath(os.path.join(__dir__, './QtDesigner')))
# from Ui_once import Ui_Form
database_directory = os.path.join(parent_directory, "database")
sys.path.append(database_directory)
import cx_Oracle
from oracle_long_conn import OracleDatabase, conn
# commom_directory = os.path.join(parent_directory, "common")
# sys.path.append(commom_directory)
# from log_handler import log_init
from compoment import PopupWindow, confirm
#-- -----------------------------------------------------------------------------------------------
# class CreatedWindow(QMainWindow, Ui_Form):
class CreatedWindow(QMainWindow):
    # 初始化一下db为None，后者有判断是否有连接
    db = None

    def __init__(self):
        super().__init__()
        '''加载ui的方式'''
        # 加载设计的UI文件
        uic.loadUi("GUI\QtDesigner\once.ui", self) 
        # 采用编译后的py文件 载入UI
        # self.setupUi(self)  # 使用编译后的 setupUi 方法

        # self.btn.clicked.connect(self.btnClicked)  # 连接按钮的clicked信号与槽函数
        # self.alert.clicked.connect(alert)  # 连接按钮的clicked信号与槽函数
        '''使用partial_func传递参数'''
        # partial_func = partial(alert, arg='test')
        # self.alert.clicked.connect(partial_func)
        '''使用lambda传递参数'''
        self.alert.clicked.connect(lambda checked, arg=1: self.showMsg(arg))

        # 测试数据
        self.units = [(10101, 'Pcs', 'Pcs'), (101659, '件', '件'), (101661, '条', '条'), (101662, '米', '米'), (101663, '千米', '千米')]
        self.unit_comboBox.clear()
        for row in self.units:
            self.unit_comboBox.addItem(row[2])

        # 点击下拉列表，触发对应事件
        #self.unit_comboBox.currentIndexChanged.connect(lambda: self.unit_comboBox(self.unitSelected.currentIndex()))  
        self.unit_comboBox.currentIndexChanged.connect(self.unitSelected)

        # 搜索查询
        self.unit_comboBox.lineEdit().textEdited.connect(self.filterComboBox)

        # 连接数据库，并初始化单位
        # self.db = conn_oracle(self)

    # def btnClicked(self):
    #     # 在按钮被点击时执行的操作
    #     print("button clicked !")
    #     PopupWindow('e', "Popup Title", "This is a sample popup message.").exec_()

    def showMsg(self, arg):
        message = f"Button clicked! Argument: {arg}"
        QMessageBox.information(self, "Tip", message)

    def unitSelected(self, index):
            # [index][2]
        print(f'current select {index} the item : {self.unit_comboBox.itemText(index)}')
        # QMessageBox.information(self, "Tip", f'current select the {self.units[index][2]}')

    # 输入过滤搜索
    def filterComboBox(self, text):
        # print("User input:", text)
        self.unit_comboBox.clear()  # 清空下拉列表
        pattern = re.compile(text, re.IGNORECASE)
        
        for index in range(len(self.units)):
            item_text = self.units[index][2]
            if re.search(pattern, item_text):
                # print(f"Matched {index} item: {item_text}")
                self.unit_comboBox.addItem(item_text)  # 添加匹配的选项
                # 如果完全相等 设置为当前index，否则0
                if text.lower() == item_text.lower():
                    print(f"Matched index : {index} , item: {item_text}")
                    self.unit_comboBox.setCurrentIndex(index)
                else:
                    self.unit_comboBox.setCurrentIndex(0)

    def closeEvent(self, event):
        # if confirm('确认关闭', '您确定要关闭窗口吗？'):
        #     self.closeWindow()
        #     # self.close()
        # else:
        #     event.ignore()
        self.closeWindow()

    def closeWindow(self):
        # 在窗口关闭时关闭数据库连接等操作
        self.closeDatabaseConnections()
        self.close()

    def closeDatabaseConnections(self):
        try:
            # 关闭数据库连接的操作
            if self.db is not None:
                self.db.close()
        except Exception as e:
            logging.error(f'Error closing database connections: {e}')

def conn_oracle(window):
    db = OracleDatabase(conn())
    # 初始化 单位值
    initialize_units_box(db, window)

def initialize_units_box(db, window):
    window.units = get_units(db)
    if len(window.units) > 0:
        window.unit_comboBox.clear()
        for row in window.units:
            window.unit_comboBox.addItem(row[2])

# def filterComboBox(self, text):
#     self.combo_box.clear()  # 清空下拉列表

#     for item in ["Option 1", "Option 2", "Option 3"]:
#         if text.lower() in item.lower():
#             self.combo_box.addItem(item)  # 添加匹配的选项     

def get_units(db):
    try:
        # units = ["Pcs", "条", "件"]
        # # 构建 IN 条件字符串
        # in_units = ', '.join(':' + str(i + 1) for i in range(len(units)))
        # query = f'''
        # SELECT TBU.FUNITID, TBU.FNUMBER, TBUL.FNAME 
        # FROM KINGDEE00.T_BD_UNIT TBU LEFT JOIN KINGDEE00.T_BD_UNIT_L TBUL ON TBUL.FUNITID = TBU.FUNITID 
        # WHERE TBU.FFORBIDSTATUS = 'A' AND TBU.FDOCUMENTSTATUS = 'C' AND TBUL.FNAME IN ({in_units})
        # '''
        query = f'''
        SELECT TBU.FUNITID, TBU.FNUMBER, TBUL.FNAME 
        FROM KINGDEE00.T_BD_UNIT TBU LEFT JOIN KINGDEE00.T_BD_UNIT_L TBUL ON TBUL.FUNITID = TBU.FUNITID 
        WHERE TBU.FFORBIDSTATUS = 'A' AND TBU.FDOCUMENTSTATUS = 'C'
        '''
        result = db.execute_query(query)
        # logging.info(f'query: {query}, result: {result}')

        # print(query, result)
        return result
    except cx_Oracle.DatabaseError as e:
        print("Error:", e)
    finally:
        db.close()  # 在这里调用 close() 方法关闭连接池

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CreatedWindow()

    window.show()
    app.exec()

