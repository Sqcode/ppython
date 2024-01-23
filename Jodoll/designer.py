import sys, os, logging, re, time, datetime
sys.path_importer_cache.clear()
logging.basicConfig(filename="log.log", level=logging.INFO, format="%(asctime)s [%(levelname)s] (%(module)s:%(lineno)d) - %(message)s")
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox , QComboBox
from PyQt5.QtGui import QIcon
from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import Qt
# from functools import partial
from oracle_long_conn import get_connection
# commom_directory = os.path.join(parent_directory, "common")
# sys.path.append(commom_directory)
# from log_handler import log_init
from compoment import PopupWindow, confirm
#-- -----------------------------------------------------------------------------------------------
# from global_variables import fName, fNumber, fUnitId, fNuit, fMaterialId, table, tableEntry
import spec as sp
from mulComboBox import CheckableComboBox

fNumber = None
fUnitId = None
fNuit = None
fMaterialId = None
table = 'T_PUR_POORDER'
tableEntry = 'T_PUR_POORDERENTRY'
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

        self.units =[]
        # 连接标签切换事件
        self.tabWidget.currentChanged.connect(self.tab_changed)
    
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
        
        # get_material_unit(self)

        # -- 页签2 -----------------------------------------------------------------------------------------------

        # 单据类型 测试数据
        # self.billsTypeList = [(1, '采购订单', 'T_PUR_POORDER', 'T_PUR_POORDERENTRY'), (2, '收料通知单', 'T_PUR_RECEIVE', 'T_PUR_RECEIVEENTRY'), (3, '销售订单', 'T_SAL_ORDER', 'T_SAL_ORDERENTRY'), (4, '委外订单', 'T_SUB_REQORDER', 'T_SUB_REQORDERENTRY')]
        self.billsTypeList = [(1, '采购订单', 'T_PUR_POORDER', 'T_PUR_POORDERENTRY', 'FQTY', 'F_SCAG_FDEMAL', 'F_SCAG_FDEMAL_TAG'), (2, '采购申请单', 'T_PUR_REQUISITION', 'T_PUR_REQENTRY', 'FREQQTY', 'F_SCAG_FDEMAL', 'F_SCAG_FDEMAL_TAG'), (3, '收料通知单', 'T_PUR_RECEIVE', 'T_PUR_RECEIVEENTRY', 'FACTRECEIVEQTY', 'F_SCAG_FDEMAL', 'F_SCAG_FDEMAL_TAG'), (4, '销售订单', 'T_SAL_ORDER', 'T_SAL_ORDERENTRY', 'FQTY', 'F_SCAG_LARGETEXT', 'F_SCAG_LARGETEXT_TAG'), (5, '委外订单', 'T_SUB_REQORDER', 'T_SUB_REQORDERENTRY', 'FQTY', 'F_SCAG_FDEMAL', 'F_SCAG_FDEMAL_TAG')]
        for row in self.billsTypeList:
            self.billsTypeComboBox.addItem(row[1])
        
        self.billsTypeComboBox.currentIndexChanged.connect(self.billsTypeSelected)


        self.materialsList = []
        '''绑定`获取明细` 使用lambda传递参数'''
        self.getBillsBtn.clicked.connect(lambda checked, arg=self : get_materials_box(arg))
        # 单据编码 自填
        self.billNoText.editingFinished.connect(lambda arg=self : get_materials_box(arg))

        # 安装事件过滤器
        # self.installEventFilter(self)

        self.materialsComboBox.currentIndexChanged.connect(self.materialSelected)
        # 物料编码 自填
        self.materialsComboBox.lineEdit().textEdited.connect(self.get_material_aux)

        # 刷新尺码
        self.resetBtn.clicked.connect(lambda checked, arg=self : reset(arg))
        self.updateBtn.clicked.connect(lambda checked, arg=self : update_spec(arg))

        # 更新辅助属性
        # self.updateAuxcBtn.clicked.connect(lambda checked, arg=self : update_aux(arg))

        # self.AuxS.stateChanged.connect(self.checkbox_state_changed)
        self.AuxC.clicked.connect(lambda state: auxCChenkBox_changed(state, 100002, self))
        self.AuxS.clicked.connect(lambda state, checked=self.AuxS.isChecked(): auxCChenkBox_changed(state, 100001, self))

        # self.AuxC.stateChanged.connect(self.checkbox_state_changed)


        # -- 页签1 -----------------------------------------------------------------------------------------------

    def tab_changed(self, index):
        # 获取当前选定的标签的索引和文本
        current_tab_text = self.tabWidget.tabText(index)
        # 根据不同的标签触发不同的事件
        if current_tab_text == "尺码款型":
            # print("切换到标签页1, 尺码款型")
            pass
            # 在这里触发事件1的操作
        elif current_tab_text == "物料单位":
            # print("切换到标签页2, 物料单位")
            if len(self.units) <= 0:
                # 初始化 单位值
                initialize_units_box(self)
            
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
    # -- -----------------------------------------------------------------------------------------------
    '''页签1'''
    def billsTypeSelected(self, index):
        global table, tableEntry
        # print(table, tableEntry)
        name = self.billsTypeComboBox.itemText(index)
        for index in range(len(self.billsTypeList)):
            item_text = self.billsTypeList[index][1]
            if name == item_text:
                table = self.billsTypeList[index][2]
                tableEntry = self.billsTypeList[index][3]
                # print(f"Matched index : {index} , item: {table},{tableEntry}")
                break
        # print(table, tableEntry)

        # QMessageBox.information(self, "Tip", f'current select the {self.units[index][2]}')

    def materialSelected(self, index):
        global fNumber, fMaterialId, table, tableEntry
        fNumber = None
        fMaterialId = None
        fNumber = self.materialsComboBox.itemText(index).strip()

        if len(fNumber) > 0:
        # fNumber = fNumber[:fNumber.find("【")].strip()
            self.reserveAuxCSText.setPlainText('')
            self.newAuxCSText.setPlainText('')

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

                        break
            # 获取物料尺码款型信息
            self.get_material_aux(fNumber)
        
    def get_material_aux(self, text):
        global success, demal, demalTag, fNumber, AuxC
        fNumber = text
        # fNumber = text[:text.find("【")].strip()

        if (get_material(fNumber)):
            # 获取是否开启
            aux_auc = sp.get_material_aux(fNumber)
            self.AuxS.setChecked(True if aux_auc.get(100001) else False)
            self.AuxC.setChecked(True if aux_auc.get(100002) else False)
            # self.updateAuxcBtn.setEnabled(True)
            # 开放刷新按钮
            # chk = self.AuxC.isChecked()
            # self.resetBtn.setEnabled(True if chk else False)

            # 任意有一个 解锁？
            chk = self.AuxC.isChecked() or self.AuxS.isChecked()
            self.resetBtn.setEnabled(True if chk else False)

            # 获取款型
            AuxCS = sp.get_material_spec(fNumber)
            # auxc_list = AuxCS.get('AuxC', [])
            AuxC = sorted(AuxCS.get("AuxC", []), key=lambda x: x["AuxNumber"])
            # 如果存在'AuxC'且不为空列表，则获取第一个字典的'AuxNumber'值
            # aux_numbers = AuxC[0]['AuxNumber'] if AuxC else None
            # 使用列表推导式获取所有'AuxNumber'的值
            aux_numbers = [item['AuxNumber'] for item in AuxC]
            # print(AuxCS, AuxC, aux_numbers)
            
            comboBox = window.findChild(QComboBox, "mulAuxC")
            if comboBox and aux_numbers:
                comboBox.clear()  # 清除现有的选项

                # 添加新的选项
                comboBox.addItems(aux_numbers)
                selected_values = comboBox.currentData()
                # print("当前选择的值是:", selected_values)

                # 当前选择款型值
                current_AuxC(self.AuxC.isChecked())

            if self.AuxC.isChecked():
                comboBox.setVisible(True)
            else:
                comboBox.setVisible(False)
            
            self.AuxS.setEnabled(True)
            self.AuxC.setEnabled(True)
     
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

    # def eventFilter(self, obj, event):
    #     # 检查是否发生鼠标点击事件
    #     if event.type() == event.MouseButtonPress:
    #         # 如果点击位置是窗口或非文本框部分，则使文本框失去焦点
    #         if obj == self and event.target() != self.billNoText:
    #             self.billNoText.clearFocus()
    #     return super().eventFilter(obj, event)

    # 单据编号，获取焦点后，再失去焦点。则重新获取明细
    def mousePressEvent(self, event):
        #current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 获取当前拥有焦点的部件
        current_focus_widget = QApplication.focusWidget()
        # print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), current_focus_widget, current_focus_widget != self.billNoText, self.billNoText.hasFocus())
        # 如果有焦点的部件，清除焦点
        if current_focus_widget and self.billNoText.hasFocus():
            self.billNoText.clearFocus()
            self.billNoText.editingFinished.emit()
            # get_materials_box(self)

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

