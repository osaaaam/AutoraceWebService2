# 月次処理 - 9
# RDS停止

import json
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from module import awsmanagement
from module import message


def lambda_handler(event, context):
    try:
        # RDSが稼働中であれば、停止
        rds_client = awsmanagement.Rds()
        status = rds_client.get_status()
        if status == "available":
            pass
        elif status == "stopped":
            rds_client.start
        else:
            err_msg = message.Message.err7
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
