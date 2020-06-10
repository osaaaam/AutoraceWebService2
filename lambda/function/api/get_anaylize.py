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

# 分析1（複数予測結果の集計）
def anaylize_rule1(d_anaylize_model, db_client, l_d_race_head, l_d_race_info, l_race_key):

    ### 予測
    # どのモデルの予測値を集計させるか判別（最大5こまで）
    l_anaylize_model = d_anaylize_model["詳細"].split(",")
    count_anaylize_model = len(l_anaylize_model)
    l_anaylize_model = l_anaylize_model + ["99", "99", "99", "99", "99"]
    l_anaylize_model = l_anaylize_model[:5]
    # 集計した予測値を取得
    l_d_anaylize_result_detail = db_client.execute_select(
        sql.Sql.select_W_ANAYLIZE_RESULT_VALUE_for_anaylize, l_race_key + l_anaylize_model
    )
    # 集計した予測値を整形し、リストに格納
    l_result = [
        l_d_anaylize_result_detail[0]["１号車"] / count_anaylize_model,
        l_d_anaylize_result_detail[0]["２号車"] / count_anaylize_model,
        l_d_anaylize_result_detail[0]["３号車"] / count_anaylize_model,
        l_d_anaylize_result_detail[0]["４号車"] / count_anaylize_model,
        l_d_anaylize_result_detail[0]["５号車"] / count_anaylize_model,
        l_d_anaylize_result_detail[0]["６号車"] / count_anaylize_model,
        l_d_anaylize_result_detail[0]["７号車"] / count_anaylize_model,
        l_d_anaylize_result_detail[0]["８号車"] / count_anaylize_model
    ]

    ### 予測値をDBへ取り込み
    db_client.execute_insert(
        sql.Sql.insert_W_ANAYLIZE_RESULT_VALUE,
        l_race_key + [d_anaylize_model["モデル"]] + l_result
    )

    ### 予測着順をDBへ取り込み（7車制を考慮）
    l_d_result = []
    for i in range(len(l_d_race_info)):
        # 予測値整形
        if d_anaylize_model["アウトプット"] == "競争タイム":
            # 競争タイムから、ヨーイドンからゴールまでのタイムを計算
            l_result[i] = l_result[i] / 100 * (l_d_race_head[0]["距離"] + l_d_race_info[i]["ハンデ"])
        # 着順を決める用に、辞書型でリストに格納
        l_d_result.append({"車番": l_d_race_info[i]["車番"], "予測結果": l_result[i]})
    # ソートして着順に車番を取得する
    l_d_result.sort(key=lambda x:x['予測結果'])
    l_car_no = []
    for d_result in l_d_result:
        l_car_no.append(d_result["車番"])
    l_car_no.append(None)
    # INSERT
    db_client.execute_insert(
        sql.Sql.insert_W_ANAYLIZE_RESULT_RANK,
        l_race_key + [
            d_anaylize_model["モデル"],
            d_anaylize_model["アルゴリズム"],
            None,
            None,
            d_anaylize_model["インプット"],
            d_anaylize_model["アウトプット"]
        ] + l_car_no[:8]
    )


