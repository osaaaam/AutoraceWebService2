import json
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from module import dbaccess
from module import message
from module import sql


def lambda_handler(event, context):
    try:
        # パラム取得
        dated = event["queryStringParameters"]["dated"]
        place = event["queryStringParameters"]["place"]
        round = event["queryStringParameters"]["round"]
        l_race_key = [dated, place, round]

        # 過去レース情報取得
        db_client = dbaccess.Dbaccess()
        l_d_race_head = db_client.execute_select(sql.Sql.select_T_RACE_HEAD_by_racekey, l_race_key)
        l_d_race_info = db_client.execute_select(sql.Sql.select_T_RACE_RACER_by_racekey, l_race_key)
        l_d_race_result = db_client.execute_select(sql.Sql.select_T_RACE_RESULT_by_racekey, l_race_key)

        # 0件だった場合、エラー
        if len(l_d_race_head) == 0 or len(l_d_race_info) == 0 or len(l_d_race_result) == 0:
            err_msg = message.Message.err1.format(dated, place, round)
            raise Exception(err_msg)

        # レスポンス
        return {
            "headers": {
                "Access-Control-Allow-Origin" : "*",
                "Access-Control-Allow-Credentials": "true"
            },
            'statusCode': 200,
            'body': json.dumps({
                "race_head" : l_d_race_head,
                "race_info" : l_d_race_info,
                "race_result" : l_d_race_result
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

    finally:
        del db_client
