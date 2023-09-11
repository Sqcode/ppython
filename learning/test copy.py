import json, os, time
from oracle_long_conn import OracleDatabase, get_connection, close

billNoFID = None
fMaterialId = None

def update_spec(demal, demalTag):
    global connectionPool, fMaterialId, billNoFID

    sql = '''
        UPDATE KINGDEE00.T_PUR_POORDERENTRY SET F_SCAG_FDEMAL = :DEMAL, F_SCAG_FDEMAL_TAG = :DEMALTAG 
        WHERE FENTRYID = (SELECT FENTRYID FROM KINGDEE00.T_PUR_POORDERENTRY WHERE FID = :FID AND FMATERIALID = :FMATERIALID)
    '''
    params = {"FID": billNoFID, "FMATERIALID": fMaterialId, "DEMAL": demal, "DEMALTAG": demalTag.encode()}
    rowcount = connectionPool.execute_update(sql, params)

    if rowcount > 0:
        print(f"Update successful")

# 重设规格值
def reset_spec(commonPrefix, AuxCs, AuxCS, AuxCSQty):
    result = {"FlexList": []}
    newSum = 0 # 新规格格式 数量
    newSpecQtyList = [] # 新规格格式
    # print(f'reset_spec: {AuxCS}, {AuxCSQty}')
    
    for auxs_item in sorted(AuxCS.get("AuxS", []), key=lambda x: x["AuxNumber"]):
        auxs_auxnumber = auxs_item["AuxNumber"]
        item = {
            "AuxS": auxs_item,
            "Qty": 0.0
        }
        auxs_qty = 0.0
        if commonPrefix in auxs_auxnumber:
            # 替换前缀
            auxs_qty = AuxCSQty.get(auxs_auxnumber.replace(commonPrefix, ''), 0.0)
            newSum += auxs_qty
            item['Qty'] = auxs_qty

        auxc_data = sorted(AuxCS.get("AuxC", []), key=lambda x: x["AuxNumber"])
        # 款型
        if len(auxc_data) > 0:
            # for auxc_item in auxc_data:
            for index, auxc_item in enumerate(auxc_data):
                if index > 0:
                    break
                auxc_auxnumber = auxc_item["AuxNumber"]
                item['AuxC'] = auxc_item
                result["FlexList"].append(item) 
                if auxs_qty > 0:
                    print(f'尺码: {auxs_auxnumber}, 数量 {auxs_qty}')
                    newSpecQtyList.append(f"{auxs_auxnumber}{auxc_auxnumber}:{auxs_qty}")
                
        else:
            result["FlexList"].append(item) 
            if auxs_qty > 0:
                print(f'尺码: {auxs_auxnumber}, 数量 {auxs_qty}')
                newSpecQtyList.append(f"{auxs_auxnumber}:{auxs_qty}")
        
    originSum = sum(AuxCSQty.values())

    newSpecQtyTagListString = json.dumps(result, ensure_ascii=False)
    print(f'新尺码组Tag：{newSpecQtyTagListString}')

    newSpecQtyListString = ','.join(newSpecQtyList)
    print(f'新尺码组: {newSpecQtyListString}')

    if originSum != newSum:
        print(f'总数量不符,源：{originSum},新：{newSum}\n 请检查核对当前物料的尺码值 是否重复或不存在！')
        return False
    
    return True, newSpecQtyListString, newSpecQtyTagListString

# 获取单据上的所有物料明细
def get_bills(FBillno):
    global connectionPool, billNoFID
    sql = '''
        SELECT TPPE.FID, TBM.FNUMBER, TBML.FNAME, TPPE.F_SCAG_FDEMAL
        FROM KINGDEE00.T_PUR_POORDERENTRY TPPE
        LEFT JOIN KINGDEE00.T_BD_MATERIAL TBM ON TBM.FMATERIALID = TPPE.FMATERIALID -- 物料
        LEFT JOIN KINGDEE00.T_BD_MATERIAL_L TBML ON TBML.FMATERIALID = TBM.FMATERIALID -- 物料基础资料
        WHERE TPPE.FID = (SELECT FID FROM KINGDEE00.T_PUR_POORDER WHERE FBillno = :FBILLNO) 
    '''
    params = {"FBILLNO": FBillno}
    list = connectionPool.execute_query(sql, params)

    # 格式化
    list_data = {}
    for item in list:
        fid, fnumber, fname, fdemal = item
        if fid not in list_data:
            list_data[fid] = []
        list_data[fid].append({"FNumber": fnumber, "FName": fname, "FDemal": fdemal})
        billNoFID = fid
    print(f'订单号：{FBillno}, 明细：{list_data}')
    return list_data

