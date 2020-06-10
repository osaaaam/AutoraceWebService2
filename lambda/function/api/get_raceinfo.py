import json
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from module import dbaccess
from module import message
from module import scraping
from module import sql


# スクレイピングして、成功したら、DBへINSERT
def scraped_insert(db_client, l_race_key):
    url = scraping.Scraping.url_program
    scraping_client = scraping.Scraping(url, [l_race_key[0]], [l_race_key[1]], [l_race_key[2]])
    scraping_client.get_raceinfo_by_url_program()
    # スクレイピング結果が格納されていなかった場合、エラー
    if len(scraping_client.out_l_header) == 0:
        return False
    else:
        # ヘッダー情報をDBへINSERT
        l_param = l_race_key + scraping_client.out_l_header
        db_client.execute_insert(sql.Sql.insert_W_RACE_HEAD, l_param)
        # レース情報をDBへINSERT
        for i in range(len(scraping_client.out_l_racer)):
            l_param = l_race_key + [
                i + 1,
                scraping_client.out_l_racer[i],
                scraping_client.out_l_represent[i],
                scraping_client.out_l_hande[i],
                scraping_client.out_l_trialrun[i],
                scraping_client.out_l_deviation[i],
                scraping_client.out_l_position_x[i],
                scraping_client.out_l_position_y[i]
            ]
            db_client.execute_insert(sql.Sql.insert_W_RACE_INFO, l_param)
        return True


def check_exist_data(l_d_race_head, l_d_race_info):
    # 0件の場合
    if len(l_d_race_head) == 0 and len(l_d_race_info) == 0:
        return False
    # 試走が出ていない
    for d_race_info in l_d_race_info:
        if d_race_info["試走タイム"] is None:
            return False
    return True


def lambda_handler(event, context):
    try:
        # パラム取得
        dated = event["queryStringParameters"]["dated"]
        place = event["queryStringParameters"]["place"]
        round = event["queryStringParameters"]["round"]
        l_race_key = [dated, place, round]

        # レース情報取得（レース当日の情報取得のため、作業用テーブルを検索する）
        db_client = dbaccess.Dbaccess()
        l_d_race_head = db_client.execute_select(sql.Sql.select_W_RACE_HEAD_for_view, l_race_key)
        l_d_race_info = db_client.execute_select(sql.Sql.select_W_RACE_INFO_for_view, l_race_key)

        # 0件だった場合、試走タイムが出ていなかった場合、DELETE → スクレイピング → INSERT
        # 成功した場合、画面表示用にレース情報を再セット
        if check_exist_data(l_d_race_head, l_d_race_info) == False:
            db_client.execute_delete(sql.Sql.delete_W_RACE_HEAD_by_racekey, l_race_key)
            db_client.execute_delete(sql.Sql.delete_W_RACE_INFO_by_racekey, l_race_key)
            flg_scraped_insert = scraped_insert(db_client, l_race_key)
            if flg_scraped_insert:
                l_d_race_head = db_client.execute_select(sql.Sql.select_W_RACE_HEAD_for_view, l_race_key)
                l_d_race_info = db_client.execute_select(sql.Sql.select_W_RACE_INFO_for_view, l_race_key)

        # 0件だった場合、エラー（ここでは試走タイム等の情報がなくてもOK）
        if len(l_d_race_head) == 0 or len(l_d_race_info) == 0:
            err_msg = message.Message.err2.format(place, round)
            raise Exception(err_msg)

        db_client.commit()

        # レスポンス
        return {
            "headers": {
                "Access-Control-Allow-Origin" : "*",
                "Access-Control-Allow-Credentials": "true"
            },
            'statusCode': 200,
            'body': json.dumps({
                "race_head" : l_d_race_head,
                "race_info" : l_d_race_info
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
