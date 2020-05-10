import json
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from module import dbaccess
from module import scraping
from module import message
from module import sql


def lambda_handler(event, context):

    try:
        # パラム取得
        p_dated = event["queryStringParameters"]["dated"]
        p_place = event["queryStringParameters"]["place"]
        p_round = event["queryStringParameters"]["round"]

        # レース情報取得（レース当日の情報取得のため、作業用テーブルを検索する）
        db_client = dbaccess.Dbaccess()
        race_head = db_client.execute_select(sql.Sql.select_W_RACE_HEAD_by_racekey, [p_dated, p_place, p_round])
        race_info = db_client.execute_select(sql.Sql.select_W_RACE_RACER_by_racekey, [p_dated, p_place, p_round])

        # 0件だった場合、スクレイピング
        # 成功した場合、DBへINSERTし、レース情報再セット
        if len(race_head) == 0 and len(race_info) == 0:
            url = scraping.Scraping.url_program
            scraping_client = scraping.Scraping(url, [p_dated], [p_place], [p_round])
            scraping_client.get_raceinfo_url_program()
            # スクレイピング結果が格納されていなかった場合、エラー
            scraped_data = scraping_client.out_list_header[0]
            if len(scraped_data) == 0:
                err_msg = message.Message.err2.format(p_place, p_round)
                raise Exception(err_msg)
            # ヘッダー情報をDBへINSERT
            list_param = [p_dated, p_place, p_round] + scraping_client.out_list_header[0]
            db_client.execute_insert(sql.Sql.insert_W_RACE_HEAD, list_param)
            # レース情報をDBへINSERT
            for i in range(len(scraping_client.out_list_racer[0])):
                list_param = [
                    p_dated,
                    p_place,
                    p_round,
                    i + 1,
                    scraping_client.out_list_racer[0][i],
                    scraping_client.out_list_represent[0][i],
                    scraping_client.out_list_hande[0][i],
                    scraping_client.out_list_trialrun[0][i],
                    scraping_client.out_list_deviation[0][i],
                    None
                ]
                db_client.execute_insert(sql.Sql.insert_W_RACE_RACER, list_param)
            db_client.commit()
            # 画面表示用レース情報再セット
            race_head = db_client.execute_select(sql.Sql.select_W_RACE_HEAD_by_racekey, [p_dated, p_place, p_round])
            race_info = db_client.execute_select(sql.Sql.select_W_RACE_RACER_by_racekey, [p_dated, p_place, p_round])

        # 0件だった場合、エラー
        if len(race_head) == 0 or len(race_info) == 0:
            err_msg = message.Message.err2.format(p_place, p_round)
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
                "race_info" : race_info
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
