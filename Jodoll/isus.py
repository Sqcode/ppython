import requests,random, time, pymysql
import json
import pandas as pd
from datetime import datetime
import os, time, requests, random, telnetlib, json, pypinyin, cv2, traceback
__dir__ = os.path.dirname(os.path.abspath(__file__))
# print(__dir__)
from bs4 import BeautifulSoup
from openpyxl import Workbook
import pytz
import logging
# 请求地址模板
base_url = "https://isus.vip/gw.managerCompany.coreUser.getViewList"

# 设置时区为北京时间
tz = pytz.timezone('Asia/Shanghai')
current_time = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

# 请求头
headers = {
    "Cookie": "gr_user_id=7fcc0daa-1e75-4ce4-b2ea-35757ea73137; bfc5363a9e6b44fe_gr_session_id=29fc33cd-a119-48c1-b942-a49e5d70f7d9; bfc5363a9e6b44fe_gr_session_id_sent_vst=29fc33cd-a119-48c1-b942-a49e5d70f7d9", 
    "passport": "G1oA-J0HdkyYmHUJhj-qjKZ06r6Pc0opcPkdC26JJvNZzCM2ueoJK09oqi8wiZqHV9PhhBl6Xb0KHIGZQGiMQcqyfgG3VLrb2W-CMj3737K1GpIA"
}

# 分页参数
params = {
    "page": 1,
    "rows": 1000,          # 每页数量
    "nickname": "",
    "source": "",
    "mobile": "",
    "from": "",
    "activeBtn": ""
}

# 字符串转毫秒级时间戳函数
def str_to_millis(date_str, fmt='%Y-%m-%d %H:%M:%S'):
    dt = datetime.strptime(date_str, fmt)
    timestamp_seconds = time.mktime(dt.timetuple())
    return int(timestamp_seconds * 1000)  # 转换为毫秒级时间戳（字符串）

def parse_timestamp(ts):
    """将毫秒时间戳转换为可读时间"""
    return datetime.fromtimestamp(ts / 1000).strftime('%Y-%m-%d %H:%M:%S')
# 将毫秒时间戳转为 datetime 格式字符串
def timestamp_to_datetime(timestamp_ms):
    if not timestamp_ms:
        return None
    try:
        # 时间戳是毫秒，除以 1000 得到秒
        dt = datetime.fromtimestamp(int(timestamp_ms) / 1000)
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        print(f"时间戳转换失败: {e}")
        return None

def fetch_data(page, from_date_str, to_date_str):
    
    # 转换为毫秒时间戳（字符串）
    fromAt = str_to_millis(from_date_str)
    toAt = str_to_millis(to_date_str)

    params["page"] = page
    params["fromAt"] = fromAt
    params["toAt"] = toAt
    response = requests.get(base_url, headers=headers, params=params)
    if response.status_code == 200:
        try:
            data = response.json()
            # print(data)
            return data
        except Exception as e:
            print(f"解析JSON失败: {e}")
            return None
    else:
        print(f"请求失败，状态码：{response.status_code}")
        return None
    
def batch_main(from_date_str, to_date_str):
    page = 1
    total_page = 1  # 初始为1，在第一次请求后更新
    global_count = 0  # 全局用户计数器
    batch_size = 500
    batch_users = []  # 批量缓存用户

    while page <= total_page:
        print(f"\n正在获取第 {page} 页数据...")

        data = fetch_data(page, from_date_str, to_date_str)

        if not data:
            print(f"第 {page} 页数据为空或请求失败")
            page += 1
            continue

        # 第一次获取总页数和总记录数
        if page == 1:
            try:
                total_page = data['pager']['pageMax']
                total_count = data['pager']['count']
                print(f"共 {total_count} 条记录，总页数: {total_page}")
            except KeyError as e:
                print("接口返回缺少字段:", e)
                return

        if 'list' in data:
            users = data.get('list', [])
            user_count = len(users)
            print(f"第 {page} 页共 {user_count} 个用户")

            for idx, user in enumerate(users, start=1):
                global_count += 1
                # print(f"[获取第 {global_count} 个用户] 用户：{user['userId']}")

                # 添加到批量缓存中
                batch_users.append(user)

                # 每满 500 条插入一次
                if len(batch_users) >= batch_size:
                    batch_insert_users(batch_users)
                    batch_users = []  # 清空缓存
        else:
            print(f"第 {page} 页没有数据或请求失败")

         # 随机延迟
        delay = random.uniform(1, 5)
        time.sleep(delay)

        # 下一页
        page += 1

    # 插入剩余不足 500 条的数据
    if batch_users:
        batch_insert_users(batch_users)

