import requests,random, time, pymysql
import json
import pandas as pd
from datetime import datetime
import os, time, requests, random, telnetlib, json, pypinyin, cv2, traceback
__dir__ = os.path.dirname(os.path.abspath(__file__))
# print(__dir__)
from bs4 import BeautifulSoup
from openpyxl import Workbook

from urllib.parse import urlparse
def format_timestamp(ms):
    if ms is None or not isinstance(ms, (int, float)):
        return ""  # 返回空字符串或者 "未知"
    try:
        return datetime.fromtimestamp(ms / 1000).strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        print(f"⚠️ 时间戳转换失败: {e}, 原始值: {ms}")
        return ""
    
def fetch_material_data(page_num, page_size=20):
    global db
    # 1. 设置请求参数
    url = 'https://hope.demogic.com/api-marketing/content/page-material?requestProject=marketing'  # 替换为你的目标URL
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Content-Type': 'application/json',
        'Cookie': 'JSESSIONID=49E256C895C43E6CC2E4DE1AC7B9084C; Path=/; _abfpc=a47a63c4e9475b910f4d83b1aeab359ce402ec05_2.0; cna=d0c1f4faa09a6df69841a72d66beea34; enterpriseId=ff8080816f3345d5016f59b7fdb87bf0; tgw_l7_route=24c4e1fc660a6b84af415ca53882223e; web_login_cookie_id=ff8080816f42af5a016f59b8021934eb; web_login_cookie_id_last_login_time=1749792582047'  # 替换为你需要设置的 Cookie 值
    }
    # 如果你有登录等操作，也可以通过会话自动管理 Cookie
    # session = requests.Session()
    # session.post('https://example.com/login', data={"username": "xxx", "password": "xxx"})
    # response = session.post(url, headers=headers, json=payload)
# ,"materialSourceList":null "topFlag":null,
    # payload = {"search":"","relationGoodsStatus":"","materialType":"","publishStatus":"","producerId":"","contentCategoryId":"","contentCategoryIdList":[],"contentTagId":"","goodsId":"","pageNum":1,"pageSize":20,"showSelfFlag":0,"orderField":"","order":"","queryScene":1,"contentColumnId":"","producerUserId":"","creatorName":""}
    payload = {"pageNum":page_num,"pageSize":page_size,"queryScene":1, "search":""}
    # payload = {"pageNum":page_num,"pageSize":page_size,"queryScene":1, "search":""}

    # 2. 发送 POST 请求
    response = requests.post(url, headers=headers, json=payload)

    # 3. 检查响应状态码
    if response.status_code == 200:
        result = response.json()
        if result.get("code") == "0":
            print(f"✅ 第 {page_num} 页请求成功，共获取 {len(result['result']['result'])} 条数据")
            return result['result']['result']
        else:
            print(f"❌ 第 {page_num} 页请求失败，错误信息：{result.get('message')}")
            return []
    else:
        print(f"⚠️ HTTP 错误码：{response.status_code}")
        return []

# 创建资源存储目录
RESOURCE_DIR = "./resources"
os.makedirs(RESOURCE_DIR, exist_ok=True)

def download_resource(url, title, material_id):
    if not url or url == "":
        print(f"⚠️ 空链接，跳过: {title}")
        return

    # 获取扩展名
    parsed_url = urlparse(url)
    ext = os.path.splitext(parsed_url.path)[1].lstrip('.')  # 提取后缀，如 jpg、mp4
    if not ext:
        ext = "bin"  # 默认二进制格式

    filename = f"{title}_{material_id}.{ext}"
    
    # 创建标题文件夹： ./resources/标题/
    title_dir = os.path.join(RESOURCE_DIR, title)
    os.makedirs(title_dir, exist_ok=True)
    
    filepath = os.path.join(title_dir, filename)

    try:
        print(f"📥 正在下载: {filename}")
        response = requests.get(url, stream=True, timeout=10)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            print(f"✅ 已保存至: {filepath}")
        else:
            print(f"❌ 下载失败，HTTP状态码: {response.status_code}")
    except Exception as e:
        print(f"🚫 下载出错: {e}")
def parse_material(item):
    return {
        'content_material_id': item.get('contentMaterialId'),
        'material_image_urls': item.get('materialImageUrls'),
        'material_video_url': item.get('materialVideoUrl'),
        'material_title': item.get('materialTitle'),
        'material_sub_title': item.get('materialSubTitle'),
        'publish_begin_time': format_timestamp(item.get('publishBeginTime')),
        'publish_end_time': format_timestamp(item.get('publishEndTime')),
        'material_content': item.get('materialContent'),
        'create_time': format_timestamp(item.get('createTime')),
        'update_time': format_timestamp(item.get('updateTime')),

        # 处理 contentTagList
        'tags': ",".join(
            [tag.get('contentTagName', '') for tag in (item.get('contentTagList') or []) if tag.get('contentTagName')]
        ),

        # contentCategory
        'category_id': item.get('contentCategory', {}).get('contentCategoryId'),
        'category_name': item.get('contentCategory', {}).get('contentCategoryName'),

        # columnList
        'column_list': ",".join(
            [col.get('contentColumnName', '') for col in (item.get('columnList') or []) if col.get('contentColumnName')]
        ),

        # relationList
        'related_titles': ",".join(
            [rel.get('materialTitle', '') for rel in (item.get('relationList') or []) if rel.get('materialTitle')]
        )
    }
    
