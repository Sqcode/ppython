import sys, os, logging, re, time
sys.path_importer_cache.clear()
logging.basicConfig(filename="log.log", level=logging.INFO, format="%(asctime)s [%(levelname)s] (%(module)s:%(lineno)d) - %(message)s")
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5 import uic
# from functools import partial
from oracle_long_conn import get_connection
# commom_directory = os.path.join(parent_directory, "common")
# sys.path.append(commom_directory)
# from log_handler import log_init
from compoment import PopupWindow, confirm
#-- -----------------------------------------------------------------------------------------------
from global_variables import fNumber, fUnitId, fNuit, fMaterialId
import spec as sp

# fNumber = None
# fUnitId = None
# fNuit = None
# fMaterialId = None

# from Ui_once import Ui_Form
# class CreatedWindow(QMainWindow, Ui_Form):
class CreatedWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        '''加载ui的方式'''
        # 加载设计的UI文件
        icon_path = os.path.join(os.path.dirname(__file__), "tool.ui")
        uic.loadUi(icon_path, self) 

        # 采用编译后的py文件 载入UI
        # self.setupUi(self)  # 使用编译后的 setupUi 方法
        # self.setWindowIcon(QIcon("E:\\Dev\\ppython\\Jodoll\\32tool.ico"))  # 替换为图标文件的路径

        icon_path = os.path.join(os.path.dirname(__file__), "32tool.ico")
        self.setWindowIcon(QIcon(icon_path))
        # self.setWindowIcon(QIcon("32tool.ico"))  # 替换为图标文件的路径

        # 连接数据库
        # conn = get_connection()

        self.btn.clicked.connect(self.updateUnit)  # 连接按钮的clicked信号与槽函数
        # self.getUnit.clicked.connect(get_material_unit)  # 连接按钮的clicked信号与槽函数
        '''使用partial_func传递参数'''
        # partial_func = partial(alert, arg='test')
        # self.alert.clicked.connect(partial_func)
        '''绑定`获取单位` 使用lambda传递参数'''
        self.getUnit.clicked.connect(lambda checked, arg=self : get_material_unit(arg))

        # 测试数据
        # self.units = [(10101, 'Pcs', 'Pcs'), (101659, '件', '件'), (101661, '条', '条'), (101662, '米', '米'), (101663, '千米', '千米')]
        # self.unitComboBox.clear()
        # for row in self.units:
        #     self.unitComboBox.addItem(row[2])

        # 点击下拉列表，触发对应事件
        #self.unitComboBox.currentIndexChanged.connect(lambda: self.unitComboBox(self.unitSelected.currentIndex()))  
        self.unitComboBox.currentIndexChanged.connect(self.unitSelected)
        # 搜索查询
        self.unitComboBox.lineEdit().textEdited.connect(self.filterComboBox)
        # 物料编码
        # self.fnumberText.lineEdit().textEdited.connect(self.filterComboBox)
        
        # 初始化 单位值
        # initialize_units_box(self)
        # get_material_unit(self)

        # -- 页签2 -----------------------------------------------------------------------------------------------

        # 单据类型 测试数据
        self.billsTypeList = [(1, '采购订单', 'T_PUR_POORDER', 'T_PUR_POORDERENTRY'), (2, '收料通知单', 'T_PUR_RECEIVE', 'T_PUR_RECEIVEENTRY'), (3, '销售订单', 'T_SAL_ORDER', 'T_SAL_ORDERENTRY'), (4, '委外订单', 'T_SUB_REQORDER', 'T_SUB_REQORDERENTRY')]        # self.unitComboBox.clear()
        for row in self.billsTypeList:
            self.billsTypeComboBox.addItem(row[1])
        
        self.materialsList = []
        '''绑定`获取明细` 使用lambda传递参数'''
        self.getBillsBtn.clicked.connect(lambda checked, arg=self : get_materials_box(arg))
        self.materialsComboBox.currentIndexChanged.connect(self.materialSelected)


        # 刷新尺码
        self.resetBtn.clicked.connect(lambda checked, arg=self : reset(arg))
        self.updateBtn.clicked.connect(lambda checked, arg=self : update_spec(arg))


        # -- 页签1 -----------------------------------------------------------------------------------------------

    '''页签2'''
    def updateUnit(self):
        global fUnitId
        # unitIndex = self.unitComboBox.currentIndex()
        if fUnitId is None:
           PopupWindow(self, 'e', "错误", "请正确选择要更新的单位!").exec_()
           return
        
        # 查询下物料信息
        fMaterialId = get_material_unit(self)
        if fMaterialId is not None:
            update_material_unit(fMaterialId)

        # print(f'fNumber: {fNumber} ， current select {unitIndex} the item : {self.unitComboBox.itemText(unitIndex)}')

    def unitSelected(self, index):
        global fUnitId, fNuit
        fUnitId = None
        fNuit = self.unitComboBox.itemText(index)
        for index in range(len(self.units)):
            item_text = self.units[index][2]
            if fNuit.lower() == item_text.lower():
                # print(f"Matched index : {index} , item: {item_text}")
                # self.unitComboBox.setCurrentIndex(index)
                fUnitId = self.units[index][0]
                # print(f'current select {index} , the item : {fNuit}, fUnitId: {fUnitId}')
                break

        # QMessageBox.information(self, "Tip", f'current select the {self.units[index][2]}')

    # 输入过滤搜索
    def filterComboBox(self, text):
        # print("User input:", text)
        global fUnitId, fNuit
        fUnitId = None

        self.unitComboBox.clear()  # 清空下拉列表
        pattern = re.compile(text, re.IGNORECASE)
        # self.unitComboBox.setCurrentIndex(0)
        for index in range(len(self.units)):
            item_text = self.units[index][2]
            if re.search(pattern, item_text):
                # print(f"Matched {index} item: {item_text}")
                self.unitComboBox.addItem(item_text)  # 添加匹配的选项
            # 如果完全相等 设置为当前index，否则0
            if text.lower() == item_text.lower():
                self.unitComboBox.setCurrentIndex(index)
                fUnitId = self.units[index][0]
                fNuit = text
                # print(f"Pretty Matched index : {index} , item: {fNuit}, fUnitId: {fUnitId}")
    '''页签1'''

    def materialSelected(self, index):
        global fNumber, fMaterialId
        fNumber = None
        fMaterialId = None
        fNumber = self.materialsComboBox.itemText(index)

        materialsList = self.materialsList
        # 遍历列表中的元素（每个元素都是一个包含字典的列表）
        for item_list in materialsList:
            # 遍历包含字典的列表中的每个字典
            for item_dict in item_list:
                item_text = item_dict['FNumber'] # 访问字典的键 'FNumber'
                # item_text = list(self.materialsList)[0][1]['FNumber']

                if fNumber == item_text:
                    # print(f"Matched index : {index} , item: {item_text}")
                    fMaterialId = item_dict['FMaterialId']
                    fName = item_dict['FName']
                    fDemal = item_dict['FDemal']
                    self.AuxCSText.setPlainText(fDemal)
                    # print(f'current select {index} , the item : {fNumber}:{fName}, fDemal: {fDemal}')
                    break
        # 获取是否开启
        aux_auc = sp.get_material_aux(fNumber)
        self.AuxS.setChecked(True if aux_auc.get(100001) else False)
        self.AuxC.setChecked(True if aux_auc.get(100002) else False)

        chk = self.AuxC.isChecked()
        self.resetBtn.setEnabled(True if chk else False)

    '''关闭'''
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
        conn = get_connection()
        try:
            # 关闭数据库连接的操作
            if conn is not None:
                conn.close()
        except Exception as e:
            logging.error(f'Error closing database connections')