def main(from_date_str, to_date_str):
    page = 1
    total_page = 1  # 初始值为1，在首次请求后更新

    global_count = 0  # 全局插入用户计数器

    while page <= total_page:
        print(f"\n正在获取第 {page} 页数据...")

        # 请求数据
        data = fetch_data(page, from_date_str, to_date_str)

        if not data:
            print(f"第 {page} 页数据为空或请求失败")
            page += 1
            continue

        # 第一次获取到数据后设置 total_page
        if page == 1:
            try:
                total_page = data['pager']['pageMax']
                total_count = data['pager']['count']
                print(f"共 {total_count} 条记录，总页数: {total_page}")
            except KeyError as e:
                print("接口返回缺少关键字段:", e)
                return

        if 'list' in data:
            users = data.get('list', [])
            user_count = len(users)
            print(f"第 {page} 页共 {user_count} 个用户")

            for idx, user in enumerate(users, start=1):
                insert_user_to_db(user)
                global_count += 1
                print(f"[第 {global_count} 个用户] 已插入用户：{user['userId']}")

                # 随机延迟
                delay = random.uniform(0.1, 1)
                time.sleep(delay)

        else:
            print(f"第 {page} 页没有数据或请求失败")

        # 下一页
        page += 1
# 获取数据库连接
def get_connection(user, pwd, host='192.168.100.81', database='third_api'):
    # 打开数据库连接
    global db
    db = pymysql.connect(port=3307, host=host, user=user, password=pwd, database=database, 
    init_command='SET time_zone="+08:00"')
    get_cursor()
    return db

def get_cursor():
    global cursor
    cursor = db.cursor()

# 更新
def upd(sql):
    global db
    # print(sql)
    try:
        # 执行SQL语句
        cursor.execute(sql)
    # 提交到数据库执行
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()

def batch_insert_users(users):
    global db
    """
    批量插入用户数据，根据 coreUserStatistics 是否存在，选择插入字段
    :param users: 用户对象列表
    """
    # 分别缓存两类数据
    values_with_stats = []
    values_without_stats = []

    for user in users:
        userId = user.get('userId', '')
        nickname = user.get('nickname', '')
        mobile = user.get('mobile', '')
        gender = user.get('gender', 0)
        created = user.get('created', None)
        appWxaId = user.get('appWxaId', '')
        appWxbId = user.get('appWxbId', '')
        level = user.get('level', 0)
        avatar = user.get('avatar', '')
        coreUserStatistics = user.get('coreUserStatistics', '')
        shopSaleUser = user.get('shopSaleUser', '')
        from_ = user.get('from', '')

        created_ts = parse_timestamp(created)
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        created_by = 'system'
        deleted = 0

        stats = user.get('coreUserStatistics', {})
        if stats and isinstance(stats, dict):  # 存在 coreUserStatistics 并且是字典
            last_order_at = timestamp_to_datetime(stats.get('lastOrderAt'))
            order_count = stats.get('orderCount', 0)
            refund_price = stats.get('refundPrice', 0)
            total_price = stats.get('totalPrice', 0)

            values_with_stats.append((
                userId, nickname, mobile, gender, created_ts,
                appWxaId, appWxbId, level, avatar,
                json.dumps(stats, ensure_ascii=False), json.dumps(shopSaleUser, ensure_ascii=False), from_,
                created_by, current_time, deleted,
                last_order_at, order_count, refund_price, total_price
            ))

        else:  # 没有 coreUserStatistics 或为空
            values_without_stats.append((
                userId, nickname, mobile, gender, created_ts,
                appWxaId, appWxbId, level, avatar,
                json.dumps(stats, ensure_ascii=False), json.dumps(shopSaleUser, ensure_ascii=False), from_,
                created_by, current_time, deleted
            ))

    # SQL 插入语句模板
    sql_with_stats = """
    INSERT INTO isus_user (
        user_id, nick_name, mobile, gender, created,
        app_wxa_id, app_wxb_id, level, avatar,
        core_user_statistics, shop_sale_user, `from`,
        created_by, created_time, deleted,
        last_order_at, order_count, refund_price, total_price
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE updated_time = NOW()
    """

    sql_without_stats = """
    INSERT INTO isus_user (
        user_id, nick_name, mobile, gender, created,
        app_wxa_id, app_wxb_id, level, avatar,
        core_user_statistics, shop_sale_user, `from`,
        created_by, created_time, deleted
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE updated_time = NOW()
    """

    try:
        if values_with_stats:
            cursor.executemany(sql_with_stats, values_with_stats)
        if values_without_stats:
            cursor.executemany(sql_without_stats, values_without_stats)

        db.commit()
        print(f"已批量插入 {len(values_with_stats) + len(values_without_stats)} 条用户数据")

    except Exception as e:
        print(f"批量插入失败: {e}")
        db.rollback()

