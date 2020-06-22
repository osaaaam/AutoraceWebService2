class Sql:

    ##### 作業用 #####
    # 挿入 レースヘッダ
    insert_W_RACE_HEAD = " INSERT INTO auto2.w_race_head ( "\
                         "     dated, "\
                         "     place, "\
                         "     round, "\
                         "     race_name, "\
                         "     distance, "\
                         "     weather, "\
                         "     temperature, "\
                         "     humidity, "\
                         "     runway_temperature, "\
                         "     runway_condition, "\
                         "     race_system, "\
                         "     race_type "\
                         " ) "\
                         " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "

    # 挿入 レース情報
    insert_W_RACE_INFO = " INSERT INTO auto2.w_race_info ( "\
                          "     dated, "\
                          "     place, "\
                          "     round, "\
                          "     car_no, "\
                          "     racer, "\
                          "     represent, "\
                          "     hande, "\
                          "     trialrun, "\
                          "     deviation, "\
                          "     position_x, "\
                          "     position_y "\
                          " ) "\
                          " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "

    # 削除 作業用レースヘッダ
    delete_W_RACE_HEAD_by_racekey = " DELETE FROM auto2.w_race_head rh "\
                                    "  WHERE rh.dated = %s "\
                                    "    AND rh.place = %s "\
                                    "    AND rh.round = %s "

    # 削除 作業用レースヘッダ
    delete_W_RACE_INFO_by_racekey = " DELETE FROM auto2.w_race_info ri "\
                                    "  WHERE ri.dated = %s "\
                                    "    AND ri.place = %s "\
                                    "    AND ri.round = %s "

    # 選択 作業用レース場
    select_W_PLACE_by_dated = " SELECT wp.place レース場 "\
                              "   FROM auto2.w_place wp "\
                              "  WHERE wp.dated = %s "

    # 挿入 作業用レース場
    insert_W_PLACE = " INSERT INTO auto2.w_place ( "\
                         "     dated, "\
                         "     place "\
                         " ) "\
                         " VALUES (%s, %s) "

    ##### 画面表示用 #####
    # 選択 レースヘッダ
    select_W_RACE_HEAD_for_view = " SELECT rh.race_name レース "\
                                    "       ,rh.distance 距離 "\
                                    "       ,rh.weather 天候 "\
                                    "       ,rh.temperature 気温 "\
                                    "       ,rh.humidity 湿度 "\
                                    "       ,rh.runway_temperature 走路温度 "\
                                    "       ,rh.runway_condition 走路状況 "\
                                    "       ,rh.race_system 制度 "\
                                    "       ,rh.race_type 種別 "\
                                    "   FROM auto2.w_race_head rh "\
                                    "  WHERE rh.dated = %s "\
                                    "    AND rh.place = %s "\
                                    "    AND rh.round = %s "

    # 選択 レース情報
    select_W_RACE_INFO_for_view = " SELECT ri.car_no 車番 "\
                                     "       ,ri.racer 選手名 "\
                                     "       ,ri.represent 所属 "\
                                     "       ,ri.hande ハンデ "\
                                     "       ,ri.trialrun 試走タイム "\
                                     "       ,ri.deviation 試走偏差 "\
                                     "   FROM auto2.w_race_info ri "\
                                     "  WHERE ri.dated = %s "\
                                     "    AND ri.place = %s "\
                                     "    AND ri.round = %s "\
                                     "  ORDER BY ri.car_no "

    # 選択 予測値
    select_W_ANAYLIZE_RESULT_VALUE_for_view = " SELECT av.model_no モデル "\
                                               "       ,av.first_car １号車 "\
                                               "       ,av.second_car ２号車 "\
                                               "       ,av.third_car ３号車 "\
                                               "       ,av.fourth_car ４号車 "\
                                               "       ,av.fifth_car ５号車 "\
                                               "       ,av.sixth_car ６号車 "\
                                               "       ,av.seventh_car ７号車 "\
                                               "       ,av.eighth_car ８号車 "\
                                               "   FROM auto2.w_anaylize_result_value av "\
                                               "  WHERE av.dated = %s "\
                                               "    AND av.place = %s "\
                                               "    AND av.round = %s "

    # 選択 予測順位
    select_W_ANAYLIZE_RESULT_RANK_for_view = " SELECT ar.model_no モデル "\
                                        "       ,ar.algorithm アルゴリズム "\
                                        "       ,ar.count_data 学習件数 "\
                                        "       ,ar.features インプット "\
                                        "       ,ar.target アウトプット "\
                                        "       ,ar.first_place ◎ "\
                                        "       ,ar.second_place ○ "\
                                        "       ,ar.third_place ▲ "\
                                        "       ,ar.fourth_place △ "\
                                        "   FROM auto2.w_anaylize_result_rank ar "\
                                        "  WHERE ar.dated = %s "\
                                        "    AND ar.place = %s "\
                                        "    AND ar.round = %s "


    ##### 分析用 #####
    # 選択 予測値
    select_W_ANAYLIZE_RESULT_VALUE_for_anaylize = " SELECT SUM(av.first_car) １号車 "\
                                                   "       ,SUM(av.second_car) ２号車 "\
                                                   "       ,SUM(av.third_car) ３号車 "\
                                                   "       ,SUM(av.fourth_car) ４号車 "\
                                                   "       ,SUM(av.fifth_car) ５号車 "\
                                                   "       ,SUM(av.sixth_car) ６号車 "\
                                                   "       ,SUM(av.seventh_car) ７号車 "\
                                                   "       ,SUM(av.eighth_car) ８号車 "\
                                                   "   FROM auto2.w_anaylize_result_value av "\
                                                   "  WHERE av.dated = %s "\
                                                   "    AND av.place = %s "\
                                                   "    AND av.round = %s "\
                                                   "    AND av.model_no IN (%s, %s, %s, %s, %s) "\
                                                   "  GROUP BY av.dated, av.place, av.round "

    # 挿入 予測値
    insert_W_ANAYLIZE_RESULT_VALUE = " INSERT INTO auto2.w_anaylize_result_value ( "\
                                      "     dated, "\
                                      "     place, "\
                                      "     round, "\
                                      "     model_no, "\
                                      "     first_car, "\
                                      "     second_car, "\
                                      "     third_car, "\
                                      "     fourth_car, "\
                                      "     fifth_car, "\
                                      "     sixth_car, "\
                                      "     seventh_car, "\
                                      "     eighth_car "\
                                      " ) "\
                                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "

    # 挿入 予測順位
    insert_W_ANAYLIZE_RESULT_RANK = " INSERT INTO auto2.w_anaylize_result_rank ( "\
                               "     dated, "\
                               "     place, "\
                               "     round, "\
                               "     model_no, "\
                               "     algorithm, "\
                               "     algorithm_list, "\
                               "     count_data, "\
                               "     features, "\
                               "     target, "\
                               "     first_place, "\
                               "     second_place, "\
                               "     third_place, "\
                               "     fourth_place, "\
                               "     fifth_place, "\
                               "     sixth_place, "\
                               "     seventh_place, "\
                               "     eighth_place "\
                               " ) "\
                               " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "

    # 選択 訓練データ
    select_train_data_for_anaylize = " SELECT ri.car_no 車番 "\
                                     "       ,ri.hande ハンデ "\
                                     "       ,ri.trialrun 試走タイム "\
                                     "       ,ri.deviation 試走偏差 "\
                                     "       ,ri.position_x 横ポジション "\
                                     "       ,ri.position_y 縦ポジション "\
                                     "       ,rr.racetime 競争タイム "\
                                     "       ,rr.rank 着順 "\
                                     "       ,rh.temperature 気温 "\
                                     "       ,rh.humidity 湿度 "\
                                     "       ,rh.runway_temperature 走路温度 "\
                                     "   FROM auto2.t_race_info ri "\
                                     "  INNER JOIN auto2.t_race_head rh "\
                                     "     ON ri.dated = rh.dated "\
                                     "    AND ri.place = rh.place "\
                                     "    AND ri.round = rh.round "\
                                     "  INNER JOIN auto2.t_race_result rr "\
                                     "     ON ri.dated = rr.dated "\
                                     "    AND ri.place = rr.place "\
                                     "    AND ri.round = rr.round "\
                                     "    AND ri.car_no = rr.car_no "\
                                     "  WHERE ri.racer = %s "\
                                     "    AND rh.runway_condition = %s "\
                                     "    AND rh.race_system = %s "\
                                     "    AND rh.race_type = %s "

    # 選択 テストデータ
    select_test_data_for_anaylize = " SELECT ri.car_no 車番 "\
                                    "       ,ri.hande ハンデ "\
                                    "       ,ri.trialrun 試走タイム "\
                                    "       ,ri.deviation 試走偏差 "\
                                    "       ,ri.position_x 横ポジション "\
                                    "       ,ri.position_y 縦ポジション "\
                                    "       ,rh.temperature 気温 "\
                                    "       ,rh.humidity 湿度 "\
                                    "       ,rh.runway_temperature 走路温度 "\
                                    "   FROM auto2.w_race_info ri "\
                                    "  INNER JOIN auto2.w_race_head rh "\
                                    "     ON ri.dated = rh.dated "\
                                    "    AND ri.place = rh.place "\
                                    "    AND ri.round = rh.round "\
                                    "  WHERE ri.dated = %s "\
                                    "    AND ri.place = %s "\
                                    "    AND ri.round = %s "\
                                    "    AND ri.car_no = %s "

    # 選択 予測モデル
    select_M_ANAYLIZE_MODEL = " SELECT am.model_no モデル "\
                              "       ,am.algorithm アルゴリズム "\
                              "       ,am.algorithm_list 詳細 "\
                              "       ,am.features インプット "\
                              "       ,am.target アウトプット "\
                              "   FROM auto2.m_anaylize_model am "


    ##### 月次処理用 #####
    # 選択 月次ログ
    select_T_MONTHLY_LOG = " SELECT TO_CHAR(dated, 'yyyy-mm-dd') 開催日 "\
                           "       ,place レース場 "\
                           "       ,round ラウンド "\
                           "   FROM auto2.t_monthly_log "\
                           "  WHERE status = 0 "\
                           "  ORDER BY dated, place, round "\
                           "  OFFSET 0 LIMIT 240 "

    # 挿入 月次ログ
    insert_T_MONTHLY_LOG = " INSERT INTO auto2.t_monthly_log ( "\
                            "     dated, "\
                            "     place, "\
                            "     round, "\
                            "     status, "\
                            "     err_msg "\
                            " ) "\
                            " VALUES (%s, %s, %s, %s, %s) "

    # 更新 月次ログ
    update_T_MONTHLY_LOG = " UPDATE auto2.t_monthly_log "\
                           "    SET status = %s "\
                           "       ,err_msg = %s "\
                           "  WHERE dated = %s "\
                           "    AND place = %s "\
                           "    AND round = %s "

    # 挿入 レースヘッダ
    insert_T_RACE_HEAD = " INSERT INTO auto2.t_race_head ( "\
                         "     dated, "\
                         "     place, "\
                         "     round, "\
                         "     race_name, "\
                         "     distance, "\
                         "     weather, "\
                         "     temperature, "\
                         "     humidity, "\
                         "     runway_temperature, "\
                         "     runway_condition, "\
                         "     race_system, "\
                         "     race_type "\
                         " ) "\
                         " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "

    # 挿入 レース情報
    insert_T_RACE_INFO = " INSERT INTO auto2.t_race_info ( "\
                          "     dated, "\
                          "     place, "\
                          "     round, "\
                          "     car_no, "\
                          "     racer, "\
                          "     represent, "\
                          "     hande, "\
                          "     trialrun, "\
                          "     deviation, "\
                          "     position_x, "\
                          "     position_y "\
                          " ) "\
                          " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "

    # 挿入 レース結果
    insert_T_RACE_RESULT = " INSERT INTO auto2.t_race_result ( "\
                           "     dated, "\
                           "     place, "\
                           "     round, "\
                           "     car_no, "\
                           "     racetime, "\
                           "     starttime, "\
                           "     rank "\
                          " ) "\
                          " VALUES (%s, %s, %s, %s, %s, %s, %s) "

    # 挿入 レース払戻
    insert_T_RACE_PAYOFF = " INSERT INTO auto2.t_race_payoff ( "\
                           "     dated, "\
                           "     place, "\
                           "     round, "\
                           "     payoff_3t, "\
                           "     payoff_3f, "\
                           "     payoff_2t, "\
                           "     payoff_2f, "\
                           "     payoff_1t, "\
                           "     first_place, "\
                           "     second_place, "\
                           "     third_place, "\
                           "     fourth_place, "\
                           "     fifth_place, "\
                           "     sixth_place, "\
                           "     seventh_place, "\
                           "     eighth_place "\
                          " ) "\
                          " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
