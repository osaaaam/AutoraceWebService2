# 月次処理 - 1
# 先月に開催された全日程、全レース場をDBへセット

import json
import datetime
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
    for place in scraping_client.out_list_place:
        for i in range(12):
            l_param = [dated, place, i+1, 0, None]
            db_client.execute_insert(sql.Sql.insert_T_MONTHLY_LOG, l_param)


def lambda_handler(event, context):
    try:
        ## 先月の全部の日付を配列に格納する
        l_dated = []
        # 今日を取得
        today = datetime.datetime.today()
        # 当月1日の値を出す
        thismonth = datetime.datetime(today.year, today.month, 1)
        # 前月末日の値を出す
        lastmonth = thismonth + datetime.timedelta(days=-1)
        # 配列に格納
        yyyymm = lastmonth.strftime("%Y-%m-")
        dd = lastmonth.strftime("%d")
        for i in range(int(dd)):
            l_dated.append(yyyymm + ("0"+str(i+1))[-2:])

        # 先月の全部の日付をスクレイピング → 開催していたらINSERT
        db_client = dbaccess.Dbaccess()
        for dated in l_dated:
            scraped_insert(db_client, dated)
        
        db_client.commit()

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

    finally:
        del db_client