# 插入用户数据到数据库
def insert_user_to_db(user):
    userId = user.get('userId', '')
    nickname = user.get('nickname', '')
    mobile = user.get('mobile', '')
    gender = user.get('gender', 0)
    created = user.get('created', None)
    appWxaId = user.get('appWxaId', '')
    appWxbId = user.get('appWxbId', '')
    level = user.get('level', 0)
    avatar = user.get('avatar', '')
    coreUserStatistics = user.get('coreUserStatistics', '')

    shopSaleUser = user.get('shopSaleUser', '')
    from_ = user.get('from', '')

    # 额外字段模拟值
    created_by = 'system'
    # updated_by = 'system'
    deleted = 0
    created_ts = parse_timestamp(created)
    # 设置 created_time 为当前时间

    current_time = datetime.now()

    # 核心统计信息
    stats = user.get('coreUserStatistics', {})
    if stats:
        last_order_at = timestamp_to_datetime(stats.get('lastOrderAt'))
        order_count = stats.get('orderCount', 0)
        refund_price = stats.get('refundPrice', 0)
        total_price = stats.get('totalPrice', 0)

        # 构建 SQL 插入语句
        sql = f"""
        INSERT INTO isus_user (
            user_id, nick_name, mobile, gender, created, app_wxa_id, app_wxb_id, level, avatar, 
            core_user_statistics, shop_sale_user, `from`, created_by, created_time, deleted, last_order_at, order_count, refund_price, total_price
        ) VALUES (
            '{userId}', '{nickname}', '{mobile}', {gender}, '{created_ts if created_ts else 'NULL'}',
            '{appWxaId}', '{appWxbId}', {level}, '{avatar}', "{coreUserStatistics}", "{shopSaleUser}", '{from_}', '{created_by}', '{current_time}', {deleted} ,  '{last_order_at}', {order_count}, {refund_price}, {total_price}
        )
        """
    else:
        # 构建 SQL 插入语句
        sql = f"""
        INSERT INTO isus_user (
            user_id, nick_name, mobile, gender, created, app_wxa_id, app_wxb_id, level, avatar, 
            core_user_statistics, shop_sale_user, `from`, created_by, created_time, deleted
        ) VALUES (
            '{userId}', '{nickname}', '{mobile}', {gender}, '{created_ts if created_ts else 'NULL'}',
            '{appWxaId}', '{appWxbId}', {level}, '{avatar}', "{coreUserStatistics}", "{shopSaleUser}", '{from_}', '{created_by}', '{current_time}', {deleted} 
        )
        """
    # print(sql)
    upd(sql)

