# 分析テスト
# 分析モデルの精度を確認する

import json
import datetime
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from module import anaylize
from module import dbaccess
from module import message
from module import scraping
from module import sql


# 分析2（scikit-learnの回帰分析を使用し、各選手ごとに予測する）
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
                l_race_key[0], #日付
                l_d_race_info[i]["選手名"],
                l_d_race_head[0]["走路状況"]
                # l_d_race_head[0]["制度"],
                # l_d_race_head[0]["種別"]
            ]
        )
        # 訓練データの件数取得
        train_count += len(l_d_train_data)
        # テストデータを準備
        l_d_test_date = db_client.execute_select(
            sql.Sql.select_test_data_for_anaylize2,
            l_race_key + [l_d_race_info[i]["車番"]]
        )
        # 予測実行
        result = anaylize_client.execute_anaylize(
            l_d_train_data, l_d_test_date, d_anaylize_model["アウトプット"], d_anaylize_model["インプット"].split(",")
        )[0]
        if d_anaylize_model["アウトプット"] == "着順":
            # Int型で結果が返却されるため、float型にする
            result = float(result)
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


def lambda_handler(event, context):
    try:

        db_client = dbaccess.Dbaccess()

        # 月次処理ログテーブルから対象レース取得
        l_d_target = db_client.execute_select(sql.Sql.select_T_MONTHLY_LOG2, [])

        for d_target in l_d_target:

            l_race_key = [d_target["開催日"], d_target["レース場"], d_target["ラウンド"]]

            # 予測レース情報取得
            l_d_race_head = db_client.execute_select(sql.Sql.select_T_RACE_HEAD, l_race_key)
            l_d_race_info = db_client.execute_select(sql.Sql.select_T_RACE_INFO, l_race_key)

            # 分析方法をDBから取得
            l_d_anaylize_model = db_client.execute_select(sql.Sql.select_M_ANAYLIZE_MODEL, [])

            # 分析実行
            try:
                for d_anaylize_model in l_d_anaylize_model:
                    anaylize_rule2(
                        d_anaylize_model, db_client, l_d_race_head, l_d_race_info, l_race_key
                    )

            except Exception as e:
                print(str(e))

            # 月次処理ログテーブルを更新
            l_param = [2, None] + l_race_key
            db_client.execute_update(sql.Sql.update_T_MONTHLY_LOG, l_param)

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
