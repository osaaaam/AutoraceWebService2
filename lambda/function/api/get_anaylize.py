import json
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from module import anaylize
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
    if len(scraping_client.out_lists_header[0]) == 0:
        return False
    else:
        # ヘッダー情報をDBへINSERT
        l_param = l_race_key + scraping_client.out_lists_header[0]
        db_client.execute_insert(sql.Sql.insert_W_RACE_HEAD, l_param)
        # レース情報をDBへINSERT
        for i in range(len(scraping_client.out_lists_racer[0])):
            l_param = l_race_key + [
                i + 1,
                scraping_client.out_lists_racer[0][i],
                scraping_client.out_lists_represent[0][i],
                scraping_client.out_lists_hande[0][i],
                scraping_client.out_lists_trialrun[0][i],
                scraping_client.out_lists_deviation[0][i],
                scraping_client.out_lists_position[0][i]
            ]
            db_client.execute_insert(sql.Sql.insert_W_RACE_RACER, l_param)
        db_client.commit()
        return True


# 分析1（scikit-learnの回帰分析を使用し、各選手ごとに競争タイムを予測する）
def anaylize_rule1(d_anaylize_model, db_client, l_d_race_head, l_d_race_info, l_race_key):
    anaylize_client = anaylize.Sklearn(d_anaylize_model["アルゴリズム"])
    l_d_result = []
    l_result_ori = []
    train_count = 0
    for i in range(len(l_d_race_info)):
        # 訓練データを準備
        l_d_train_data = db_client.execute_select(
            sql.Sql.select_train_data_for_anaylize,
            [l_d_race_info[i]["選手名"], l_d_race_head[0]["距離"], l_d_race_head[0]["走路状況"]]
        )
        # 訓練データの件数
        train_count += len(l_d_train_data)
        # テストデータを準備
        l_d_test_date = db_client.execute_select(
            sql.Sql.select_test_data_for_anaylize,
            l_race_key + [l_d_race_info[i]["車番"]]
        )
        # 実行
        l_result = anaylize_client.execute_anaylize(
            l_d_train_data, l_d_test_date, d_anaylize_model["アウトプット"], d_anaylize_model["インプット"].split(",")
        )
        # 整形前の予測結果をリストに格納
        l_result_ori.append(l_result[0])
        # 予測結果整形
        if d_anaylize_model["アウトプット"] == "競争タイム":
            # 競争タイムから、ヨーイドンからゴールまでのタイムを計算
            l_result[0] = l_result[0] / 100 * (l_d_race_head[0]["距離"] + l_d_race_info[i]["ハンデ"])
        # 整形後の予測結果を、辞書型でリストに格納
        l_d_result.append({"車番": l_d_race_info[i]["車番"], "予測結果": l_result[0]})

    # オリジナルの予測結果をDBへ取り込み（7車制を考慮）
    l_result_ori.append(None)
    l_result_ori = l_result_ori[:8]
    db_client.execute_insert(
        sql.Sql.insert_W_ANAYLIZE_RESULT_DETAIL,
        l_race_key + [d_anaylize_model["モデル"]] + l_result_ori
    )
    # 整形後の予測結果をDBへ取り込み（7車制を考慮）
    # 予測結果でソート
    l_d_result.sort(key=lambda x:x['予測結果'])
    l_car_no = []
    for d_result in l_d_result:
        l_car_no.append(d_result["車番"])
    l_car_no.append(None)
    db_client.execute_insert(
        sql.Sql.insert_W_ANAYLIZE_RESULT,
        l_race_key + [
            d_anaylize_model["モデル"],
            d_anaylize_model["アルゴリズム"],
            None,
            train_count,
            d_anaylize_model["インプット"],
            d_anaylize_model["アウトプット"]
        ] + l_car_no[:8]
    )
    db_client.commit()


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
        l_d_race_info = db_client.execute_select(sql.Sql.select_W_RACE_RACER_for_view, l_race_key)

        # 0件だった場合、試走タイムが出ていなかった場合、DELETE → スクレイピング → INSERT
        # 成功した場合、画面表示用にレース情報を再セット
        if check_exist_data(l_d_race_head, l_d_race_info) == False:
            db_client.execute_delete(sql.Sql.delete_W_RACE_HEAD_by_racekey, l_race_key)
            db_client.execute_delete(sql.Sql.delete_W_RACE_RACER_by_racekey, l_race_key)
            flg_scraped_insert = scraped_insert(db_client, l_race_key)
            if flg_scraped_insert:
                l_d_race_head = db_client.execute_select(sql.Sql.select_W_RACE_HEAD_for_view, l_race_key)
                l_d_race_info = db_client.execute_select(sql.Sql.select_W_RACE_RACER_for_view, l_race_key)
            else:
                err_msg = message.Message.err2.format(place, round)
                raise Exception(err_msg)

        # 0件だった場合、試走タイムが出ていなかった場合、エラー
        if check_exist_data(l_d_race_head, l_d_race_info) == False:
            err_msg = message.Message.err3
            raise Exception(err_msg)

        # 分析済みレースか確認
        l_d_anaylize_result = db_client.execute_select(sql.Sql.select_W_ANAYLIZE_RESULT_for_view, l_race_key)
        l_d_anaylize_result_detail = db_client.execute_select(sql.Sql.select_W_ANAYLIZE_RESULT_DETAIL_for_view, l_race_key)
        if len(l_d_anaylize_result) == 0:
            # 分析方法をDBから取得
            l_d_anaylize_model = db_client.execute_select(sql.Sql.select_M_ANAYLIZE_MODEL, [])
            # 分析実行
            try:
                for d_anaylize_model in l_d_anaylize_model:
                    anaylize_rule1(
                        d_anaylize_model, db_client, l_d_race_head, l_d_race_info, l_race_key
                    )
                # 画面表示用に再セット
                l_d_anaylize_result = db_client.execute_select(sql.Sql.select_W_ANAYLIZE_RESULT_for_view, l_race_key)
                l_d_anaylize_result_detail = db_client.execute_select(sql.Sql.select_W_ANAYLIZE_RESULT_DETAIL_for_view, l_race_key)
            except Exception as e:
                print(str(e))
                err_msg = message.Message.err4
                raise Exception(err_msg)

        # レスポンス
        return {
            "headers": {
                "Access-Control-Allow-Origin" : "*",
                "Access-Control-Allow-Credentials": "true"
            },
            'statusCode': 200,
            'body': json.dumps({
                "race_head": l_d_race_head,
                "race_info": l_d_race_info,
                "anaylize": l_d_anaylize_result,
                "anaylize_detail": l_d_anaylize_result_detail
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