# 查询物料，是否存在
def get_material(fNumber):
    global fMaterailId, fName
    
    conn = get_connection()
    sql = '''
        SELECT TBM.FMATERIALID, TBM.FNUMBER, TBML.FNAME
        FROM KINGDEE00.T_BD_MATERIAL TBM
        LEFT JOIN KINGDEE00.T_BD_MATERIAL_L TBML ON TBML.FMATERIALID = TBM.FMATERIALID
        WHERE TBM.FNUMBER = :FNUMBER AND TBM.FUSEORGID = 1
        '''
    params = {"FNUMBER": fNumber}
    result = conn.execute_query(sql, params)

    if len(result) == 0:
        PopupWindow('e', "错误", '查询不到物料信息，请确认!', QApplication.activeWindow()).exec_()
        return False
    
    # print(result)
    # fNameText
    QApplication.activeWindow().fNameText.setText(result[0][2])

    return True

# 获取一下物料单位信息，再更新
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
        update_query7 = f"UPDATE KINGDEE00.T_STK_INVBAL SET FBASEUNITID = {fUnitId} WHERE FMATERIALID IN ({fMaterialId})"
        update_query8 = f"UPDATE KINGDEE00.T_STK_INVENTORY SET FBASEUNITID = {fUnitId}, FSTOCKUNITID = {fUnitId}, FSECUNITID = 0 WHERE FMATERIALID IN ({fMaterialId})"
        update_queries = [update_query1, update_query2, update_query3, update_query4, update_query5, update_query6, update_query7, update_query8]
        # 更新
        conn.execute_transaction(update_queries)

        str = f"物料：{fNumber}，单位【{fNuit}】更新成功!"
        logging.info(str)
        PopupWindow('i', "提示：", str, QApplication.activeWindow()).exec_()
        
