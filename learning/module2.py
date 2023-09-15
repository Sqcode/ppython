# from global_variables import table, tableEntry, global_var1, global_var2, global_var
# import global_variables as gv
import importlib

import os, configparser
# def function_in_module2():
#     print(f"module2: global_var1 = {global_var1}")
#     print(f"module2: global_var2 = {global_var2}")

def prf():
    table, tableEntry = config()
    # importlib.reload(gv)  # 重新加载模块2
    # print(f'm2: {gvable} = {gv.tableEntry}')
    print(f'm2: {table} = {tableEntry}')

def config():
    # 获取当前脚本所在目录
    script_directory = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(script_directory, 'global_variables.ini')
    # 创建配置解析器对象
    config = configparser.ConfigParser()
    # 读取配置文件
    config.read(config_file_path)
    # 获取全局变量值
    table = config.get('Variables', 'table')
    tableEntry = config.get('Variables', 'tableEntry')

    # print(f'm1 before: {table} = {tableEntry}')
    return table, tableEntry

# def function_in_module2():
#     print(f"module2: global_var = {global_var}")


# if __name__ == "__main__":
#     print('开始')
#     prf()