# 获取单据上的 规格 specString = "046:13,048:51,050:53,052:41,054:19"
def get_bills_specString(fBillNo, fNumber):
    global connectionPool
    # 采购订单
    sql = '''
        SELECT F_SCAG_FDEMAL, DBMS_LOB.SUBSTR(F_SCAG_FDEMAL_TAG, 4000, 1) AS BLOB_DATA 
        FROM KINGDEE00.T_PUR_POORDERENTRY 
        WHERE FID = (SELECT FID FROM KINGDEE00.T_PUR_POORDER WHERE FBillno = :FBILLNO) 
            AND FMATERIALID = (SELECT FMATERIALID FROM KINGDEE00.T_BD_MATERIAL WHERE FNUMBER = :FNUMBER AND FUSEORGID = 1)
    '''
    params = {"FNUMBER": fNumber, "FBILLNO": fBillNo}

    specString = connectionPool.execute_query(sql, params)
    return specString[0][0].split(',')

# 源规格 是否存在现物料尺码组
def check_in_specList(fNumber, commonPrefix, AuxS):
    # 获取物流的可选值
    AuxCS = get_material_spec(fNumber)
    '''
    判断物料的尺码规格 是否存在
    '''
    auxs_list = AuxCS.get('AuxS', [])
    auxnumber_values = [item['AuxNumber'].replace(commonPrefix, '') for item in auxs_list if '_' in item['AuxNumber']]
    # print(AuxS, auxnumber_values)
    for auxs_key in AuxS:
        if auxs_key not in auxnumber_values:
            print(f'现物料不存在尺码值【{auxs_key}】！')
            return False
    return True, AuxCS

# 查询物料的可选尺码、款型
def get_material_spec(fNumber):
    global connectionPool, fMaterialId
    sql = f'''
        SELECT TBM.FMATERIALID, TBM.FNUMBER MaterialCode, TBML.FNAME MaterialName, TBAVE.FAUXPTYID AuxId, TBAVE.FAUXPTYNUMBER AuxNumber, (CASE WHEN TBAV.FMATERIALAUXPROPERTYID = 100001 THEN 'AuxS' WHEN TBAV.FMATERIALAUXPROPERTYID = 100002 THEN 'AuxC' ELSE CAST(NULL AS VARCHAR2(1)) END) JsonKey
        FROM KINGDEE00.T_BD_MATERIAL TBM
        LEFT JOIN KINGDEE00.T_BD_AUXPTYVALUE TBAV ON TBAV.FMATERIALID = TBM.FMATERIALID  
        LEFT JOIN KINGDEE00.T_BD_AUXPTYVALUEENTITY TBAVE ON TBAVE.FAUXPTYVALUEID = TBAV.FAUXPTYVALUEID 
        LEFT JOIN KINGDEE00.T_BD_MATERIAL_L TBML ON (TBML.FMATERIALID = TBM.FMATERIALID AND TBML.FLOCALEID = 2052)
        WHERE 1=1 AND TBM.FUSEORGID = 1 AND TBM.FDOCUMENTSTATUS = 'C'
        AND TBM.FNUMBER = :FNUMBER
        ORDER BY TBM.FNUMBER
    '''
    params = {"FNUMBER": fNumber}
    specList = connectionPool.execute_query(sql, params)

    # 格式化
    grouped_data = {}
    for item in specList:
        FMaterialId, material_code, material_name, aux_id, aux_number, json_key = item
        # （这里还是别去掉吧,后面匹配取有下划线的值）检查aux_number是否包含下划线,如果包含才添加到grouped_data中
        # if json_key == 'AuxS' and "_" not in aux_number:
        #     continue
        fMaterialId = FMaterialId
        if json_key not in grouped_data:
            grouped_data[json_key] = []
        grouped_data[json_key].append({"AuxId": aux_id, "AuxNumber": aux_number})

    return grouped_data

# 查询物料的款型是否开启
def get_material_aux(fNumber):
    global connectionPool
    # 获取款型是否使用 FAUXPROPERTYID = 100002 
    sql_auxc = '''
        SELECT FAUXPROPERTYID, FISENABLE FROM KINGDEE00.T_BD_MATERIALAUXPTY 
        WHERE 1=1 AND FUSEORGID = 1 AND FUSEORGID = 1
        AND FMATERIALID = (SELECT FMATERIALID FROM KINGDEE00.T_BD_MATERIAL WHERE FNUMBER = :FNUMBER AND FUSEORGID = 1)
    '''
    params = {"FNUMBER": fNumber}
    res = connectionPool.execute_query(sql_auxc, params)

    # 格式化
    aux_auc = {}
    for item in res:
        auxPropertyId , isEnable = item
        aux_auc[auxPropertyId] = bool(int(isEnable))

    # print(aux_auc, aux_auc.get(100002))
    # if (aux_auc.get(100002)):
    #     print(f'款型未开启：{aux_auc}')
    #     return False
    
    return aux_auc

