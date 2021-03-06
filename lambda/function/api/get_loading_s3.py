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

        # S3からハンデ情報を取得
        l_d_race_hande = []
        for file in l_file:
            for d_race_hande in csv.DictReader(s3_client.get_file(file, awsmanagement.S3.s3_bucket_data_daily)):
                l_d_race_hande.append(d_race_hande)

        # S3から予測履歴情報を取得
        file = "history.csv"
        l_d_history = []
        for d_history in csv.DictReader(s3_client.get_file(file, awsmanagement.S3.s3_bucket_data_history)):
            l_d_history.append(d_history)

        # S3から設定ファイル数を取得
        file = "setting.csv"
        l_d_setting = []
        for d_setting in csv.DictReader(s3_client.get_file(file, awsmanagement.S3.s3_bucket_data_history)):
            l_d_setting.append(d_setting)

        # レスポンス
        return {
            'statusCode': 200,
            'body': json.dumps({
                "message": "ok",
                "RaceKey": l_d_race_key,
                "RaceHande": l_d_race_hande,
                "History": l_d_history,
                "Setting": l_d_setting
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