# 单位下拉框赋值
def initialize_units_box(self):
    self.units = get_units()
    if len(self.units) > 0:
        self.unitComboBox.clear()
        for row in self.units:
            self.unitComboBox.addItem(row[2])

# 查询数据库获取单位
def get_units():
    conn = get_connection()
    try:
        sql = f'''
        SELECT TBU.FUNITID, TBU.FNUMBER, TBUL.FNAME 
        FROM KINGDEE00.T_BD_UNIT TBU LEFT JOIN KINGDEE00.T_BD_UNIT_L TBUL ON TBUL.FUNITID = TBU.FUNITID 
        WHERE TBU.FFORBIDSTATUS = 'A' AND TBU.FDOCUMENTSTATUS = 'C'
        '''
        result = conn.execute_query(sql)
        # logging.info(f'sql: {sql}, result: {result}')
        return result
    except Exception as e:
        logging.error(f"get_units Error ")

# 获取一下物料信息，再更新
def get_material_unit(self):
    global fNumber
    fNumber = self.fnumberText.text()
    conn = get_connection()

    if len(fNumber) == 0:
        PopupWindow(self, 'e', "错误", "请填写物料编码!").exec_()
        return
    
    # 简单查询下基本单位
    sql = '''
        SELECT FMATERIALID, FBASEUNITID 
        FROM KINGDEE00.T_BD_MaterialBase 
        WHERE FMATERIALID IN (SELECT TBM.FMATERIALID FROM KINGDEE00.T_BD_MATERIAL TBM WHERE TBM.FNUMBER = :FNUMBER)
        '''
    params = {"FNUMBER": fNumber}
    result = conn.execute_query(sql, params)

    if len(result) == 0:
        PopupWindow(self, 'e', "错误", "查询不到物料信息，请确认!").exec_()
        return
    
    unit_id = result[0][1]
    # pattern = re.compile(result[0][1], re.IGNORECASE)
    for index in range(len(self.units)):
        item_id = self.units[index][0]
        if unit_id == item_id:
            self.currentUnitText.setText(self.units[index][2])
    # 更新
    return result[0][0]
    # update_material_unit(self, result[0][0])

