import os


# # 输入的字符串列表
# input_strings = ["1_046无", "1_048无", "1_050无", "1_052无", "1_054无"]

# # 找到所有字符串中的相同部分，包括 "无"
# common_part = None

# for s in input_strings:
#     if common_part is None:
#         common_part = s
#     else:
#         for i in range(min(len(common_part), len(s))):
#             if common_part[i] != s[i]:
#                 common_part = common_part[:i]
#                 break

# print(common_part)


# # 输入的字符串列表
# input_strings = ["1_046无", "1_048无", "1_050无", "1_052无", "1_054无"]

# # 提取相同部分的前缀，不包括数字
# common_prefix = ""
# i = 0

# while all(i < len(s) and s[i] == input_strings[0][i] and not s[i].isdigit() for s in input_strings):
#     common_prefix += input_strings[0][i]
#     i += 1

# print(common_prefix)

# # 输入的字符串列表
# input_strings = ['46无','48无','50无','52无','54无']

# # 提取相同部分的前缀，不包括数字
# common_prefix = ""
# i = 0

# while i < len(input_strings[0]) and all(s.startswith(input_strings[0][:i+1]) for s in input_strings):
#     if not input_strings[0][i].isdigit():
#         common_prefix += input_strings[0][i]
#     i += 1

# print(common_prefix)

# # 输入的字符串列表
# input_strings = ['46无','48无','50无','52无','54无']

# # 提取相同部分的前缀，不包括数字
# common_prefix = ""
# i = 0

# while i < len(input_strings[0]) and all(s.startswith(input_strings[0][:i+1]) for s in input_strings):
#     if not input_strings[0][i].isdigit():
#         common_prefix += input_strings[0][i]
#     i += 1

# if not common_prefix:
#     print("没有相同的前缀")
# else:
#     print(common_prefix)
# 输入的字符串列表
# input_strings = ["1_046无", "1_048无", "1_050无", "1_052无", "1_054无"]

# -- -----------------------------------------------------------------------------------------------
# input_strings = ['46无','48无','50无','52无','54无']
# -- -----------------------------------------------------------------------------------------------

# # 获取共同的前缀字符串 1_0 2_0 
# def common_prefix(data_dict):
#     arr = [s for s in data_dict.keys()]  # 只获取字典中的值，形成新的列表
#     # 提取相同部分的前缀
#     common_prefix = os.path.commonprefix(arr)
#     # 去除原字符串中的 "1_0" 并输出
#     result = ','.join(s.replace(common_prefix, '') for s in arr)
#     print(f'数组：{arr}\n相同的前缀：{common_prefix}\nReult: {result}')

#     return common_prefix, result

def common_prefix(data_dict):
    arr = [s for s in data_dict.keys()]  # 只获取字典中的键，形成新的列表
    # 提取相同部分的前缀
    common_prefix = os.path.commonprefix(arr)
    # 使用一个新字典存储替换后的键和原始的 values
    new_data_dict = {}
    for key, value in data_dict.items():
        new_key = key.replace(common_prefix, '')
        new_data_dict[new_key] = value
    
    result = ','.join(new_data_dict.keys())

    print(f'参数：{data_dict}\n相同的前缀：{common_prefix}\n尺码: {result}')
    
    return common_prefix, new_data_dict

# 获取共同的字符(款型) 区分尺码款型
def get_AuxC(data_dict):
    arr = [s for s in data_dict.keys()]  # 只获取字典中的键，形成新的列表
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
            # 获取共同的字符，因为只有二维的 所以只会有1个值
            AuxC = list(AuxCs)[0]  
            # 去除共同字符并分割成数字
            # AuxSc = [s.replace(common_value, '') for s in arr]
            AuxSc = [s[:-1] if s.endswith(AuxC) else s for s in arr]
            new_key = key.replace(AuxC, '')
        new_data_dict[new_key] = value

    AuxSc = sorted(AuxSc)
    if AuxSc:
        print(f"款型：{AuxC}，尺码：{AuxSc}")
    else:
        AuxSc = arr
        print(f"无款型，尺码：{AuxSc}")

    return AuxCs, AuxSc, new_data_dict

# 获取字符串中的尺码，尺码数量
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

# 规格数量 无用
def spec_qty(AuxS, AuxC, specQtyList):
    if AuxC:
        # 获取共同的字符，因为只有二维的 所以只会有1个值
        auxc = list(AuxC)[0]  
        # 去除共同字符并分割成数字
        result = [s.replace(auxc, '') for s in specQtyList]

    specQtyList.keys()
    print()


if __name__ == "__main__":
    # str = '1_046A,1_048A,1_050A,1_052A,1_054A'
    # str = '1_046A,1_048A,1_050AA,1_052A,1_054A'
    # str = '1_046无,1_048无,1_050无,1_052无,1_054无'
    # str = '1_046,1_048,1_050,1_052,1_054'
    # str = '46无,48无,50无,52无,54无'
    # str = '2_040无:65,2_041无:62,2_042无:45,2_043无:28,2_038无:32,2_039无:68'
    # str = '1_046无:13,1_048无:51,1_050无:53,1_052无:41,1_054无:19'
    # str = '46:13,48:51,50:53,52:41,54:19'
    arr = str.split(',')
    # split_spec(arr)

    specList, specQtyList = split_spec(arr)
    # print('specQtyList', specQtyList)
    commonPrefix, afterSpecList = common_prefix(specQtyList)
    # print(commonPrefix, afterSpecList)

    AuxC, AuxS, AuxCSQty = get_AuxC(afterSpecList)
    print(AuxCSQty)
    # AuxS：尺码，AuxC：款型


    # AuxC, AuxS = get_AuxC()
    # # commonChar, sizeList = get_AuxC(common_prefix(split_spec(arr)))
    # print(f'specList: {specList}\nspecQtyList: {specQtyList}\nAuxS: {AuxS}\nAuxC：{AuxC}')
    # get_AuxC(common_prefix(split_spec(arr)))
    # get_AuxC(common_prefix(arr))
    # str1 = '100.06.34'
    # print('100.06.34'[1:6])