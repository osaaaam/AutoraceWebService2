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

            elif scraping_client.out_l_trialrun[i] == "":
                err_msg = "試走タイム発表後に予測可能です"
                raise Exception(err_msg)

            elif scraping_client.out_l_header[6] != "良走路":
                err_msg = "良走路のレースのみ予測可能です"
                raise Exception(err_msg)

            else:
                l_d_result = []
                l_result = []
                train_count = 0

                for i in range(len(scraping_client.out_l_racer)):

                    # S3から訓練データを準備
                    l_d_train_data = []
                    s3_client = awsmanagement.S3()
                    for d_train_data in csv.DictReader(s3_client.get_file(scraping_client.out_l_racer[i] + ".csv")):
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

                    # 予測値をリストに格納
                    l_result.append(result)
                    # 予測値整形
                    # 競争タイムから、ヨーイドンからゴールまでのタイムを計算
                    # 競争タイム = 競争タイム ÷ 100 × (レース距離 + ハンデ)
                    result = result / 100 * (int(scraping_client.out_l_header[1]) + int(scraping_client.out_l_hande[i]))
                    # 着順を決める用に、辞書型でリストに格納
                    l_d_result.append({"車番": i+1, "予測結果": result})

                # ソートして着順に車番を取得する
                l_d_result.sort(key=lambda x:x['予測結果'])
                l_car_no = []
                for d_result in l_d_result:
                    l_car_no.append(d_result["車番"])

                print(l_car_no)
                print()

        # レスポンス
        return {
            'statusCode': 200,
            'body': json.dumps("ok")
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

    # finally:
    #     del db_client