def get_student(from_date_str, to_date_str):
    
    # Step 1: 查询符合条件的用户
    query_sql = """
    SELECT user_id, id
    FROM isus_user 
    WHERE created >= %s AND created <= %s and id > 223128 order by id asc
    """

    cursor.execute(query_sql, (from_date_str, to_date_str))
    users = cursor.fetchall()  # [(user_id, created), ...]
    print(f"处理用户: {len(users)}")

    # print(users)
    student_values = []

    for user_row in users:
        user_id = user_row[0]
        id = user_row[1]
        # print(f"正在处理用户: {user_id}")

        # Step 2: 请求接口获取学生数据
        url = f"https://isus.vip/gw.managerCompany.coreStudent.getViewList?rows=1000&page=1&userId={user_id}"
        try:
            response = requests.get(url, headers=headers)
        except Exception as e:
            batch_insert_student(student_values)
            student_values.clear()
            print(f"请求错误: {id}: {user_id}")

        if response.status_code != 200:
            print(f"请求失败，用户ID: {user_id}")
            continue

        try:
            data = response.json()
            # print(data)
            student_list = data.get("list", [])  # 假设接口返回的数据结构中有 data 字段

        except json.JSONDecodeError:
            print(f"JSON 解析失败，用户ID: {user_id}")
            continue

        if len(student_list) > 0:
            print(f"正在处理用户: {id}: {user_id}")

        # Step 3: 遍历学生列表，准备插入数据
        for student in student_list:
            student_id = student.get("studentId")
            gender = student.get("gender", 0)
            student_no = student.get("studentNo", "")
            name = student.get("name", "")
            school_id = student.get("schoolId", "")
            school_name = student.get("school", {}).get("name", "")
            class_name = student.get("class", "未分班")
            grade = student.get("grade", "")
            created_ts = student.get("created")

            # 时间戳转 datetime
            created = datetime.fromtimestamp(created_ts / 1000) if created_ts else None

            # 准备插入字段
            now = datetime.now()
            deleted = 0

            student_values.append((
                student_id, user_id, gender, student_no, name,
                school_id, school_name, class_name, grade, created,
                'system', now, deleted
            ))
            
            # 每 100 条插入一次
            if len(student_values) >= 100:
                batch_insert_student(student_values)
                student_values.clear()
    
    # 插入剩余不足 100 条的数据
    if student_values:
        batch_insert_student(student_values)
        student_values.clear()


    if student_values:
        try:
            cursor.executemany(student_values)
            db.commit()
            print(f"成功处理 {len(student_values)} 条学生数据")
        except Exception as e:
            print(f"插入失败: {e}")
            db.rollback()
    else:
        print("没有学生数据需要插入")

def batch_insert_student(values):
    global db

    # Step 4: 批量插入学生数据（忽略重复）
    insert_sql = """
    INSERT INTO isus_student (
        student_id, user_id, gender, student_no, name,
        school_id, school_name, class_name, grade, created,
        created_by, created_time, deleted
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE updated_time = NOW()
    """

    try:
        cursor.executemany(insert_sql, values)
        db.commit()
        print(f"成功插入 {len(values)} 条数据")
    except Exception as e:
        print(f"插入失败: {e}")
        db.rollback()

def safe_get(data: dict, key: str, default=''):
    """
    安全获取字段值，若字段不存在则返回默认值。
    如果值为 "" 或 None，则统一返回 default。
    """
    value = data.get(key)
    if value is None or value == "":
        return default
    return value

