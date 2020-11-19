# 月次処理 - 5
# 月次選手ワークテーブルの再作成

import json
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from module import dbaccess
from module import sql


def lambda_handler(event, context):
    try:

        # テーブルデータ再作成
        db_client = dbaccess.Dbaccess()
        db_client.execute_delete(sql.Sql.delete_W_MONTHLY_RACER, [])
        db_client.execute_insert(sql.Sql.insert_W_MONTHLY_RACER, [])
        db_client.commit()

        # レスポンス
        return {
            'statusCode': 200,
            'body': json.dumps("ok")
        }

    except Exception as e:
        print(str(e))
        # レスポンス
        return {
            'statusCode': 400,
            'body': json.dumps("ng")
        }

    finally:
        del db_client
