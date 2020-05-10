import json
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from module import dbaccess
from module import message
from module import scraping
from module import sql


# スクレイピングして、成功したら、DBへINSERT
def scraped_insert(db_client, dated):
    url = scraping.Scraping.url_program
    scraping_client = scraping.Scraping(url, [dated], ['isesaki','kawaguchi','hamamatsu','sanyou','iizuka'], ['1'])
    scraping_client.get_place_by_url_program()
    # スクレイピング結果が格納されていなかった場合、エラー
    if len(scraping_client.out_list_place) == 0:
        return False
    else:
        # レース場をDBへINSERT
        for place in scraping_client.out_list_place:
            l_param = [dated, place]
            db_client.execute_insert(sql.Sql.insert_W_PLACE, l_param)
        db_client.commit()
        return True


def lambda_handler(event, context):
    try:
        # パラム取得
        dated = event["queryStringParameters"]["dated"]

        # 本日のレース場取得
        db_client = dbaccess.Dbaccess()
        l_d_place = db_client.execute_select(sql.Sql.select_W_PLACE_by_dated, [dated])

        # 0件だった場合、スクレイピング → INSERT
        # 成功した場合、画面表示用にレース場を再セット
        if len(l_d_place) == 0:
            flg_scraped_insert = scraped_insert(db_client, dated)
            if flg_scraped_insert:
                l_d_place = db_client.execute_select(sql.Sql.select_W_PLACE_by_dated, [dated])

        # 0件だった場合、エラー
        if len(l_d_place) == 0:
            err_msg = message.Message.err5
            raise Exception(err_msg)

        # レスポンス
        return {
            "headers": {
                "Access-Control-Allow-Origin" : "*",
                "Access-Control-Allow-Credentials": "true"
            },
            'statusCode': 200,
            'body': json.dumps({
                "place" : l_d_place
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
