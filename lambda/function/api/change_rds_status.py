import json
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from module import awsmanagement


def lambda_handler(event, context):
    try:
        # RDSのステータス確認
        rds_client = awsmanagement.Rds()
        status = rds_client.get_status()
        # RDSが稼働中であれば、停止
        if status == "available":
            rds_client.stop()
        # RDSが停止であれば、開始
        elif status == "stopped":
            rds_client.start()

        # レスポンス
        return {
            "headers": {
                "Access-Control-Allow-Origin" : "*",
                "Access-Control-Allow-Credentials": "true"
            },
            'statusCode': 200,
            'body': json.dumps(status)
        }

    except Exception as e:
        print(str(e))
        # レスポンス
        return {
            "headers": {
                "Access-Control-Allow-Origin" : "*",
                "Access-Control-Allow-Credentials": "true"
            },
            'statusCode': 400,
            'body': json.dumps(str(e))
        }