def get_student_detail(student_id):
    """
    获取学生详情
    :param student_id: 学生ID
    :param retry: 最大重试次数
    :param delay: 每次重试间隔秒数
    :return: 学生详情字典 或 None
    """
    url = f"https://isus.vip/gw.managerCompany.coreStudent.get?studentId={student_id}"

    try:
        print(f"获取学生详情 - ID: {student_id}")
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            try:
                data = response.json()
                # print(data)
                student_data = data.get("result", {}) 

                if not student_data:
                    print(f"接口返回空数据 - studentId: {student_id}")
                    return None

                # 解析嵌套字段
                person = student_data.get("person", {})
                school = student_data.get("school", {})
                parsed_data = {
                    # 主表字段（isus_student_info）
                    "student_id": safe_get(student_data, "studentId"),
                    "user_id": safe_get(student_data, "userId"),
                    "student_no": safe_get(student_data, "studentNo"),
                    "identity_card_no": safe_get(student_data, "identityCardNo"),
                    "examination_card_no": safe_get(student_data, "examinationCardNo"),
                    "IDNo": safe_get(student_data, "IDNo"),
                    "email": safe_get(student_data, "email"),
                    "enroll_no": safe_get(student_data, "enrollNo"),
                    "is_resident": int(safe_get(student_data, "isResident", False)),
                    "person_id": safe_get(student_data, "personId"),
                    "family_id": safe_get(student_data, "familyId"),
                    "customer_id": safe_get(student_data, "customerId"),
                    "school_id": safe_get(student_data, "schoolId"),
                    "school_name": safe_get(school, "name", ""),
                    "grade": safe_get(student_data, "grade"),
                    "class_name": safe_get(student_data, "class"),
                    "name": safe_get(student_data, "name"),
                    "nickname": safe_get(student_data, "nickname"),
                    "gender": safe_get(student_data, "gender", 0),
                    "status": safe_get(student_data, "status", 1),
                    "student_store_id": safe_get(student_data, "studentStoreId"),
                    "created": timestamp_to_datetime(safe_get(student_data, "created")),
                    "updated": timestamp_to_datetime(safe_get(student_data, "updated")),

                    # 子表字段（isus_student_person）
                    "person": {
                        "name": safe_get(person, "name"),
                        "nickname": safe_get(person, "nickname"),
                        "gender": safe_get(person, "gender", 0),
                        "age": safe_get(person, "age", 0),
                        "birth": timestamp_to_datetime(safe_get(person, "birth")),
                        "blood": safe_get(person, "blood"),
                        "height": safe_get(person, "height", 0),
                        "weight": safe_get(person, "weight", 0),
                        "hip": safe_get(person, "hip", 0),
                        "waist": safe_get(person, "waist", 0),
                        "bust": safe_get(person, "bust", 0),
                        "vamp": safe_get(person, "vamp", 0),
                        "tarsal": safe_get(person, "tarsal", 0),
                        "avatar": safe_get(person, "avatar"),
                        "allergy": safe_get(person, "allergy"),
                        "medicine": safe_get(person, "medicine"),
                        "note": safe_get(person, "note"),
                        "type": safe_get(person, "type"),
                        "class_name": safe_get(person, "className"),
                        "grade": safe_get(person, "grade"),
                        "other": safe_get(person, "other"),
                        "foot_length": float(safe_get(person, "footLength", 0.0)),
                        "foot_type": safe_get(person, "footType"),
                        "shoe_size": safe_get(person, "shoeSize"),
                        "shoe_brand": safe_get(person, "shoeBrand"),
                        "preference": safe_get(person, "preference"),
                        "intention": safe_get(person, "intention"),
                        "contact_name": safe_get(person, "contactName"),
                        "contact_phone": safe_get(person, "contactPhone"),
                        "person_id": safe_get(person, "personId"),
                        "user_id": safe_get(person, "userId"),
                        "family_id": safe_get(person, "familyId"),
                        "customer_id": safe_get(person, "customerId"),
                        "relation": safe_get(person, "relation"),
                        "special": safe_get(person, "special", 0),
                        "created": timestamp_to_datetime(safe_get(person, "created")),
                        "updated": timestamp_to_datetime(safe_get(person, "updated"))
                    }
                }
                # print(f"成功获取学生详情 - studentId: {student_id}")
                return parsed_data

            except json.JSONDecodeError as je:
                print(f"JSON 解码失败 - studentId: {student_id}, 错误: {je}")
        else:
            print(f"HTTP 请求失败 - 状态码: {response.status_code}, studentId: {student_id}")

    except requests.RequestException as re:
        print(f"网络请求失败 - studentId: {student_id}, 错误: {re}")
        
    return None

