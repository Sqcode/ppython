import requests,random, time, pymysql
import json
import pandas as pd
from datetime import datetime
import os, time, requests, random, telnetlib, json, pypinyin, cv2, traceback
__dir__ = os.path.dirname(os.path.abspath(__file__))
# print(__dir__)
from bs4 import BeautifulSoup
from openpyxl import Workbook

# 转换时间戳函数
def format_timestamp(ms):
    return datetime.fromtimestamp(ms / 1000).strftime('%Y-%m-%d %H:%M:%S')

# 🔽 新增函数：从 Excel 读取 member_id 列表
def read_member_ids(file_path):
    """
    从 Excel 文件中读取 member_id 列
    :param file_path: Excel 文件路径
    :return: 去重后的 member_id 列表
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件未找到: {file_path}")

    try:
        df = pd.read_excel(file_path)
        if 'member_id' not in df.columns:
            raise ValueError("Excel 文件中缺少 'member_id' 列")

        # 去重 + 转为字符串类型
        member_ids = df['member_id'].dropna().astype(str).unique().tolist()
        return member_ids
    except Exception as e:
        raise RuntimeError(f"读取 Excel 文件失败: {e}")
    
def get(beginTime, endTime, memberId):
    global db
    # 1. 设置请求参数
    url = 'https://hope.demogic.com/api-member/member-load-operate-log-page?requestProject=member'  # 替换为你的目标URL
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Content-Type': 'application/json',
        'Cookie': 'Path=/; _abfpc=a47a63c4e9475b910f4d83b1aeab359ce402ec05_2.0; cna=d0c1f4faa09a6df69841a72d66beea34; web_login_cookie_id=ff8080816f42af5a016f59b8021934eb; web_login_cookie_id_last_login_time=1751701196396; tgw_l7_route=24c4e1fc660a6b84af415ca53882223e'  # 替换为你需要设置的 Cookie 值
    }

    # 如果你有登录等操作，也可以通过会话自动管理 Cookie
    # session = requests.Session()
    # session.post('https://example.com/login', data={"username": "xxx", "password": "xxx"})
    # response = session.post(url, headers=headers, json=payload)

    payload = {"pageSize":100,"currentPage":1,"beginTime": beginTime,"endTime": endTime,"memberId": memberId}

    # 2. 发送 POST 请求
    response = requests.post(url, headers=headers, json=payload)

    # 3. 检查响应状态码
    if response.status_code == 200:
        try:
            data = response.json()  # 解析返回的 JSON 数据
        except json.JSONDecodeError:
            print("返回内容不是合法的JSON")
            with open("raw_response.txt", "w", encoding="utf-8") as f:
                f.write(response.text)
            print("原始响应已保存为 raw_response.txt，请检查。")
            exit()
        
        all_data = []

        page = 1
        total_page = 1
        while page <= total_page:
            payload = {
                "pageSize": 100,
                "currentPage": page,
                "beginTime": beginTime,
                "endTime": endTime,
                "memberId": memberId
            }

            response = requests.post(url, headers=headers, json=payload)
            if response.status_code != 200:
                print(f"请求失败，状态码: {response.status_code}")
                break

            data = response.json()
            if data.get('errorCode') != 0:
                print("接口返回错误:", data.get('message'))
                break

            result_page = data['result']['page']
            total_page = result_page['totalPage']
            current_data = result_page['result']

            if current_data:
                # 添加 memberId 并格式化时间戳
                for item in current_data:
                    item['memberId'] = memberId
                    if 'createTime' in item:
                        item['createTime'] = format_timestamp(item['createTime'])

                    sql = f"""Insert into gic_member_log (`log_id`,`create_time`,`oper_type`,`oper_content`,`oper_reason`,`oper_remark`,`refer_log_id`,`member_id`) 
        values ('{item['logId']}','{item['createTime']}','{item['operType']}','{item['operContent']}','{item['operReason']}', '{item['operRemark']}', '{item['referLogId']}','{memberId}')"""
                    upd(sql)
                						

                all_data.extend(current_data)
            # print(f"第 {page}/{total_page} 页数据已获取")
            page += 1
        
        return all_data
       
    else:
        print(f"请求失败，状态码: {response.status_code}")
        print("响应内容:", response.text)

def start():
    output_dir = os.path.join(__dir__, '..', 'dic')
    # 获取当前脚本所在的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 构造输入文件的绝对路径
    input_excel = os.path.join(current_dir, '..', 'dic', '2025member.xlsx')
    try:
        member_ids = read_member_ids(input_excel)
        print(f"共发现 {len(member_ids)} 个 memberId")
    except Exception as e:
        print(f"错误：{e}")
        exit(1)

    # 按每批 50 个分组处理
    BATCH_SIZE = 1000
    total_batches = (len(member_ids) + BATCH_SIZE - 1) // BATCH_SIZE
    file_index = 1        # 导出文件计数器  
    EXPORT_EVERY = 10000  # 每处理多少个用户导出一份 Excel
    all_data = []
    for i in range(total_batches):
        start_idx = i * BATCH_SIZE
        end_idx = min((i + 1) * BATCH_SIZE, len(member_ids))
        batch_member_ids = member_ids[start_idx:end_idx]

        print(f"\n👉 正在处理第 {i+1}/{total_batches} 批数据，共 {len(batch_member_ids)} 个 memberId")

        # 遍历这一批中的每个 memberId，并记录全局序号
        for idx, member_id in enumerate(batch_member_ids, start=start_idx + 1):
            print(f"📊 正在处理第 {idx} / 共 {len(member_ids)} 个 memberId: {member_id}")

            # 模拟请求逻辑（替换为你的接口调用）
            # fetch_member_logs(member_id)
            data = get("2021-01-01", "2025-07-12", member_id)
            # all_data.extend(data)
            # 随机延迟
            delay = random.uniform(0.1, 1)
            # print(f"⏱️  随机等待 {delay:.2f} 秒...\n")
            time.sleep(delay)
    # if not all_data:
    #     print("没有获取到任何数据")
    # else:
    #     # 转换为 DataFrame
    #     df = pd.DataFrame(all_data)
    #     os.makedirs('dic', exist_ok=True)

    #     output_file = os.path.join(__dir__, '../dic/%s'%str(round(time.time() * 1000)) + '.xlsx')
    #     df.to_excel(output_file, index=False, engine='openpyxl')

    #     print(f"共获取 {len(all_data)} 条记录，已保存至：{output_file}")

    print('处理完成！')


# 获取数据库连接
def get_connection(user, pwd, host='localhost', database='gic'):
    # 打开数据库连接
    global db
    db = pymysql.connect(host=host, user=user, password=pwd, database=database)
    get_cursor()
    return db

def get_cursor():
    global cursor
    cursor = db.cursor()

# 更新
def upd(sql):
    # print(sql)
    try:
        # 执行SQL语句
        cursor.execute(sql)
    # 提交到数据库执行
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()

if __name__ == "__main__":
    db = get_connection('root', 'root')
    # sql = f"""Insert into gic_member_log (`log_id`,`create_time`,`oper_type`,`oper_content`,`oper_reason`,`oper_remark`,`refer_log_id`,`member_id`) 
    #     values ('111','2025-06-12 14:27:19','333','444','555', '666', '777','888')"""
    # upd(sql)
    start()

    db.close()
    # start()
    # data = get("2022-06-13", "2025-06-12", "ff808081855937a70185682ee5506c8d")
    # print(data)