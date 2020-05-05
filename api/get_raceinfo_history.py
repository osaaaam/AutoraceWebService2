import json
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from module import dbaccess
from module import message
from module import sql


def lambda_handler(event, context):

    try:
        # パラム取得
        p_dated = event["queryStringParameters"]["dated"]
        p_place = event["queryStringParameters"]["place"]
        p_round = event["queryStringParameters"]["round"]

        # レース情報取得
        db_client = dbaccess.Dbaccess()
        race_head = db_client.execute_select(sql.Sql.select_T_RACE_HEAD_by_racekey, [p_dated, p_place, p_round])
        race_info = db_client.execute_select(sql.Sql.select_T_RACE_RACER_by_racekey, [p_dated, p_place, p_round])
        race_result = db_client.execute_select(sql.Sql.select_T_RACE_RESULT_by_racekey, [p_dated, p_place, p_round])

        # 0件だった場合、エラー
        if len(race_head) == 0 or len(race_info) == 0 or len(race_result) == 0:
            err_msg = message.Message.err1.format(p_dated, p_place, p_round)
            raise Exception(err_msg)

        # レスポンス
        return {
            "headers": {
                "Access-Control-Allow-Origin" : "*",
                "Access-Control-Allow-Credentials": "true"
            },
            'statusCode': 200,
            'body': json.dumps({
                "race_head" : race_head,
                "race_info" : race_info,
                "race_result" : race_result
            })
        }

    except Exception as e:
        print(e)
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
