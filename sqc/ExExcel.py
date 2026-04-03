import os
import pandas as pd

def merge_excel_files(input_folder, output_file):
    """
    合并指定文件夹中的所有Excel文件到一个新的Excel文件中。

    :param input_folder: 包含Excel文件的文件夹路径
    :param output_file: 输出的合并后的Excel文件路径
    """
    # 存储所有数据的列表
    all_data = []

    # 遍历文件夹中的所有文件
    for file_name in os.listdir(input_folder):
        # 检查文件是否为Excel文件
        if file_name.endswith('.xlsx') or file_name.endswith('.xls'):
            file_path = os.path.join(input_folder, file_name)
            print(f"正在读取文件: {file_path}")

            # 读取Excel文件中的所有工作表
            excel_data = pd.read_excel(file_path, sheet_name=None)

            # 遍历每个工作表并将数据添加到all_data
            for sheet_name, df in excel_data.items():
                df['来源文件'] = file_name  # 添加一列标记数据来源
                df['工作表名称'] = sheet_name
                all_data.append(df)

    if not all_data:
        print("未找到任何Excel文件！")
        return

    # 将所有数据合并为一个DataFrame
    combined_data = pd.concat(all_data, ignore_index=True)

    # 将合并后的数据写入新的Excel文件
    combined_data.to_excel(output_file, index=False, engine='openpyxl')
    print(f"合并完成，结果已保存到: {output_file}")


if __name__ == "__main__":
    # 提示用户输入文件夹路径和输出文件名
    input_folder = input("请输入包含Excel文件的文件夹路径: ").strip()
    output_file = input("请输入合并后的Excel文件保存路径（包括文件名）: ").strip()

    if not os.path.exists(input_folder):
        print("指定的文件夹路径不存在，请检查后重试！")
    else:
        merge_excel_files(input_folder, output_file)