def main():
    global db
    PAGE_SIZE = 20
    CURRENT_PAGE = 1
    all_items = []

    while True:
        print(f"\n👉 正在抓取第 {CURRENT_PAGE} 页数据...")
        items = fetch_material_data(CURRENT_PAGE, PAGE_SIZE)

        if not items:
            print("🔚 没有更多数据了")
            break

        parsed_items = [parse_material(item) for item in items]
        all_items.extend(parsed_items)

        # 批量写入数据库
        df = pd.DataFrame(parsed_items)
        # 将 DataFrame 转为字典列表
        records = df.to_dict(orient='records')
        # 构造 SQL 插入语句并执行
        for record in records:
            sql = f"""INSERT INTO gic_source (
                content_material_id, 
                material_image_urls,
                material_video_url,
                material_title,
                material_sub_title,
                publish_begin_time,
                publish_end_time,
                material_content,
                create_time,
                update_time,
                tags,
                category_id,
                category_name,
                column_list,
                related_titles
            ) VALUES (
                {f"'{record.get('content_material_id')}'" if record.get('content_material_id') else 'NULL'},
                {f"'{record.get('material_image_urls')}'" if record.get('material_image_urls') else 'NULL'},
                {f"'{record.get('material_video_url')}'" if record.get('material_video_url') else 'NULL'},
                {f"'{record.get('material_title')}'" if record.get('material_title') else 'NULL'},
                {f"'{record.get('material_sub_title')}'" if record.get('material_sub_title') else 'NULL'},
                {f"'{record.get('publish_begin_time')}'" if record.get('publish_begin_time') else 'NULL'},
                {f"'{record.get('publish_end_time')}'" if record.get('publish_end_time') else 'NULL'},
                {f"'{record.get('material_content')}'" if record.get('material_content') else 'NULL'},
                {f"'{record.get('create_time')}'" if record.get('create_time') else 'NULL'},
                {f"'{record.get('update_time')}'" if record.get('update_time') else 'NULL'},
                {f"'{record.get('tags')}'" if record.get('tags') else 'NULL'},
                {f"'{record.get('category_id')}'" if record.get('category_id') else 'NULL'},
                {f"'{record.get('category_name')}'" if record.get('category_name') else 'NULL'},
                {f"'{record.get('column_list')}'" if record.get('column_list') else 'NULL'},
                {f"'{record.get('related_titles')}'" if record.get('related_titles') else 'NULL'}
            )
            """
            upd(sql)
                    # sql = f"""Insert into gic_member_log (`log_id`,`create_time`,`oper_type`,`oper_content`,`oper_reason`,`oper_remark`,`refer_log_id`,`member_id`) 
        # values ('{item['logId']}','{item['createTime']}','{item['operType']}','{item['operContent']}','{item['operReason']}', '{item['operRemark']}', '{item['referLogId']}','{memberId}')"""
                    # upd(sql)
                
        # df.to_sql(name='gic_source', con=db, if_exists='append', index=False, method='multi', chunksize=1000)
        # print(f"✅ 第 {CURRENT_PAGE} 页共 {len(items)} 条数据已写入数据库")
        # 下载资源
        # for item in items:
        #     title = item.get('materialTitle')
        #     material_id = item.get('contentMaterialId')
            
        #     # 处理图片链接（可能包含多个链接）
        #     image_urls = item.get('materialImageUrls', '')
        #     if image_urls:  # 确保不是空字符串或None
        #         image_urls_list = [url.strip() for url in image_urls.split(',')]  # 分割并去除每项两端的空白字符
        #         for idx, image_url in enumerate(image_urls_list):
        #             download_resource(image_url, title, f"{material_id}_{idx}")  # 使用索引区分不同图片
            
        #     # 处理视频链接
        #     video_url = item.get('materialVideoUrl')
        #     if video_url:
        #         download_resource(video_url, title, material_id)
        # 控制频率
        delay = random.uniform(0.5, 1.5)
        print(f"⏱️ 等待 {delay:.2f} 秒后继续...")
        time.sleep(delay)

        CURRENT_PAGE += 1

        # 如果当前页数据不足一页，停止
        if len(items) < PAGE_SIZE:
            break

    print(f"\n🎉 总共抓取并保存 {len(all_items)} 条素材数据。")
        #             sql = f"""Insert into gic_member_log (`log_id`,`create_time`,`oper_type`,`oper_content`,`oper_reason`,`oper_remark`,`refer_log_id`,`member_id`) 
        # values ('{item['logId']}','{item['createTime']}','{item['operType']}','{item['operContent']}','{item['operReason']}', '{item['operRemark']}', '{item['referLogId']}','{memberId}')"""
        #             upd(sql)
                						
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
    main()
    # sql = f"""Insert into gic_member_log (`log_id`,`create_time`,`oper_type`,`oper_content`,`oper_reason`,`oper_remark`,`refer_log_id`,`member_id`) 
    #     values ('111','2025-06-12 14:27:19','333','444','555', '666', '777','888')"""
    # upd(sql)
    # start()

    db.close()
    # start()
    # data = get("2024-06-13", "2025-06-12", "00000000909d0f200190a72fd282044a")
    # print(data)