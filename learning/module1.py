# from global_variables import table, tableEntry, global_var1, global_var2, global_var
import module2 as m2
# import importlib
import os, configparser
# module1.py

# def function_in_module1():
#     global global_var1

#     print(f"module1: global_var1 = {global_var1}")
#     print(f"module1: global_var2 = {global_var2}")

#     global_var1 = "Modified in module1"
#     m2.function_in_module2()


def update(table, tableEntry):
    # global table, tableEntry
    print(f'm1 before: {table} = {tableEntry}')

    table = 1
    tableEntry = 1
    print(f'm1 after: {table} = {tableEntry}')
    # importlib.reload(m2)  # 重新加载模块2
    m2.prf()

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

if __name__ == "__main__":
    print('开始')
    table, tableEntry = config()
    update(table, tableEntry)
    # function_in_module1()

    
# def modify_global_variable():
#     global global_var
#     global_var = "Modified in module1"

# if __name__ == "__main__":
#     print(f"module1: global_var before modification = {global_var}")
#     modify_global_variable()
#     print(f"module1: global_var after modification = {global_var}")
#     m2.function_in_module2()