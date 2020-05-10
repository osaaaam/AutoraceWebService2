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
    scraping_client.get_raceinfo_url_program()
    # スクレイピング結果が格納されていなかった場合、エラー
    l_scraped_data = scraping_client.out_lists_header[0]
    if len(l_scraped_data) == 0:
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


# 分析1
def anaylize_model1(db_client, l_d_race_head, l_d_race_info, l_race_key):
    # ランダムフォレストで予測する
    anaylize_client = anaylize.Sklearn("RandomForestRegressor")
    l_d_result = []
    train_count = 0
    for i in range(len(l_d_race_info)):
        # 訓練データを準備
        l_d_train_data = db_client.execute_select(
            sql.Sql.select_train_data_for_anaylize,
            [l_d_race_info[i]["選手名"], l_d_race_head[0]["距離"], l_d_race_head[0]["走路状況"]]
        )
        # テストデータを準備
        l_d_test_date = db_client.execute_select(
            sql.Sql.select_test_data_for_anaylize,
            l_race_key + [l_d_race_info[i]["車番"]]
        )
        # 実行
        l_result = anaylize_client.execute_anaylize(
            l_d_train_data, l_d_test_date, "競争タイム", ["車番", "ハンデ", "試走タイム"]
        )
        # 辞書型をリストに格納
        l_d_result.append({"車番": l_d_race_info[i]["車番"], "結果": l_result[0]})
        # 訓練データの件数
        train_count += len(l_d_train_data)

    # 画面表示用に整形
    l_d_result.sort(key=lambda x:x['結果'])
    return {
        "予測モデル": "RandomForest",
        "学習件数": str(train_count) + "R",
        "INPUT": "選手名、距離、走路状態、車番、ハンデ、試走",
        "OUTPUT": "競争タイム",
        "◎": l_d_result[0]["車番"],
        "○": l_d_result[1]["車番"],
        "▲": l_d_result[2]["車番"],
        "△": l_d_result[3]["車番"]
    }


# 分析2
def anaylize_model2(db_client, l_d_race_head, l_d_race_info, l_race_key):
    # ランダムフォレストで予測する
    anaylize_client = anaylize.Sklearn("RandomForestRegressor")
    l_d_result = []
    train_count = 0
    for i in range(len(l_d_race_info)):
        # 訓練データを準備
        l_d_train_data = db_client.execute_select(
            sql.Sql.select_train_data_for_anaylize,
            [l_d_race_info[i]["選手名"], l_d_race_head[0]["距離"], l_d_race_head[0]["走路状況"]]
        )
        # テストデータを準備
        l_d_test_date = db_client.execute_select(
            sql.Sql.select_test_data_for_anaylize,
            l_race_key + [l_d_race_info[i]["車番"]]
        )
        # 実行
        l_result = anaylize_client.execute_anaylize(
            l_d_train_data, l_d_test_date, "競争タイム", ["車番", "ハンデ", "試走タイム", "ポジション", "気温", "湿度", "走路温度"]
        )
        # 辞書型をリストに格納
        l_d_result.append({"車番": l_d_race_info[i]["車番"], "結果": l_result[0]})
        # 訓練データの件数
        train_count += len(l_d_train_data)

    # 画面表示用に整形
    l_d_result.sort(key=lambda x:x['結果'])
    return {
        "予測モデル": "RandomForest",
        "学習件数": str(train_count) + "R",
        "INPUT": "選手名、距離、走路状態、車番、ハンデ、試走、ポジション、気温、湿度、走路温度",
        "OUTPUT": "競争タイム",
        "◎": l_d_result[0]["車番"],
        "○": l_d_result[1]["車番"],
        "▲": l_d_result[2]["車番"],
        "△": l_d_result[3]["車番"]
    }


def lambda_handler(event, context):
    try:
        # パラム取得
        dated = event["queryStringParameters"]["dated"]
        place = event["queryStringParameters"]["place"]
        round = event["queryStringParameters"]["round"]
        l_race_key = [dated, place, round]

        # レース情報取得（レース当日の情報取得のため、作業用テーブルを検索する）
        db_client = dbaccess.Dbaccess()
        l_d_race_head = db_client.execute_select(sql.Sql.select_W_RACE_HEAD_by_racekey, l_race_key)
        l_d_race_info = db_client.execute_select(sql.Sql.select_W_RACE_RACER_by_racekey, l_race_key)

        # 0件だった場合、スクレイピングしてDBへINSERT
        # 成功した場合、画面表示用にレース情報を再セット
        if len(l_d_race_head) == 0 and len(l_d_race_info) == 0:
            flg_scraped_insert = scraped_insert(db_client, l_race_key)
            if flg_scraped_insert:
                l_d_race_head = db_client.execute_select(sql.Sql.select_W_RACE_HEAD_by_racekey, l_race_key)
                l_d_race_info = db_client.execute_select(sql.Sql.select_W_RACE_RACER_by_racekey, l_race_key)
            else:
                err_msg = message.Message.err2.format(place, round)
                raise Exception(err_msg)

        # 0件だった場合、エラー
        if len(l_d_race_head) == 0 or len(l_d_race_info) == 0:
            err_msg = message.Message.err2.format(place, round)
            raise Exception(err_msg)

        # 分析実行
        try:
            l_d_anaylize = []
            l_d_anaylize.append(anaylize_model1(db_client, l_d_race_head, l_d_race_info, l_race_key))
            l_d_anaylize.append(anaylize_model2(db_client, l_d_race_head, l_d_race_info, l_race_key))

        except Exception as e:
            print(e)
            err_msg = message.Message.err3.format(place, round)
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
                "anaylize": l_d_anaylize
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
