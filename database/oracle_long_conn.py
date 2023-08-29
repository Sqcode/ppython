import cx_Oracle
from cx_Oracle import Connection, Cursor
from typing import List, Tuple, Any
import configparser

import sys, os
# __dir__ = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(__dir__)
# sys.path.append(os.path.abspath(os.path.join(__dir__, '../database')))

class OracleDatabase:
    def __init__(self, config_path: str):
        self.config = configparser.ConfigParser()
        self.config.read(config_path)
        
        self.username = self.config.get('Database', 'username')
        self.password = self.config.get('Database', 'password')
        self.host = self.config.get('Database', 'host')
        self.port = self.config.get('Database', 'port')
        self.service_name = self.config.get('Database', 'service_name')
        self.min_connections = self.config.getint('Database', 'min_connections')
        self.max_connections = self.config.getint('Database', 'max_connections')
        
        dsn = cx_Oracle.makedsn(self.host, self.port, service_name=self.service_name)
        self.connection_pool = cx_Oracle.SessionPool(user=self.username, password=self.password, dsn=dsn, min=self.min_connections, max=self.max_connections)
    
    def execute_query(self, query: str, params: Tuple = None) -> List[Tuple]:
        connection: Connection = self.connection_pool.acquire()
        cursor: Cursor = connection.cursor()
        
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            result: List[Tuple] = cursor.fetchall()
            return result
        
        finally:
            cursor.close()
            self.connection_pool.release(connection)
    
    def select(self, table, columns=None, where_column=None, where_value=None):
        query = f"SELECT {', '.join(columns) if columns else '*'} FROM {table}"
        if where_column and where_value:
            query += f" WHERE {where_column}=:where_val"
            return self.execute_query(query, {'where_val': where_value})
        else:
            return self.execute_query(query)
    
    def select_with_conditions(self, table, columns=None, conditions=None):
            query = f"SELECT {', '.join(columns) if columns else '*'} FROM {table}"

            if conditions:
                where_clause = " AND ".join([f"{col} = :{col}" for col in conditions])
                query += f" WHERE {where_clause}"
            return self.execute_query(query, conditions)
    # ... 其他方法 ...
    def close(self):
        self.connection_pool.close()

def conn():
    # 获取当前脚本所在目录
    script_directory = os.path.dirname(os.path.abspath(__file__))
    # 构建配置文件路径
    # return os.path.join(script_directory, '..', 'database', 'kd_config.ini')
    return os.path.join(script_directory, './kd_config.ini')

# if __name__ == '__main__':
    # db = OracleDatabase(conn())

    # try:
    #     # 查询数据
    #     # result = db.select("KINGDEE00.T_BD_UNIT_L", ["FUNITID", "FNAME", "FDESCRIPTION"], "FNAME", '米')
    #     # print(result)

    #     # query = "SELECT a as b FROM tablename WHERE column_name = :value"
    #     # params = {"value": "some_value"}

    #     # query = '''
    #     # SELECT TBU.FUNITID, TBU.FNUMBER, TBUL.FNAME 
    #     # FROM KINGDEE00.T_BD_UNIT TBU LEFT JOIN KINGDEE00.T_BD_UNIT_L TBUL ON TBUL.FUNITID = TBU.FUNITID 
    #     # WHERE TBU.FFORBIDSTATUS = 'A' AND TBU.FDOCUMENTSTATUS = 'C' AND TBUL.FNAME IN ('Pcs', '条', '件') 
    #     # '''
    #     # params = {}

    #     # query = '''
    #     # SELECT TBU.FUNITID, TBU.FNUMBER, TBUL.FNAME 
    #     # FROM KINGDEE00.T_BD_UNIT TBU LEFT JOIN KINGDEE00.T_BD_UNIT_L TBUL ON TBUL.FUNITID = TBU.FUNITID 
    #     # WHERE TBU.FFORBIDSTATUS = 'A' AND TBU.FDOCUMENTSTATUS = 'C' AND TBUL.FNAME= :FNAME
    #     # '''
    #     # params = {"FNAME": "条"}

    #     units = ["Pcs", "条", "件"]

    #     # 构建 IN 条件字符串
    #     in_units = ', '.join(':' + str(i + 1) for i in range(len(units)))
    #     query = f'''
    #     SELECT TBU.FUNITID, TBU.FNUMBER, TBUL.FNAME 
    #     FROM KINGDEE00.T_BD_UNIT TBU LEFT JOIN KINGDEE00.T_BD_UNIT_L TBUL ON TBUL.FUNITID = TBU.FUNITID 
    #     WHERE TBU.FFORBIDSTATUS = 'A' AND TBU.FDOCUMENTSTATUS = 'C' AND TBUL.FNAME IN ({in_units})
    #     '''
    #     result = db.execute_query(query, units)
    #     print(query, result)
    
    # except cx_Oracle.DatabaseError as e:
    #     print("Error:", e)
    # finally:
    #     db.close()  # 在这里调用 close() 方法关闭连接池
