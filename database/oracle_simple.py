import cx_Oracle

class OracleDatabase:
    def __init__(self, username, password, host, port, service_name):
        self.connection = cx_Oracle.connect(f"{username}/{password}@{host}:{port}/{service_name}")
        self.cursor = self.connection.cursor()

    def execute_query(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except cx_Oracle.DatabaseError as e:
            self.connection.rollback()
            raise e

    def execute_update(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
        except cx_Oracle.DatabaseError as e:
            self.connection.rollback()
            raise e

    def insert(self, table, columns, values):
        query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join([':'+col for col in columns])})"
        self.execute_update(query, dict(zip(columns, values)))

    def update(self, table, set_columns, set_values, where_column, where_value):
        query = f"UPDATE {table} SET {', '.join([col+'=:'+col for col in set_columns])} WHERE {where_column}=:where_val"
        params = dict(zip(set_columns, set_values))
        params['where_val'] = where_value
        self.execute_update(query, params)

    def delete(self, table, where_column, where_value):
        query = f"DELETE FROM {table} WHERE {where_column}=:where_val"
        self.execute_update(query, {'where_val': where_value})

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


    def close(self):
        self.cursor.close()
        self.connection.close()

# if __name__ == '__main__':
#     db = OracleDatabase("system", "root_R00t", "192.168.100.26", "1521", "ORCL")
#    # db = OracleDatabase("username", "password", "host", "port", "server_name")
    
#     try:
#         # 查询数据
#         result = db.select("KINGDEE00.T_BD_UNIT_L", ["FUNITID", "FNAME", "FDESCRIPTION"], "FNAME", '米')
#         print(result)

#     except cx_Oracle.DatabaseError as e:
#         print("Error:", e)


    # try:
    #     # 添加事务
    #     db.connection.begin()

    #     # # 插入数据
    #     # db.insert("employees", ["emp_id", "emp_name"], [101, "John Doe"])

    #     # # 更新数据
    #     # db.update("employees", ["emp_name"], ["Jane Smith"], "emp_id", 101)

    #     # 查询数据
    #     result = db.select("employees", ["emp_id", "emp_name"], "emp_id", 101)
    #     print(result)

    #     # # 删除数据
    #     # db.delete("employees", "emp_id", 101)

    #     # 提交事务
    #     db.connection.commit()

    # except cx_Oracle.DatabaseError as e:
    #     print("Error:", e)
    #     db.connection.rollback()

    # db.close()