# 获取尺码相同的前缀
def common_prefix(data_dict):
    arr = [s for s in data_dict.keys()]  # 只获取字典中的键,形成新的列表
    # 提取相同部分的前缀
    commonPrefix = os.path.commonprefix(arr)
    # 使用一个新字典存储替换后的键和原始的 values
    new_data_dict = {}
    for key, value in data_dict.items():
        new_key = key.replace(commonPrefix, '')
        new_data_dict[new_key] = value
    
    result = ','.join(new_data_dict.keys())

    print(f'参数：{data_dict}\n相同的前缀：{commonPrefix}\n尺码: {result}')
    
    return commonPrefix, new_data_dict

# 获取共同的字符(款型) 区分尺码款型
def get_AuxC(data_dict):
    arr = [s for s in data_dict.keys()]  # 只获取字典中的键,形成新的列表
    # 找到所有字符串中的相同值
    AuxCs = set(arr[0])  # 将第一个字符串的字符初始化为共同字符集合
    for s in arr[1:]:
        # AuxCs.intersection_update(s)  # 逐个交集更新
        AuxCs.intersection_update(c for c in s if not c.isdigit()) # 排除数字

    AuxSc = []  # 初始化 AuxSc 为空列表
    new_data_dict = {}

    for key, value in data_dict.items():
        new_key = key
        if AuxCs:
            # 获取共同的字符,因为只有二维的 所以只会有1个值,也不一定了。暂不处理
            AuxC = list(AuxCs)[0]  
            # 去除共同字符并分割成数字
            # AuxSc = [s.replace(common_value, '') for s in arr]
            AuxSc = [s[:-1] if s.endswith(AuxC) else s for s in arr]
            new_key = key.replace(AuxC, '')
        new_data_dict[new_key] = value

    AuxSc = sorted(AuxSc)
    if AuxSc:
        print(f"款型：{AuxC},尺码：{AuxSc}")
    else:
        AuxSc = arr
        print(f"无款型,尺码：{AuxSc}")

    return AuxCs, AuxSc, new_data_dict

# 获取字符串中的尺码,尺码数量
def split_spec(arr):
    data_dict = {}
    for pair in arr:
        key_value = pair.split(':')
        if len(key_value) == 2:
            key = key_value[0]
            value = float(key_value[1])
            data_dict[key] = value
    # print('data_dict', data_dict)

    return list(set(data_dict.keys())), data_dict


# if __name__ == "__main__":
#     global connectionPool
#     connectionPool = get_connection()
#     fBillNo = 'C123001'
#     fNumber = 'SP2302ZC99855'

#     # 获取单据里的明细物料
#     get_bills(fBillNo)
#     time.sleep(2)

#     str = '46:13,48:51,50:53,52:41,54:19'
#     arr = str.split(',')
#     arr = get_bills_specString(fBillNo, fNumber)
#     # 延迟一下 数据库查询
#     time.sleep(2)

#     specList, specQtyList = split_spec(arr)
#     # print('specQtyList', specQtyList)

#     commonPrefix, AuxCSList = common_prefix(specQtyList)
#     # print(commonPrefix, AuxCSList)

#     # AuxS：尺码,AuxC：款型
#     AuxC, AuxS, AuxCSQty = get_AuxC(AuxCSList)
#     # print(AuxCSQty)

#     # 重设值
#     # print(f'AuxC: {AuxC}\nAuxS: {AuxS}\nAuxCSQty: {AuxCSQty}')

#     # 检查,一维内的尺码 是否在物料的可选尺码内
#     flag, AuxCS = check_in_specList(fNumber, commonPrefix, AuxS)
#     # print(specTag)

#     aux_auc = get_material_aux(fNumber)
#     # print(aux_auc)

#     # 
#     if (aux_auc and flag):
#         # JSON串,数量 拼接进去
#         success, demal, demalTag = reset_spec(commonPrefix, None, AuxCS, AuxCSQty)
#         # if (success):
#         #     update_spec(demal, demalTag)

#     close(connectionPool)