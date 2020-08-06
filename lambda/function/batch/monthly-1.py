# 月次処理 - 1
# RDS起動（15分くらいかかる）

import json
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from module import awsmanagement
from module import message


def lambda_handler(event, context):
    try:
        # RDSが停止状態であれば、起動
        rds_client = awsmanagement.Rds()
        status = rds_client.get_status()
        print("RDSの稼働状態：" + status)
        if status == "available":
            pass
        elif status == "stopped":
            print("起動します。")
            rds_client.start()
        else:
            err_msg = message.Message.err6
            raise Exception(err_msg)

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
