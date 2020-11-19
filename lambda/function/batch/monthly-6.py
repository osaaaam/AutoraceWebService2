# 月次処理 - 6
# 全選手分、予測用ファイル（訓練データ）をS3に作成

import json
import datetime
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from module import awsmanagement
from module import dbaccess
from module import sql


def lambda_handler(event, context):
    try:

        db_client = dbaccess.Dbaccess()

        # 月次選手ワークテーブルから取得
        l_d_target = db_client.execute_select(sql.Sql.select_W_MONTHLY_RACER, [])

        for d_target in l_d_target:

            # 訓練データを準備
            l_d_train_data = db_client.execute_select(
                sql.Sql.select_train_data_for_anaylize,
                [
                    "2017-03-31", #データを持っていない日付を置いておく
                    d_target["選手名"],
                    "良走路"
                    # l_d_race_head[0]["制度"],
                    # l_d_race_head[0]["種別"]
                ]
            )

            # 1件以上あれば出力
            if len(l_d_train_data) > 0:

                # csv形式に変換
                csv_value = ""
                csv_value = csv_value + "車番" + ","
                csv_value = csv_value + "ハンデ" + ","
                csv_value = csv_value + "試走タイム" + ","
                csv_value = csv_value + "試走偏差" + ","
                csv_value = csv_value + "横ポジション" + ","
                csv_value = csv_value + "縦ポジション" + ","
                csv_value = csv_value + "競争タイム" + ","
                csv_value = csv_value + "着順" + ","
                csv_value = csv_value + "気温" + ","
                csv_value = csv_value + "湿度" + ","
                csv_value = csv_value + "走路温度" + "\n"
                for d_train_data in l_d_train_data:
                    csv_value = csv_value + str(d_train_data["車番"]) + ","
                    csv_value = csv_value + str(d_train_data["ハンデ"]) + ","
                    csv_value = csv_value + str(d_train_data["試走タイム"]) + ","
                    csv_value = csv_value + str(d_train_data["試走偏差"]) + ","
                    csv_value = csv_value + str(d_train_data["横ポジション"]) + ","
                    csv_value = csv_value + str(d_train_data["縦ポジション"]) + ","
                    csv_value = csv_value + str(d_train_data["競争タイム"]) + ","
                    csv_value = csv_value + str(d_train_data["着順"]) + ","
                    csv_value = csv_value + str(d_train_data["気温"]) + ","
                    csv_value = csv_value + str(d_train_data["湿度"]) + ","
                    csv_value = csv_value + str(d_train_data["走路温度"]) + "\n"

                # S3にUP
                s3_client = awsmanagement.S3()
                s3_client.put_file(d_target["選手名"] + ".csv", csv_value)

            # 選手ワークテーブルを削除
            db_client.execute_delete(sql.Sql.delete_W_MONTHLY_RACER_by_racer, [d_target["選手名"]])
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
