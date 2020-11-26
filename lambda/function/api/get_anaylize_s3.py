import json
import os, sys
import csv
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from module import anaylize
from module import awsmanagement
from module import message
from module import scraping


def lambda_handler(event, context):
    try:
        # パラム取得
        dated = event["queryStringParameters"]["dated"]
        place = event["queryStringParameters"]["place"]
        round = event["queryStringParameters"]["round"]

        # スクレイピング
        url = scraping.Scraping.url_program
        scraping_client = scraping.Scraping(url, [dated], [place], [round])
        scraping_client.get_raceinfo_by_url_program()
        # スクレイピング結果が格納されていなかった場合、エラー
        if len(scraping_client.out_l_header) == 0:
            err_msg = message.Message.err3
            raise Exception(err_msg)

        else:
            # 分析開始
            anaylize_client = anaylize.Sklearn("RandomForestRegressor")
            if scraping_client.out_l_header[7] != "8車制":
                err_msg = "8車制のレースのみ予測可能です"
                raise Exception(err_msg)

            elif scraping_client.out_l_trialrun[0] == "":
                err_msg = "試走タイム発表後に予測可能です"
                raise Exception(err_msg)

            elif scraping_client.out_l_header[6] != "良走路":
                err_msg = "良走路のレースのみ予測可能です"
                raise Exception(err_msg)

            else:
                l_d_result = []
                train_count = 0

                for i in range(len(scraping_client.out_l_racer)):

                    # S3から訓練データを準備
                    l_d_train_data = []
                    s3_client = awsmanagement.S3()
                    for d_train_data in csv.DictReader(s3_client.get_file(scraping_client.out_l_racer[i] + ".csv", awsmanagement.S3.s3_bucket_data)):
                        l_d_train_data.append(d_train_data)
                    # 訓練データの件数取得
                    train_count += len(l_d_train_data)

                    # テストデータを準備
                    l_d_test_date = [{
                        "車番": i+1,
                        "ハンデ": scraping_client.out_l_hande[i],
                        "試走タイム": scraping_client.out_l_trialrun[i],
                        "試走偏差": scraping_client.out_l_deviation[i],
                        "横ポジション": scraping_client.out_l_position_x[i],
                        "縦ポジション": scraping_client.out_l_position_y[i],
                        "気温": scraping_client.out_l_header[3],
                        "湿度": scraping_client.out_l_header[4],
                        "走路温度": scraping_client.out_l_header[5]
                    }]

                    # 予測実行（訓練データはs3のcsvファイル）
                    result = anaylize_client.execute_anaylize(
                        l_d_train_data,
                        l_d_test_date,
                        "競争タイム",
                        ["試走タイム","横ポジション","縦ポジション","走路温度"]
                    )[0]

                    # 予測値整形
                    # 競争タイムから、ヨーイドンからゴールまでのタイムを計算
                    # 競争タイム ÷ 100 × (レース距離 + ハンデ)
                    result2 = result / 100 * (int(scraping_client.out_l_header[1]) + int(scraping_client.out_l_hande[i]))
                    # 着順を決める用に、辞書型でリストに格納
                    l_d_result.append({"車番": str(i+1), "選手名": scraping_client.out_l_racer[i], "競争タイム": str(result), "並替用": result2})

                # ソートして着順に車番を取得する
                l_d_result.sort(key=lambda x:x['並替用'])

                # S3にcsvファイル出力
                csv_value = ""
                csv_value = csv_value + "訓練レース数" + ","
                csv_value = csv_value + "車番" + ","
                csv_value = csv_value + "選手名" + ","
                csv_value = csv_value + "競争タイム" + "\n"
                for i in range(len(l_d_result)):
                    csv_value = csv_value + str(train_count) + ","
                    csv_value = csv_value + str(l_d_result[i]["車番"]) + ","
                    csv_value = csv_value + l_d_result[i]["選手名"] + ","
                    csv_value = csv_value + str(l_d_result[i]["競争タイム"]) + "\n"

                # S3にUP
                if place == "kawaguchi":
                    place_kana = "川口"
                elif place == "isesaki":
                    place_kana = "伊勢崎"
                elif place == "hamamatsu":
                    place_kana = "浜松"
                elif place == "iizuka":
                    place_kana = "飯塚"
                elif place == "sanyou":
                    place_kana = "山陽"
                else:
                    place_kana = "その他"

                s3_client = awsmanagement.S3()
                s3_client.put_file(place_kana + "/" + round + "R.csv", csv_value, awsmanagement.S3.s3_bucket_data_anaylize)

        # レスポンス
        return {
            'statusCode': 200,
            'body': json.dumps({
                "message": "ok",
                "TrainCount": str(train_count),
                "Anaylize": l_d_result
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
            'body': json.dumps({
                "message": str(e)
            })
        }

    # finally:
    #     del db_client
