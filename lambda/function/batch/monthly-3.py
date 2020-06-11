# 月次処理 - 3
# 先月に開催された全日程、全レース場をinputに、レース情報取り込み

import json
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from module import dbaccess
from module import message
from module import scraping
from module import sql


# スクレイピングして、成功したら、DBへINSERT
def scraped_insert_info(db_client, l_race_key):
    url = scraping.Scraping.url_program
    scraping_client = scraping.Scraping(url, [l_race_key[0]], [l_race_key[1]], [l_race_key[2]])
    scraping_client.get_raceinfo_by_url_program()
    # スクレイピング結果が格納されていなかった場合、エラー
    if len(scraping_client.out_l_header) == 0:
        return scraping_client.out_err_msg
    else:
        try:
            # ヘッダー情報をDBへINSERT
            l_param = l_race_key + scraping_client.out_l_header
            db_client.execute_insert(sql.Sql.insert_T_RACE_HEAD, l_param)
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
                db_client.execute_insert(sql.Sql.insert_T_RACE_INFO, l_param)
            return ""
        except Exception as e:
            print(str(e))
            return str(e)


# スクレイピングして、成功したら、DBへINSERT
def scraped_insert_result(db_client, l_race_key):
    url = scraping.Scraping.url_result
    scraping_client = scraping.Scraping(url, [l_race_key[0]], [l_race_key[1]], [l_race_key[2]])
    scraping_client.get_raceresult_by_url_result()
    # スクレイピング結果が格納されていなかった場合、エラー
    if len(scraping_client.out_l_rank) == 0:
        return scraping_client.out_err_msg
    else:
        try:
            # 払戻額をDBへINSERT（着順は7車制を考慮）
            l_param = l_race_key + scraping_client.out_l_payoff + (scraping_client.out_l_car_no + [None])[:8]
            db_client.execute_insert(sql.Sql.insert_T_RACE_PAYOFF, l_param)
            # レース結果をDBへINSERT
            for i in range(len(scraping_client.out_l_car_no)):
                l_param = l_race_key + [
                    scraping_client.out_l_car_no[i],
                    scraping_client.out_l_racetime[i],
                    scraping_client.out_l_starttime[i],
                    scraping_client.out_l_rank[i]
                ]
                db_client.execute_insert(sql.Sql.insert_T_RACE_RESULT, l_param)
            return ""
        except Exception as e:
            print(str(e))
            return str(e)


def lambda_handler(event, context):
    try:
        # 月次処理対象を取得
        db_client = dbaccess.Dbaccess()
        l_d_target = db_client.execute_select(sql.Sql.select_T_MONTHLY_LOG, [])

        # 処理対象分ループ
        for d_target in l_d_target:
            l_race_key = [d_target["開催日"], d_target["レース場"], d_target["ラウンド"]]
            print(l_race_key)
            # スクレイピング → INSERTをし、エラーメッセージ取得
            err_msg = scraped_insert_info(db_client, l_race_key)
            if err_msg == "":
                err_msg = scraped_insert_result(db_client, l_race_key)
                if err_msg == "":
                    l_param = [1, None] + l_race_key
                else:
                    db_client.rollback()
                    l_param = [92, err_msg] + l_race_key
            else:
                db_client.rollback()
                l_param = [91, err_msg] + l_race_key

            db_client.execute_update(sql.Sql.update_T_MONTHLY_LOG, l_param)
            # 1処理ずつコミットする
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