def batch_students_detail(from_date_str, to_date_str):

    # Step 1: 查询符合条件的用户
    query_sql = """
    SELECT student_id, id
    FROM isus_student 
    WHERE created >= %s AND created <= %s order by id desc
    """
    cursor.execute(query_sql, (from_date_str, to_date_str))
    students = cursor.fetchall() 
    print(f"处理学生: {len(students)}")

    for student_row in students:
        student_id = student_row[0]
        id = student_row[1]
        # print(f"正在处理用户: {user_id}")

        detail = get_student_detail(student_id)
        if not detail:
            continue
        # 插入主表
        main_data = {
            "student_id": detail["student_id"],
            "user_id": detail["user_id"],
            "student_no": detail["student_no"],
            "identity_card_no": detail["identity_card_no"],
            "examination_card_no": detail["examination_card_no"],
            "IDNo": detail["IDNo"],
            "email": detail["email"],
            "enroll_no": detail["enroll_no"],
            "is_resident": detail["is_resident"],
            "person_id": detail["person_id"],
            "family_id": detail["family_id"],
            "customer_id": detail["customer_id"],
            "school_id": detail["school_id"],
            "school_name": detail["school_name"],
            "grade": detail["grade"],
            "class_name": detail["class_name"],
            "name": detail["name"],
            "nickname": detail["nickname"],
            "gender": detail["gender"],
            "status": detail["status"],
            "student_store_id": detail["student_store_id"],
            "created": detail["created"],
            "updated": detail["updated"]
        }
        insert_student_info(main_data)

        # 插入子表
        person_data = {
            "student_id": detail["student_id"],
            "name": detail["person"]["name"],
            "nickname": detail["person"]["nickname"],
            "gender": detail["person"]["gender"],
            "age": detail["person"]["age"],
            "birth": detail["person"]["birth"],
            "blood": detail["person"]["blood"],
            "height": detail["person"]["height"],
            "weight": detail["person"]["weight"],
            "hip": detail["person"]["hip"],
            "waist": detail["person"]["waist"],
            "bust": detail["person"]["bust"],
            "vamp": detail["person"]["vamp"],
            "tarsal": detail["person"]["tarsal"],
            "avatar": detail["person"]["avatar"],
            "allergy": detail["person"]["allergy"],
            "medicine": detail["person"]["medicine"],
            "note": detail["person"]["note"],
            "type": detail["person"]["type"],
            "class_name": detail["person"]["class_name"],
            "grade": detail["person"]["grade"],
            "other": detail["person"]["other"],
            "foot_length": detail["person"]["foot_length"],
            "foot_type": detail["person"]["foot_type"],
            "shoe_size": detail["person"]["shoe_size"],
            "shoe_brand": detail["person"]["shoe_brand"],
            "preference": detail["person"]["preference"],
            "intention": detail["person"]["intention"],
            "contact_name": detail["person"]["contact_name"],
            "contact_phone": detail["person"]["contact_phone"],
            "person_id": detail["person"]["person_id"],
            "user_id": detail["person"]["user_id"],
            "family_id": detail["person"]["family_id"],
            "customer_id": detail["person"]["customer_id"],
            "relation": detail["person"]["relation"],
            "special": detail["person"]["special"],
            "created": detail["person"]["created"],
            "updated": detail["person"]["updated"]
        }
        insert_student_person(person_data)

def insert_student_info(data):
    """
    插入主表 isus_student_info
    :param data: 包含字段的字典
    """
    student_id = data.get("student_id", "")
    user_id = data.get("user_id", "")
    student_no = data.get("student_no", "")
    identity_card_no = data.get("identity_card_no", "")
    examination_card_no = data.get("examination_card_no", "")
    IDNo = data.get("IDNo", "")
    email = data.get("email", "")
    enroll_no = data.get("enroll_no", "")
    is_resident = int(data.get("is_resident", 0))
    person_id = data.get("person_id", "")
    family_id = data.get("family_id", "")
    customer_id = data.get("customer_id", "")
    school_id = data.get("school_id", "")
    school_name = data.get("school_name", "")
    grade = data.get("grade", "")
    class_name = data.get("class_name", "")
    name = data.get("name", "")
    nickname = data.get("nickname", "")
    gender = int(data.get("gender", 0))
    status = int(data.get("status", 1))
    student_store_id = data.get("student_store_id", "")
    created = f"'{data['created']}'" if data.get("created") else 'NULL'
    updated = f"'{data['updated']}'" if data.get("updated") else 'NULL'
    current_time = datetime.now()

    sql = f"""
    INSERT INTO isus_student_info (
        student_id, user_id, student_no, identity_card_no, examination_card_no,
        IDNo, email, enroll_no, is_resident, person_id, family_id, customer_id,
        school_id, school_name, grade, class_name, name, nickname, gender, status,
        student_store_id, created, updated, created_by, created_time, deleted
    ) VALUES (
        '{student_id}', '{user_id}', '{student_no}', '{identity_card_no}', '{examination_card_no}',
        '{IDNo}', '{email}', '{enroll_no}', {is_resident}, '{person_id}', '{family_id}', '{customer_id}',
        '{school_id}', '{school_name}', '{grade}', '{class_name}', '{name}', '{nickname}', {gender}, {status},
        '{student_store_id}', {created}, {updated}, 'system', '{current_time}', 0
    )
    ON DUPLICATE KEY UPDATE
        name = '{name}',
        gender = {gender},
        school_id = '{school_id}',
        school_name = '{school_name}',
        class_name = '{class_name}',
        grade = '{grade}',
        updated = {updated},
        updated_time = NOW()
    """

    try:
        upd(sql)
    except Exception as e:
        print(f"[主表插入失败] student_id={student_id}, error={e}")