# 分析2（scikit-learnの回帰分析を使用し、各選手ごとに競争タイムを予測する）
def anaylize_rule2(d_anaylize_model, db_client, l_d_race_head, l_d_race_info, l_race_key):

    l_d_result = []
    l_result = []
    train_count = 0

    ### 予測
    anaylize_client = anaylize.Sklearn(d_anaylize_model["アルゴリズム"])
    for i in range(len(l_d_race_info)):
        # 訓練データを準備
        l_d_train_data = db_client.execute_select(
            sql.Sql.select_train_data_for_anaylize,
            [
                l_d_race_info[i]["選手名"],
                l_d_race_head[0]["距離"],
                l_d_race_head[0]["天候"],
                l_d_race_head[0]["走路状況"],
                l_d_race_head[0]["制度"],
                l_d_race_head[0]["種別"]
            ]
        )
        # 訓練データの件数取得
        train_count += len(l_d_train_data)
        # テストデータを準備
        l_d_test_date = db_client.execute_select(
            sql.Sql.select_test_data_for_anaylize,
            l_race_key + [l_d_race_info[i]["車番"]]
        )
        # 予測実行
        result = anaylize_client.execute_anaylize(
            l_d_train_data, l_d_test_date, d_anaylize_model["アウトプット"], d_anaylize_model["インプット"].split(",")
        )[0]
        # 予測値をリストに格納
        l_result.append(result)
        # 予測値整形
        if d_anaylize_model["アウトプット"] == "競争タイム":
            # 競争タイムから、ヨーイドンからゴールまでのタイムを計算
            result = result / 100 * (l_d_race_head[0]["距離"] + l_d_race_info[i]["ハンデ"])
        # 着順を決める用に、辞書型でリストに格納
        l_d_result.append({"車番": l_d_race_info[i]["車番"], "予測結果": result})

    ### 予測値をDBへ取り込み（7車制を考慮）
    l_result.append(None)
    db_client.execute_insert(
        sql.Sql.insert_W_ANAYLIZE_RESULT_VALUE,
        l_race_key + [d_anaylize_model["モデル"]] + l_result[:8]
    )

    ### 予測着順をDBへ取り込み（7車制を考慮）
    # ソートして着順に車番を取得する
    l_d_result.sort(key=lambda x:x['予測結果'])
    l_car_no = []
    for d_result in l_d_result:
        l_car_no.append(d_result["車番"])
    l_car_no.append(None)
    # INSERT
    db_client.execute_insert(
        sql.Sql.insert_W_ANAYLIZE_RESULT_RANK,
        l_race_key + [
            d_anaylize_model["モデル"],
            d_anaylize_model["アルゴリズム"],
            None,
            train_count,
            d_anaylize_model["インプット"],
            d_anaylize_model["アウトプット"]
        ] + l_car_no[:8]
    )


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
            else:
                err_msg = message.Message.err2.format(place, round)
                raise Exception(err_msg)

        # 0件だった場合、試走タイムが出ていなかった場合、エラー
        if check_exist_data(l_d_race_head, l_d_race_info) == False:
            err_msg = message.Message.err3
            raise Exception(err_msg)

        # スクレイピング完了後いったんコミット
        db_client.commit()

        # 分析済みレースか確認
        l_d_anaylize_result = db_client.execute_select(sql.Sql.select_W_ANAYLIZE_RESULT_RANK_for_view, l_race_key)
        l_d_anaylize_result_detail = db_client.execute_select(sql.Sql.select_W_ANAYLIZE_RESULT_VALUE_for_view, l_race_key)
        if len(l_d_anaylize_result) == 0:
            # 分析方法をDBから取得
            l_d_anaylize_model = db_client.execute_select(sql.Sql.select_M_ANAYLIZE_MODEL, [])
            # 分析実行
            try:
                for d_anaylize_model in l_d_anaylize_model:
                    if d_anaylize_model["アルゴリズム"] == "Union":
                        anaylize_rule1(
                            d_anaylize_model, db_client, l_d_race_head, l_d_race_info, l_race_key
                        )
                    else:
                        anaylize_rule2(
                            d_anaylize_model, db_client, l_d_race_head, l_d_race_info, l_race_key
                        )
                # 画面表示用に再セット
                l_d_anaylize_result = db_client.execute_select(sql.Sql.select_W_ANAYLIZE_RESULT_RANK_for_view, l_race_key)
                l_d_anaylize_result_detail = db_client.execute_select(sql.Sql.select_W_ANAYLIZE_RESULT_VALUE_for_view, l_race_key)
            except Exception as e:
                print(str(e))
                err_msg = message.Message.err4
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
