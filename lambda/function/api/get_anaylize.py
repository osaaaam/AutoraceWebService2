import json
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from module import dbaccess
from module import scraping
from module import message
from module import sql
from module import anaylize


# スクレイピングして、成功したら、DBへINSERT
def scraped_insert(db_client, p_list_key):
    url = scraping.Scraping.url_program
    scraping_client = scraping.Scraping(url, [p_list_key[0]], [p_list_key[1]], [p_list_key[2]])
    scraping_client.get_raceinfo_url_program()
    # スクレイピング結果が格納されていなかった場合、エラー
    scraped_data = scraping_client.out_list_header[0]
    if len(scraped_data) == 0:
        return False
    else:
        # ヘッダー情報をDBへINSERT
        list_param = p_list_key + scraping_client.out_list_header[0]
        db_client.execute_insert(sql.Sql.insert_W_RACE_HEAD, list_param)
        # レース情報をDBへINSERT
        for i in range(len(scraping_client.out_list_racer[0])):
            list_param = p_list_key + [
                i + 1,
                scraping_client.out_list_racer[0][i],
                scraping_client.out_list_represent[0][i],
                scraping_client.out_list_hande[0][i],
                scraping_client.out_list_trialrun[0][i],
                scraping_client.out_list_deviation[0][i],
                scraping_client.out_list_position[0][i]
            ]
            db_client.execute_insert(sql.Sql.insert_W_RACE_RACER, list_param)
        db_client.commit()
        return True


# 分析1
def anaylize_model1(db_client, race_head, race_info, p_list_key):
    # ランダムフォレストで予測する
    anaylize_client = anaylize.Sklearn("RandomForestRegressor")
    result_anaylize = []
    train_count = 0
    for i in range(len(race_info)):
        # 訓練データを準備
        train_data = db_client.execute_select(
            sql.Sql.select_train_data_for_anaylize,
            [race_info[i]["選手名"], race_head[0]["距離"], race_head[0]["走路状況"]]
        )
        # テストデータを準備
        test_date = db_client.execute_select(
            sql.Sql.select_test_data_for_anaylize,
            p_list_key + [race_info[i]["車番"]]
        )
        # 実行
        result = anaylize_client.execute_anaylize(
            train_data, test_date, "競争タイム", ["車番", "ハンデ", "試走タイム"]
        )
        # 辞書型をリストに格納
        result_anaylize.append({"車番": race_info[i]["車番"], "結果": result[0]})
        # 訓練データの件数
        train_count += len(train_data)

    # 画面表示用に整形
    result_anaylize.sort(key=lambda x:x['結果'])
    return {
        "予測モデル": "RandomForest",
        "学習件数": str(train_count) + "R",
        "INPUT": "選手名、距離、走路状態、車番、ハンデ、試走",
        "OUTPUT": "競争タイム",
        "◎": result_anaylize[0]["車番"],
        "○": result_anaylize[1]["車番"],
        "▲": result_anaylize[2]["車番"],
        "△": result_anaylize[3]["車番"]
    }


# 分析2
def anaylize_model2(db_client, race_head, race_info, p_list_key):
    # ランダムフォレストで予測する
    anaylize_client = anaylize.Sklearn("RandomForestRegressor")
    result_anaylize = []
    train_count = 0
    for i in range(len(race_info)):
        # 訓練データを準備
        train_data = db_client.execute_select(
            sql.Sql.select_train_data_for_anaylize,
            [race_info[i]["選手名"], race_head[0]["距離"], race_head[0]["走路状況"]]
        )
        # テストデータを準備
        test_date = db_client.execute_select(
            sql.Sql.select_test_data_for_anaylize,
            p_list_key + [race_info[i]["車番"]]
        )
        # 実行
        result = anaylize_client.execute_anaylize(
            train_data, test_date, "競争タイム", ["車番", "ハンデ", "試走タイム", "ポジション", "気温", "湿度", "走路温度"]
        )
        # 辞書型をリストに格納
        result_anaylize.append({"車番": race_info[i]["車番"], "結果": result[0]})
        # 訓練データの件数
        train_count += len(train_data)

    # 画面表示用に整形
    result_anaylize.sort(key=lambda x:x['結果'])
    return {
        "予測モデル": "RandomForest",
        "学習件数": str(train_count) + "R",
        "INPUT": "選手名、距離、走路状態、車番、ハンデ、試走、ポジション、気温、湿度、走路温度",
        "OUTPUT": "競争タイム",
        "◎": result_anaylize[0]["車番"],
        "○": result_anaylize[1]["車番"],
        "▲": result_anaylize[2]["車番"],
        "△": result_anaylize[3]["車番"]
    }


def lambda_handler(event, context):

    try:
        # パラム取得
        p_dated = event["queryStringParameters"]["dated"]
        p_place = event["queryStringParameters"]["place"]
        p_round = event["queryStringParameters"]["round"]
        p_list_key = [p_dated, p_place, p_round]

        # レース情報取得（レース当日の情報取得のため、作業用テーブルを検索する）
        db_client = dbaccess.Dbaccess()
        race_head = db_client.execute_select(sql.Sql.select_W_RACE_HEAD_by_racekey, p_list_key)
        race_info = db_client.execute_select(sql.Sql.select_W_RACE_RACER_by_racekey, p_list_key)

        # 0件だった場合、スクレイピングしてDBへINSERT
        # 成功した場合、画面表示用にレース情報を再セット
        if len(race_head) == 0 and len(race_info) == 0:
            scraped_result = scraped_insert(db_client, p_list_key)
            if scraped_result:
                race_head = db_client.execute_select(sql.Sql.select_W_RACE_HEAD_by_racekey, p_list_key)
                race_info = db_client.execute_select(sql.Sql.select_W_RACE_RACER_by_racekey, p_list_key)
            else:
                err_msg = message.Message.err2.format(p_place, p_round)
                raise Exception(err_msg)

        # 0件だった場合、エラー
        if len(race_head) == 0 or len(race_info) == 0:
            err_msg = message.Message.err2.format(p_place, p_round)
            raise Exception(err_msg)

        # 分析実行
        try:
            dic_anaylize = []
            dic_anaylize.append(anaylize_model1(db_client, race_head, race_info, p_list_key))
            dic_anaylize.append(anaylize_model2(db_client, race_head, race_info, p_list_key))

        except Exception as e:
            print(e)
            err_msg = message.Message.err3.format(p_place, p_round)
            raise Exception(err_msg)

        # レスポンス
        return {
            "headers": {
                "Access-Control-Allow-Origin" : "*",
                "Access-Control-Allow-Credentials": "true"
            },
            'statusCode': 200,
            'body': json.dumps({
                "race_head": race_head,
                "race_info": race_info,
                "anaylize": dic_anaylize
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