# -- -----------------------------------------------------------------------------------------------
# 明细下拉赋值
def get_materials_box(self):
    global fBillNo, table, tableEntry
    fBillNo = self.billNoText.text().strip()

    self.reserveAuxCSText.setPlainText('')
    self.newAuxCSText.setPlainText('')

    if len(fBillNo) > 0:
        # PopupWindow('e', "错误", "请填写单据编号!", self).exec_()
        # return
        materialsListDict = sp.get_bills(fBillNo, table, tableEntry)
        self.materialsList = list(materialsListDict.values())

        if len(self.materialsList) > 0:
            self.materialsComboBox.clear()
            # self.updateAuxcBtn.setEnabled(True)
            for row in self.materialsList:

                for dictionary in row:
                    dictionary['changed'] = False
                    FNumber = dictionary['FNumber']
                    # FName = dictionary['FName']
                    # FDemal = dictionary['FDemal']
                    # print(FNumber, FName, FDemal)
                    self.materialsComboBox.addItem(FNumber)
        self.AuxS.setEnabled(True)
        self.AuxC.setEnabled(True)

        # print(self.materialsList)
    else: 
        PopupWindow('w', "提示", "未填写单据编号，不能获取单据明细!", self).exec_()
        return

success = demal = demalTag = None

# 获取当前选择的款型
def current_AuxC(checked):
    global AuxC

    combo_box = window.findChild(QComboBox, "mulAuxC")
    if combo_box and checked:
        selected_values = combo_box.currentData()
        # print("当前选择的值是:", selected_values)

        AuxCs = []  # 存储选中项的列表

        for item_data in AuxC:
            for index, combo_item in enumerate(selected_values):
                # print(combo_item, item_data['AuxNumber'])
                if combo_item == item_data['AuxNumber']:
                    selected_item = {'AuxId': item_data['AuxId'], 'AuxNumber': item_data['AuxNumber']}
                    AuxCs.append(selected_item)
                    # print(f"Found matching item at index {index}")
                    # break

        # if AuxCs:
        #     for selected_item in AuxCs:
        #         print(selected_item)
        # else:
        #     print("No items selected in AuxC")

        return AuxCs
    return []