# 更新单位
def update_material_unit(fMaterialId):
    global fUnitId, fNumber, fNuit, window

    conn = get_connection()
    if fMaterialId is not None:
        update_query1 = f"UPDATE KINGDEE00.T_BD_MaterialBase SET FBASEUNITID = {fUnitId},  FWEIGHTUNITID = {fUnitId}, FVOLUMEUNITID = {fUnitId} WHERE FMATERIALID IN ({fMaterialId})"
        update_query2 = f"UPDATE KINGDEE00.T_BD_MaterialStock SET FSTOREUNITID = {fUnitId} WHERE FMATERIALID IN ({fMaterialId})"
        update_query3 = f"UPDATE KINGDEE00.T_BD_MaterialSale SET FSALEUNITID = {fUnitId}, FSALEPRICEUNITID = {fUnitId} WHERE FMATERIALID IN ({fMaterialId})"
        update_query4 = f"UPDATE KINGDEE00.T_BD_MaterialPurchase SET FPURCHASEUNITID = {fUnitId}, FPURCHASEPRICEUNITID = {fUnitId} WHERE FMATERIALID IN ({fMaterialId})"
        update_query5 = f"UPDATE KINGDEE00.T_BD_MaterialProduce SET FPRODUCEUNITID = {fUnitId}, FBOMUNITID = {fUnitId}, FMINISSUEUNITID = {fUnitId} WHERE FMATERIALID IN ({fMaterialId})"
        update_query6 = f"UPDATE KINGDEE00.T_BD_MaterialSubcon SET FSUBCONUNITID = {fUnitId}, FSUBCONPRICEUNITID = {fUnitId} WHERE FMATERIALID IN ({fMaterialId})"

        update_queries = [update_query1, update_query2, update_query3, update_query4, update_query5, update_query6]
        # 更新
        conn.execute_transaction(update_queries)

        str = f"物料：{fNumber}，单位【{fNuit}】更新成功!"
        logging.info(str)
        PopupWindow(window, 'i', "提示：", str).exec_()

# 明细下拉赋值
def get_materials_box(self):

    global fBillNo
    fBillNo = self.billNoText.text()

    if len(fBillNo) == 0:
        PopupWindow('e', "错误", "请填写单据编号!", self).exec_()
        return
    
    materialsListDict = sp.get_bills(fBillNo)
    self.materialsList = list(materialsListDict.values())

    if len(self.materialsList) > 0:
        self.materialsComboBox.clear()
        for row in self.materialsList:
            for dictionary in row:
                FNumber = dictionary['FNumber']
                # FName = dictionary['FName']
                # FDemal = dictionary['FDemal']
                # print(FNumber, FName, FDemal)
                self.materialsComboBox.addItem(FNumber)

success = demal = demalTag = None

# 刷新尺码
def reset(self):
    global success, demal, demalTag

    arr = sp.get_bills_specString(fBillNo, fNumber)
    # 延迟一下 数据库查询
    time.sleep(1)

    specList, specQtyList = sp.split_spec(arr)
    # print('specQtyList', specQtyList)

    commonPrefix, AuxCSList = sp.common_prefix(specQtyList)
    # print(commonPrefix, AuxCSList)

    # AuxS：尺码,AuxC：款型
    AuxC, AuxS, AuxCSQty = sp.get_AuxC(AuxCSList)
    # print(AuxCSQty)

    # 重设值
    # print(f'AuxC: {AuxC}\nAuxS: {AuxS}\nAuxCSQty: {AuxCSQty}')

    # 检查,一维内的尺码 是否在物料的可选尺码内
    flag, AuxCS = sp.check_in_specList(fNumber, commonPrefix, AuxS)
    # print(specTag)

    # aux_auc = sp.get_material_aux(fNumber)
    # self.AuxS.setChecked(lambda: True if aux_auc.get(100001) else False)  # 使用 lambda 设置勾选状态
    # self.AuxC.setChecked(lambda: True if aux_auc.get(100002) else False)

    # self.checkbox.isChecked():
    
    if (flag):
    #     # JSON串,数量 拼接进去
        success, demal, demalTag = sp.reset_spec(commonPrefix, None, AuxCS, AuxCSQty)
        self.newAuxCSText.setPlainText(demal)

    #     self.updateBtn.setEnabled(lambda: True if success else False)
        # self.AuxC.setChecked(True if aux_auc.get(100002) else False)
        if (success):
            self.updateBtn.setEnabled(True if success else False)
        # else:
        #     self.updateBtn.setEnabled(False)

    
# 更新
def update_spec(self):
    global success, demal, demalTag
    if (success):
        sp.update_spec(demal, demalTag)
        self.updateBtn.setEnabled(False)

    

def main():
    # 记录程序启动日志
    logging.info('Executable started with command: %s', ' '.join(sys.argv))
    # 你的程序主体部分
    global window
    app = QApplication(sys.argv)
    window = CreatedWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    print('开始')

    main()
    # input("Press Enter to exit...")