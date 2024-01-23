import pyodbc, os, logging, time
import configparser
# from dbutils.pooled_db import PooledDB
logging.basicConfig(filename="log.log", level=logging.INFO, format="%(asctime)s [%(levelname)s] (%(module)s:%(lineno)d) - %(message)s")

# class DatabaseManager:
#     def __init__(self, connection_string):
#         # 创建连接池
#         self.pool = PooledDB(
#             creator=pyodbc,  # 指定使用的数据库驱动
#             mincached=1,     # 最小空闲连接数
#             maxcached=5,     # 最大空闲连接数
#             maxshared=5,     # 最大共享连接数
#             blocking=True,   # 阻塞等待连接
#             dsn=connection_string  # 连接字符串
#         )

#     def execute_query(self, query):
#         try:
#             # 从连接池获取连接
#             conn = self.pool.connection()

#             # 执行查询
#             cursor = conn.cursor()
#             cursor.execute(query)
#             result = cursor.fetchall()

#             return result
#         except pyodbc.Error as e:
#             print(f"Error executing query: {str(e)}")
#             return []
#         finally:
#             # 在完成后关闭连接
#             if conn:
#                 conn.close()

def connect_to_database(connection_string):
    try:
        conn = pyodbc.connect(connection_string)
        print("Connected to SQL Server successfully.")
        return conn
    except pyodbc.Error as e:
        print(f"Error connecting to SQL Server: {str(e)}")
        return None

# def create_connection_pool(connection_string, pool_size=5):
#     return pyodbc.pool.ConnectionPool(connection_string, maxconnections=pool_size)

# def execute_query(connection_pool, query):
#     try:
#         with connection_pool.connect() as conn:
#             cursor = conn.cursor()
#             cursor.execute(query)
#             rows = cursor.fetchall()
#             return rows
#     except pyodbc.Error as e:
#         print(f"Error executing query: {str(e)}")
#         return []
    
def execute_query(conn, query):
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        # print("Query executed successfully.", query)
        # 提取查询结果
        result = cursor.fetchall()
        # print(cursor.fetchall())
        return result
    except pyodbc.Error as e:
        print(f"Error executing query: {str(e)}")
        return False
    finally:
        # 在完成后关闭连接
        if conn:
            conn.close()

def insert_data(conn, table_name, data):
    query = f"INSERT INTO {table_name} VALUES ({', '.join(['?'] * len(data))})"
    return execute_query(conn, query, data)

def update_data(conn, table_name, data, condition):
    query = f"UPDATE {table_name} SET {', '.join([f'{key}=?' for key in data.keys()])} WHERE {condition}"
    return execute_query(conn, query, list(data.values()))

def delete_data(conn, table_name, condition):
    query = f"DELETE FROM {table_name} WHERE {condition}"
    return execute_query(conn, query)

def create_sql_server_connection():
    server, username, password, database = load_credentials(config())
    # 构建连接字符串
    connection_string = f"Driver={{SQL Server Native Client 11.0}};Server={server};Database={database};UID={username};PWD={password}"

    try:
        conn = pyodbc.connect(connection_string, user=username, password=password)
        print("Connected to SQL Server successfully.")
        return conn
    except pyodbc.Error as e:
        print(f"Error connecting to SQL Server: {str(e)}")
        return None

def load_credentials(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)

    if 'Database' in config:
        server = config['Database'].get('server')
        username = config['Database'].get('username')
        password = config['Database'].get('password')
        database = config['Database'].get('database')
        return server, username, password, database
    else:
        return None, None, None, None

def config():
    # 获取当前脚本所在目录
    script_directory = os.path.dirname(os.path.abspath(__file__))
    # 构建配置文件路径
    return os.path.join(script_directory, './100.89.ini')

if __name__ == '__main__': 
    # 指定配置文件的路径
    # config_file = 'config.ini'

    # 加载配置文件中的数据库连接信息

    # # 创建数据库管理器实例
    # db_manager = DatabaseManager(connection_string)

    # 示例查询
    query = '''
        SELECT JHD.BYZD3 E3通知单, JHD.YDJH 源单据, CONVERT(varchar, JHD.RQ, 111) 进货单日期, JHD.DJBH 单据编号, JHDMX.SPDM 商品代码, SP.SPMC 商品名称, JHDMX.GG1DM 款型代码, GG1.GGMC 款型, JHDMX.GG2DM 尺码代码, GG2.GGMC 尺码, JHDMX.SL 数, JHDMX.SL_2 通知数, ABS(JHDMX.SL-JHDMX.SL_2) 差异数量, JHDMX.DJ 单价
        FROM SPJHD JHD
        LEFT JOIN SPJHDMX JHDMX ON JHDMX.DJBH = JHD.DJBH
        LEFT JOIN SHANGPIN SP ON SP.SPDM = JHDMX.SPDM 
        LEFT JOIN GUIGE1 GG1 ON GG1.GGDM = JHDMX.GG1DM
        LEFT JOIN GUIGE2 GG2 ON GG2.GGDM = JHDMX.GG2DM
        WHERE 1=1
        AND JHD.RQ >= '2023-09-01 00:00:00.000' 
        AND JHD.BYZD3 IS NOT NULL
        ORDER BY JHD.RQ DESC
    '''
    conn = create_sql_server_connection()
    time.sleep(3)
    result = execute_query(conn, query)
    for row in result:
        print(row)