# 获取当前选择的物料（在获取明细后的materialsList里） 取重新获取信息
def current_material(self):
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
                return item_dict
                # print(f'current select {index} , the item : {fNumber}:{fName}, fDemal: {fDemal}')
    
# 刷新尺码
def reset(self):
    global success, table, tableEntry, fBillNo, demal, demalTag, newSum
    fBillNo = self.billNoText.text()

    if len(fBillNo) == 0:
        PopupWindow('e', "错误", "请填写单据编号!", self).exec_()
        return
    
    # 获取物料的要拼接的款型
    AuxCs = current_AuxC(self.AuxC.isChecked())
    
    flag, arr = sp.get_bills_specString(fBillNo, fNumber, table, tableEntry)
    if flag:
        # 延迟一下 数据库查询
        time.sleep(1)
        specList, specQtyList = sp.split_spec(arr)
        # print('specQtyList', specQtyList)

        # 取前缀有问题先不能取
        # commonPrefix, AuxCSList, originSum = sp.common_prefix(specQtyList)

        # print(commonPrefix, AuxCSList)

        # AuxS：尺码,AuxC：款型
        # AuxC, AuxS, AuxCSQty = sp.get_AuxC(AuxCSList)
        # 只处理1个款型的数量
        Auxss, Auxcs, AuxCSQty = sp.reverse_cartesian_product(specList, specQtyList)

        self.reserveAuxCSText.setPlainText(f'尺码: {Auxss}\n款型: {Auxcs}\n数量: {AuxCSQty}')

        # print(AuxCSQty)
        # 重设值
        # print(f'AuxC: {AuxC}\nAuxS: {AuxS}\nAuxCSQty: {AuxCSQty}')

        # 检查,一维内的尺码 是否在物料的可选尺码内
        # flag, AuxCS = sp.check_in_specList(fNumber, AuxCs, commonPrefix, AuxS)
        flag, AuxCS = sp.check_in_specList(fNumber, Auxss)

        if (flag):
        #     # JSON串,数量 拼接进去
            success, demal, demalTag, newSum = sp.reset_spec(AuxCs, AuxCS, AuxCSQty)
            self.newAuxCSText.setPlainText(demal)

        #     self.updateBtn.setEnabled(lambda: True if success else False)
            # self.AuxC.setChecked(True if aux_auc.get(100002) else False)
            if (success):
                self.updateBtn.setEnabled(True if success else False)
            # else:
            #     self.updateBtn.setEnabled(False)

