import json
import os, sys
import csv
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from module import awsmanagement


def lambda_handler(event, context):
    try:

        # S3からレース情報のファイル名一覧を取得
        s3_client = awsmanagement.S3()
        l_file = s3_client.get_filelist(awsmanagement.S3.s3_bucket_data_daily)
        l_d_race_key = []
        for file in l_file:
            # フォルダ名とファイル名を分割
            l_race_key = file.split("/")
            # ファイル名の拡張子（.csv）を削除
            d_race_key = {
                "place": l_race_key[0],
                "round": l_race_key[1][:-4]
            }
            l_d_race_key.append(d_race_key)

        # レスポンス
        return {
            'statusCode': 200,
            'body': json.dumps({
                "RaceKey" : l_d_race_key,
                "RaceInfo": [
                    {"place":"kawaguchi", "round":"1", "hande":"10"},
                    {"place":"kawaguchi", "round":"2", "hande":"20"},
                    {"place":"isesaki", "round":"1", "hande":"10"}
                ]
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
            'body': json.dumps(str(e))
        }

    # finally:
    #     del db_client
