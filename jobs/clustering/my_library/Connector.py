import mysql.connector as cn
from . import key

class Connector:
    # コンストラクタでコネクターを用意する
    def __init__(self):
        try:
            self.cnx = cn.connect(
                host=key.DB_HOST,
                user=key.DB_USER,
                password=key.DB_PASSWORD,
                port=key.DB_PORT,
                database=key.DB_DATABASE
            )
            self.cur = self.cnx.cursor(buffered=True, dictionary=True)
        except cn.Error as e:
            print("Error:", str(e))

    def exec_select_sql(self, sql):
        self.cur.execute(sql)
        return self.cur.fetchall()

    def exec_insert_sql(self, sql):
        self.cur.execute(sql)
        self.cnx.commit()