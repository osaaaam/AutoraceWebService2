import json
import os, sys
import csv
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from module import awsmanagement


def lambda_handler(event, context):
    try:

        # S3からレース情報のファイル名一覧を取得
        s3_client = awsmanagement.S3()
        l_file = s3_client.get_file("川口/11R.csv", awsmanagement.S3.s3_bucket_data_anaylize)

        l_d_anaylize = []
        for d_anaylize in csv.DictReader(s3_client.get_file("川口/11R.csv", awsmanagement.S3.s3_bucket_data_anaylize)):
            l_d_anaylize.append(d_anaylize)

        # レスポンス
        return {
            'statusCode': 200,
            'body': json.dumps({
                "message": "ok",
                "Anaylize": l_d_anaylize
            })
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
            'body': json.dumps({
                "message": str(e)
            })
        }

    # finally:
    #     del db_client
