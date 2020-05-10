import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../packages'))
import psycopg2
from psycopg2.extras import DictCursor


class Dbaccess:
    # DB接続情報
    connect_info = os.getenv('CONNECT_INFO')

    def __init__(self):
        self.conn = psycopg2.connect(self.connect_info)
        self.cursor = self.conn.cursor(cursor_factory=DictCursor)
        self.conn.set_client_encoding('utf-8')

    def __del__(self):
        self.conn.rollback()
        self.cursor.close()
        self.conn.close()

    # select実行し、辞書形式で返却
    def execute_select(self, sql, list_param):
        # SQL実行
        self.cursor.execute(sql, list_param)
        # 取得結果を出力
        results = self.cursor.fetchall()
        # 辞書形式で取得
        dict_result = []
        for row in results:
            dict_result.append(dict(row))

        return dict_result

    # insert文を実行
    def execute_insert(self, sql, list_param):
        # SQL実行
        self.cursor.execute(sql, list_param)

    # コミット
    def commit(self):
        self.conn.commit()
