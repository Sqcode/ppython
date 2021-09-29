import pymysql

def get_connection(user, pwd, host='localhost', database='mysql'):
    # 打开数据库连接
    global db
    db = pymysql.connect(host=host, user=user, password=pwd, database=database)
    return db

def get_cursor():
    global cursor
    cursor = db.cursor()

def get_data(sql):
    cursor.execute(sql)
    return cursor.fetchall()

def upd(sql):
    try:
        # 执行SQL语句
        cursor.execute(sql)
    # 提交到数据库执行
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()


db = pymysql.connect(host='localhost', user='root', password='root', database='sqc')

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用 execute()  方法执行 SQL 查询
cursor.execute("SELECT * from user")

# 使用 fetchone() 方法获取单条数据.
data = cursor.fetchall()

print(f"result : {data}")

# 关闭数据库连接
db.close()