def getTableFields(self):
    global table, tableEntry

    for index in range(len(self.billsTypeList)):
        item = self.billsTypeList[index]
        if table == item[2] and tableEntry == item[3]:
            table = item[2]
            tableEntry = item[3]
            qty = item[4]
            demal = item[5]
            demanTag = item[6]
            return qty, demal, demanTag
    return False

# 更新尺码款型组合值
def update_spec(self):
    global success, demal, demalTag, newSum, table, tableEntry

    qty_field, demal_field, demalTag_field = getTableFields(self)
    if (success):
        

        sp.update_spec(demal, demalTag, newSum, qty_field, demal_field, demalTag_field, table, tableEntry)
        self.updateBtn.setEnabled(False)

        # 标记更新
        item_dict = current_material(self)
        if item_dict:
            item_dict['changed'] = True
            item_dict['FDemal'] = demal

# 更新尺码款型 勾选（TODO判断库存）
# def update_aux(self):
#     # 先查询物料信息
#     # exist = get_material()
#     # if exist: 
#         auxcChecked = self.AuxC.isChecked()
#         auxsChecked = self.AuxS.isChecked()
#         # print(auxcChecked, auxsChecked)
#         sp.update_aux(fNumber, 100002, auxcChecked)
#         sp.update_aux(fNumber, 100001, auxsChecked)

def auxCChenkBox_changed(chenked, auxPropertyId, self):
    # print(state, chenked, auxPropertyId)
    # print(chenked, auxPropertyId)

    # current_window = QApplication.activeWindow()  # 获取当前活动窗口
    # PopupWindow('w', "警告", tip, current_window).exec_()
    # confirm('警告', tip)
    aa = '开启' if chenked else '关闭'
    auxPropertyName = '尺码' if auxPropertyId == 100001 else ('款型' if auxPropertyId == 100002 else '未知')
    tip = f"{aa}【{fNumber}-{auxPropertyName}】？"
    operate = confirm('警告', tip)
    
    if operate: 
        sp.update_aux(fNumber, auxPropertyId, chenked)

        comboBox = window.findChild(QComboBox, "mulAuxC")
        if comboBox and chenked:
            comboBox.setVisible(True)
        else:
            comboBox.setVisible(False)
    else:
        self.AuxS.setChecked(not chenked) if auxPropertyId == 100001 else self.AuxC.setChecked(not chenked)
        # self.AuxS.setChecked(True) if auxPropertyId == 100001 else self.AuxC.setChecked(True)


def main():
    # 记录程序启动日志
    logging.info('Executable started with command: %s', ' '.join(sys.argv))
    # 你的程序主体部分
    global window
    app = QApplication(sys.argv)
    window = CreatedWindow()

    mul_AuxC(window)

    window.show()
    app.exec()

def mul_AuxC(window):

    # group_box = window.findChild(QtWidgets.QGroupBox, "frame") 
    group_box = window.findChild(QtWidgets.QWidget, "widget")

    comunes = ['A', 'B', 'C', 'D', '无']
    # 创建 CheckableComboBox 实例
    comboBox = CheckableComboBox()
    comboBox.addItems(comunes)
    comboBox.setFixedSize(50, 30)
    comboBox.setObjectName("mulAuxC")

    # 设置 comboBox1 在窗口上的位置
    # comboBox.move(20, 30)
    # 计算新的 x 坐标，将组件放在 QGroupBox 的右侧
    #new_x = group_box.width() - comboBox.width()
    
    # 移动 comboBox1 到新的位置
    # comboBox.move(new_x, 0)  # 这里的 0 是 Y 坐标，可以根据需要进行调整

    # comboBox1.setGeometry (20, 30, 50, 30)
    # 创建一个布局管理器，例如 QVBoxLayout
    layout = QtWidgets.QVBoxLayout()
    # 将容器添加到布局中
    layout.addWidget(comboBox)
    # 将布局设置给 QGroupBox
    group_box.setLayout(layout)
    comboBox.setVisible(False)

if __name__ == "__main__":
    # print('开始')
    main()
    # input("Press Enter to exit...")