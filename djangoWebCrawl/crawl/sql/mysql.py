import pymysql
import time

class SQL:

    def __init__(self, database, table):
        self.database = database
        self.conn = pymysql.connect(host='localhost', user='root', password='1999',
                                    charset='utf8')
        self.table = table

    def enter_database(self):
        query_add_db = f"CREATE DATABASE IF NOT EXISTS {self.database}"
        cursor = self.conn.cursor()
        cursor.execute(query_add_db)
        self.conn.select_db(self.database)
        self.conn.commit()

    def drop_table(self):
        query_drop = f"DROP TABLE IF EXISTS {self.table}"
        cursor = self.conn.cursor()
        cursor.execute(query_drop)
        self.conn.commit()

    def enter_table(self):
        query_add = f"CREATE TABLE IF NOT EXISTS {self.table} (" \
                    f"date VARCHAR(10)," \
                    f"id VARCHAR(20) PRIMARY KEY," \
                    f"Image VARCHAR(1000) ," \
                    f"Title VARCHAR(1000)," \
                    f"price VARCHAR(1000)," \
                    f"offer_url VARCHAR(1000)," \
                    f"已售 FLOAT," \
                    f"评价数目 FLOAT," \
                    f"好评率 FLOAT," \
                    f"服务能力 FLOAT," \
                    f"回头率 FLOAT," \
                    f"旺旺响应 FLOAT," \
                    f"经营模式 VARCHAR(1000)," \
                    f"办公规模 FLOAT," \
                    f"员工人数 FLOAT," \
                    f"重量 FLOAT)"
        cursor = self.conn.cursor()
        cursor.execute(query_add)
        self.conn.commit()

    def query_data(self, col_name):
        query = f"SELECT {col_name} from {self.table}"
        cursor = self.conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def insertData(self, id, img, title, price):
        query = f'''
                                    insert ignore into {self.table} (date,id,Image,Title,price)
                                    values("{time.strftime('%Y-%m-%d', time.localtime())}","{id}","{img}","{title}","{price}")
                                '''
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()

    def generalInsert(self, field: str, val: str):
        query = f'''
                    insert ignore into {self.table} {field}
                    values {val}
                '''
        print(query)
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()

    def add_col(self, col_name, after_name, input_type):
        query = f'ALTER TABLE {self.table} ADD COLUMN {col_name} {input_type} AFTER {after_name}'
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()

    def drop_col(self, col_name):
        query = f"ALTER TABLE {self.table} DROP COLUMN {col_name}"
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()

    def count_rows(self):
        query = f"SELECT COUNT(*) FROM {self.table}"
        cursor = self.conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()[0][0]

    def update_table(self, col_name, data, key_name, key, stage):
        if stage == 2:
            for i in range(len(col_name)):
                query = f'''
                                                    UPDATE {self.table}
                                                    SET {col_name[i]} = "{data[i]}"
                                                    WHERE {key_name} = "{key}"
                                                    '''

        elif stage == 3:
            query = f'''
                    UPDATE {self.table}
                    SET 
                        {col_name[0]} = "{data[0]}",
                        {col_name[1]} = "{data[1]}",
                        {col_name[2]} = "{data[2]}",
                        {col_name[3]} = "{data[3]}",
                        {col_name[4]} = "{data[4]}",
                        {col_name[5]} = "{data[5]}",
                        {col_name[6]} = "{data[6]}",
                        {col_name[7]} = "{data[7]}",
                        {col_name[8]} = "{data[8]}",
                        {col_name[9]} = "{data[9]}",
                        {col_name[10]} = "{data[10]}"
                    WHERE 
                        {key_name} = "{key}"
                    '''
        else:
            set_q = ''
            for i in range(2):
                if i == 0:
                    set_q = set_q + f'{col_name[i]} = "{data[i]}"'
                else:
                    set_q = set_q + f',{col_name[i]} = "{data[i]}"'

            query = f'''
                                UPDATE {self.table}
                                SET 
                                    {set_q}
                                WHERE 
                                    {key_name} = "{key}"
                                '''
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