def insert_student_person(data):
    """
    插入子表 isus_student_person
    :param data: 包含字段的字典
    """
    student_id = data.get("student_id", "")
    name = data.get("name", "")
    nickname = data.get("nickname", "")
    gender = int(data.get("gender", 0))
    age = int(data.get("age", 0))
    birth = f"'{data['birth']}'" if data.get("birth") else 'NULL'
    blood = data.get("blood", "")
    height = int(data.get("height", 0))
    weight = int(data.get("weight", 0))
    hip = int(data.get("hip", 0))
    waist = int(data.get("waist", 0))
    bust = int(data.get("bust", 0))
    vamp = int(data.get("vamp", 0))
    tarsal = int(data.get("tarsal", 0))
    avatar = data.get("avatar", "")
    allergy = data.get("allergy", "")
    medicine = data.get("medicine", "")
    note = data.get("note", "")
    ptype = data.get("type", "")
    class_name = data.get("class", "")
    grade = data.get("grade", "")
    other = data.get("other", "")
    foot_length = float(data.get("foot_length", 0.0))
    foot_type = data.get("foot_type", "")
    shoe_size = data.get("shoe_size", "")
    shoe_brand = data.get("shoe_brand", "")
    preference = data.get("preference", "")
    intention = data.get("intention", "")
    contact_name = data.get("contact_name", "")
    contact_phone = data.get("contact_phone", "")
    person_id = data.get("person_id", "")
    user_id = data.get("user_id", "")
    family_id = data.get("family_id", "")
    customer_id = data.get("customer_id", "")
    relation = data.get("relation", "")
    special = int(data.get("special", 0))
    created = f"'{data['created']}'" if data.get("created") else 'NULL'
    updated = f"'{data['updated']}'" if data.get("updated") else 'NULL'
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    sql = f"""
    INSERT INTO isus_student_person (
        student_id, name, nickname, gender, age, birth, blood, height, weight,
        hip, waist, bust, vamp, tarsal, avatar, allergy, medicine, note, type,
        class_name, grade, other, foot_length, foot_type, shoe_size, shoe_brand,
        preference, intention, contact_name, contact_phone, person_id, user_id,
        family_id, customer_id, relation, special, created, updated, created_by,
        created_time, deleted
    ) VALUES (
        '{student_id}', '{name}', '{nickname}', {gender}, {age}, {birth}, '{blood}', {height}, {weight},
        {hip}, {waist}, {bust}, {vamp}, {tarsal}, '{avatar}', '{allergy}', '{medicine}', '{note}', '{ptype}',
        '{class_name}', '{grade}', '{other}', {foot_length}, '{foot_type}', '{shoe_size}', '{shoe_brand}',
        '{preference}', '{intention}', '{contact_name}', '{contact_phone}', '{person_id}', '{user_id}',
        '{family_id}', '{customer_id}', '{relation}', {special}, {created}, {updated}, 'system',
        '{current_time}', 0
    )
    ON DUPLICATE KEY UPDATE
        name = '{name}',
        nickname = '{nickname}',
        gender = {gender},
        age = {age},
        birth = {birth},
        blood = '{blood}',
        height = {height},
        weight = {weight},
        foot_length = {foot_length},
        foot_type = '{foot_type}',
        shoe_size = '{shoe_size}',
        shoe_brand = '{shoe_brand}',
        contact_name = '{contact_name}',
        contact_phone = '{contact_phone}',
        updated = {updated},
        updated_time = NOW()
    """

    try:
        upd(sql)
    except Exception as e:
        print(f"[子表插入失败] student_id={student_id}, error={e}")

if __name__ == "__main__":
   
    # 用户输入起止时间（字符串）
    from_date_str = "2024-01-01 00:00:00"
    to_date_str = "2024-12-31 23:59:59"
    # to_date_str = "2023-12-31 23:59:59"

    db = get_connection('root', '1qaz2wsx')
    # main(from_date_str, to_date_str)
    # batch_main(from_date_str, to_date_str)
    # get_student(from_date_str, to_date_str)

    # 调用批量插入
    # batch_students_detail(["stuaa8840e449fe3335"])
    batch_students_detail(from_date_str, to_date_str)

    # sql = f""""""
    # upd(sql)
    db.close()

