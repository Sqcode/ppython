import pymssql, configparser, os
from dbutils.pooled_db import PooledDB

class DatabaseManager:
    def __init__(self, min_connections=1, max_connections=5):
        server, user, password, database = load_credentials(config())
        # 创建连接池
        self.pool = PooledDB(
            creator=pymssql,  # 使用 pymssql 作为连接库
            mincached=min_connections,  # 最小空闲连接数
            maxcached=max_connections,  # 最大空闲连接数
            host=server,  # 数据库服务器地址
            user=user,  # 用户名
            password=password,  # 密码
            database=database,  # 数据库名称
        )

    def execute_query(self, query, params=None):
        try:
            # 从连接池获取连接
            conn = self.pool.connection()
            cursor = conn.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            conn.commit()
            print("Query executed successfully.")
            
            # 提取查询结果
            result = cursor.fetchall()
            return result
        except pymssql.Error as e:
            print(f"Error executing query: {str(e)}")
            return None
        finally:
            if conn:
                conn.close()

    # 可以添加其他执行操作的方法，如增删改
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

# 示例用法
if __name__ == "__main__":
    # 创建数据库管理器实例

    connect=pymssql.connect(server='192.168.100.89',user='sa',password='Admin123',database='DRP2014')
    #服务器名，账号，密码，数据库名
    if connect:
        print("连接数据库成功！")
        
    # db_manager = DatabaseManager()

    # # 示例查询
    # query = '''
    #     SELECT JHD.BYZD3 E3通知单, JHD.YDJH 源单据, CONVERT(varchar, JHD.RQ, 111) 进货单日期, JHD.DJBH 单据编号, JHDMX.SPDM 商品代码, SP.SPMC 商品名称, JHDMX.GG1DM 款型代码, GG1.GGMC 款型, JHDMX.GG2DM 尺码代码, GG2.GGMC 尺码, JHDMX.SL 数, JHDMX.SL_2 通知数, ABS(JHDMX.SL-JHDMX.SL_2) 差异数量, JHDMX.DJ 单价
    #     FROM SPJHD JHD
    #     LEFT JOIN SPJHDMX JHDMX ON JHDMX.DJBH = JHD.DJBH
    #     LEFT JOIN SHANGPIN SP ON SP.SPDM = JHDMX.SPDM 
    #     LEFT JOIN GUIGE1 GG1 ON GG1.GGDM = JHDMX.GG1DM
    #     LEFT JOIN GUIGE2 GG2 ON GG2.GGDM = JHDMX.GG2DM
    #     WHERE 1=1
    #     AND JHD.RQ >= '2023-09-01 00:00:00.000' 
    #     AND JHD.BYZD3 IS NOT NULL
    #     ORDER BY JHD.RQ DESC
    # '''
    # query_result = db_manager.execute_query(query)

    # if query_result:
    #     for row in query_result:
    #         print(row)
