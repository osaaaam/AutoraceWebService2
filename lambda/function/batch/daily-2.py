# 日次処理 - 2
# 当日のレース情報ファイルをS3に作成

import json
import datetime
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from module import awsmanagement
from module import scraping


def lambda_handler(event, context):
    try:

        # 昨日分のレース情報ファイルを削除
        s3_client = awsmanagement.S3()
        l_file = s3_client.get_filelist(awsmanagement.S3.s3_bucket_data_daily)
        for file_name in l_file:
            s3_client.delete_file(file_name, awsmanagement.S3.s3_bucket_data_daily)

        # 昨日分のレース分析結果ファイルを削除
        l_file = s3_client.get_filelist(awsmanagement.S3.s3_bucket_data_anaylize)
        for file_name in l_file:
            s3_client.delete_file(file_name, awsmanagement.S3.s3_bucket_data_anaylize)

        # 今日を取得
        today = datetime.datetime.today()
        dated = today.strftime("%Y-%m-%d")

        # レース会場取得
        url = scraping.Scraping.url_program
        scraping_client = scraping.Scraping(url, [dated], ['isesaki','kawaguchi','hamamatsu','sanyou','iizuka'], ['1'])
        scraping_client.get_place_by_url_program()

        # レース会場をループし、レース情報を取得
        for place in scraping_client.out_list_place:
            for round in ['1','2','3','4','5','6','7','8','9','10','11','12']:
                scraping_client = scraping.Scraping(url, [dated], [place], [round])
                scraping_client.get_raceinfo_by_url_program()

                # レース情報が取得できていて、
                if len(scraping_client.out_l_header) != 0:
                    # 8車制であれば、
                    if scraping_client.out_l_header[7] == "8車制":
                        # S3にcsvファイル出力
                        csv_value = ""
                        csv_value = csv_value + "place" + ","
                        csv_value = csv_value + "round" + ","
                        csv_value = csv_value + "car_no" + ","
                        csv_value = csv_value + "hande" + ","
                        csv_value = csv_value + "position_x" + ","
                        csv_value = csv_value + "position_y" + "\n"
                        for i in range(8):
                            csv_value = csv_value + place + ","
                            csv_value = csv_value + round + ","
                            csv_value = csv_value + str(i+1) + ","
                            csv_value = csv_value + str(scraping_client.out_l_hande[i]) + ","
                            csv_value = csv_value + str(scraping_client.out_l_position_x[i]) + ","
                            csv_value = csv_value + str(scraping_client.out_l_position_y[i]) + "\n"

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

                        s3_client.put_file(place_kana + "/" + round + "R.csv", csv_value, awsmanagement.S3.s3_bucket_data_daily)

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
