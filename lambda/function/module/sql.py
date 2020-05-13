class Sql:

    # 画面表示用 SQL
    select_W_PLACE_by_dated = " SELECT wp.place レース場 "\
                              "   FROM auto.w_place wp "\
                              "  WHERE wp.dated = %s "

    # 画面表示用 SQL
    select_T_RACE_HEAD_for_view = " SELECT rh.race_name レース "\
                                    "       ,rh.distance 距離 "\
                                    "       ,rh.weather 天候 "\
                                    "       ,rh.temperature 気温 "\
                                    "       ,rh.humidity 湿度 "\
                                    "       ,rh.runway_temperature 走路温度 "\
                                    "       ,rh.runway_condition 走路状況 "\
                                    "   FROM auto.t_race_head rh "\
                                    "  WHERE rh.dated = %s "\
                                    "    AND rh.place = %s "\
                                    "    AND rh.round = %s "

    # 画面表示用 SQL
    select_T_RACE_RACER_for_view = " SELECT rr.car_no 車番 "\
                                     "       ,rr.racer 選手名 "\
                                     "       ,rr.hande ハンデ "\
                                     "       ,rr.trialrun 試走タイム "\
                                     "       ,rr.racetime 競争タイム "\
                                     "       ,rr.starttime ST "\
                                     "   FROM auto.t_race_racer rr "\
                                     "  WHERE rr.dated = %s "\
                                     "    AND rr.place = %s "\
                                     "    AND rr.round = %s "\
                                     "  ORDER BY rr.car_no "

    # 画面表示用 SQL
    select_T_RACE_RESULT_for_view = " SELECT rr.first_place １着 "\
                                      "       ,rr.second_place ２着 "\
                                      "       ,rr.third_place ３着 "\
                                      "       ,rr.payoff_2t ３連単 "\
                                      "       ,rr.payoff_2f ３連複 "\
                                      "       ,rr.payoff_3t ２連単 "\
                                      "       ,rr.payoff_3f ２連複 "\
                                      "       ,rr.payoff_1t 単勝 "\
                                      "   FROM auto.t_race_result rr "\
                                      "  WHERE rr.dated = %s "\
                                      "    AND rr.place = %s "\
                                      "    AND rr.round = %s "

    # 画面表示用 SQL
    select_W_RACE_HEAD_for_view = " SELECT rh.race_name レース "\
                                    "       ,rh.distance 距離 "\
                                    "       ,rh.weather 天候 "\
                                    "       ,rh.temperature 気温 "\
                                    "       ,rh.humidity 湿度 "\
                                    "       ,rh.runway_temperature 走路温度 "\
                                    "       ,rh.runway_condition 走路状況 "\
                                    "   FROM auto.w_race_head rh "\
                                    "  WHERE rh.dated = %s "\
                                    "    AND rh.place = %s "\
                                    "    AND rh.round = %s "

    # 画面表示用 SQL
    select_W_RACE_RACER_for_view = " SELECT rr.car_no 車番 "\
                                     "       ,rr.racer 選手名 "\
                                     "       ,rr.represent 所属 "\
                                     "       ,rr.hande ハンデ "\
                                     "       ,rr.trialrun 試走タイム "\
                                     "       ,rr.deviation 試走偏差 "\
                                     "   FROM auto.w_race_racer rr "\
                                     "  WHERE rr.dated = %s "\
                                     "    AND rr.place = %s "\
                                     "    AND rr.round = %s "\
                                     "  ORDER BY rr.car_no "

    # 挿入 SQL
    insert_W_PLACE = " INSERT INTO auto.w_place ( "\
                         "     dated, "\
                         "     place "\
                         " ) "\
                         " VALUES (%s, %s) "

    # 挿入 SQL
    insert_W_RACE_HEAD = " INSERT INTO auto.w_race_head ( "\
                         "     dated, "\
                         "     place, "\
                         "     round, "\
                         "     race_name, "\
                         "     distance, "\
                         "     weather, "\
                         "     temperature, "\
                         "     humidity, "\
                         "     runway_temperature, "\
                         "     runway_condition "\
                         " ) "\
                         " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "

    # 挿入 SQL
    insert_W_RACE_RACER = " INSERT INTO auto.w_race_racer ( "\
                          "     dated, "\
                          "     place, "\
                          "     round, "\
                          "     car_no, "\
                          "     racer, "\
                          "     represent, "\
                          "     hande, "\
                          "     trialrun, "\
                          "     deviation, "\
                          "     position "\
                          " ) "\
                          " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "

    # 削除 SQL
    delete_W_RACE_HEAD_by_racekey = " DELETE FROM auto.w_race_head rh "\
                                    "  WHERE rh.dated = %s "\
                                    "    AND rh.place = %s "\
                                    "    AND rh.round = %s "

    # 削除 SQL
    delete_W_RACE_RACER_by_racekey = " DELETE FROM auto.w_race_racer rr "\
                                    "  WHERE rr.dated = %s "\
                                    "    AND rr.place = %s "\
                                    "    AND rr.round = %s "

    # 分析用 SQL
    select_train_data_for_anaylize = " SELECT rr.car_no 車番 "\
                                     "       ,rr.hande ハンデ "\
                                     "       ,rr.trialrun 試走タイム "\
                                     "       ,rr.racetime 競争タイム "\
                                     "       ,rr.rank 着順 "\
                                     "       ,rh.temperature 気温 "\
                                     "       ,rh.humidity 湿度 "\
                                     "       ,rh.runway_temperature 走路温度 "\
                                     "       ,(select column_out from auto.m_convert where column_in = rh.place) レース場 "\
                                     "       ,CASE "\
                                     "          WHEN rr.car_no=1 THEN po.first_car "\
                                     "          WHEN rr.car_no=2 THEN po.second_car "\
                                     "          WHEN rr.car_no=3 THEN po.third_car "\
                                     "          WHEN rr.car_no=4 THEN po.fourth_car "\
                                     "          WHEN rr.car_no=5 THEN po.fifth_car "\
                                     "          WHEN rr.car_no=6 THEN po.sixth_car "\
                                     "          WHEN rr.car_no=7 THEN po.seventh_car "\
                                     "          WHEN rr.car_no=8 THEN po.eighth_car "\
                                     "          ELSE 0 "\
                                     "        END ポジション "\
                                     "       ,( "\
                                     "          select count(*) "\
                                     "            from auto.w_race_racer "\
                                     "           where dated = rr.dated "\
                                     "             and place = rr.place "\
                                     "             and round = rr.round "\
                                     "             and hande < rr.hande "\
                                     "        ) ハンデ前車数 "\
                                     "   FROM auto.t_race_racer rr "\
                                     "  INNER JOIN auto.t_race_head rh "\
                                     "     ON rr.dated = rh.dated "\
                                     "    AND rr.place = rh.place "\
                                     "    AND rr.round = rh.round "\
                                     "  INNER JOIN auto.t_race_position po "\
                                     "     ON rr.dated = po.dated "\
                                     "    AND rr.place = po.place "\
                                     "    AND rr.round = po.round "\
                                     "  WHERE rr.racer = %s "\
                                     "    AND rh.distance = %s "\
                                     "    AND rh.runway_condition = %s "

    # 分析用 SQL
    select_test_data_for_anaylize = " SELECT rr.car_no 車番 "\
                                    "       ,rr.hande ハンデ "\
                                    "       ,rr.trialrun 試走タイム "\
                                    "       ,rr.position ポジション "\
                                    "       ,rh.temperature 気温 "\
                                    "       ,rh.humidity 湿度 "\
                                    "       ,rh.runway_temperature 走路温度 "\
                                    "       ,(select column_out from auto.m_convert where column_in = rh.place) レース場 "\
                                    "       ,( "\
                                    "          select count(*) "\
                                    "            from auto.w_race_racer "\
                                    "           where dated = rr.dated "\
                                    "             and place = rr.place "\
                                    "             and round = rr.round "\
                                    "             and hande < rr.hande "\
                                    "        ) ハンデ前車数 "\
                                    "   FROM auto.w_race_racer rr "\
                                    "  INNER JOIN auto.w_race_head rh "\
                                    "     ON rr.dated = rh.dated "\
                                    "    AND rr.place = rh.place "\
                                    "    AND rr.round = rh.round "\
                                    "  WHERE rr.dated = %s "\
                                    "    AND rr.place = %s "\
                                    "    AND rr.round = %s "\
                                    "    AND rr.car_no = %s "

    # 分析用 SQL
    select_M_ANAYLIZE_MODEL = " SELECT am.model_no モデル "\
                              "       ,am.algorithm アルゴリズム "\
                              "       ,am.algorithm_list 詳細 "\
                              "       ,am.features インプット "\
                              "       ,am.target アウトプット "\
                              "   FROM auto.m_anaylize_model am "

    # 画面表示用分析用 SQL
    select_W_ANAYLIZE_RESULT_RANK_for_view = " SELECT ar.model_no モデル "\
                                        "       ,ar.algorithm アルゴリズム "\
                                        "       ,ar.count_data 学習件数 "\
                                        "       ,ar.features インプット "\
                                        "       ,ar.target アウトプット "\
                                        "       ,ar.first_place ◎ "\
                                        "       ,ar.second_place ○ "\
                                        "       ,ar.third_place ▲ "\
                                        "       ,ar.fourth_place △ "\
                                        "   FROM auto.w_anaylize_result_rank ar "\
                                        "  WHERE ar.dated = %s "\
                                        "    AND ar.place = %s "\
                                        "    AND ar.round = %s "

    # 画面表示用分析用 SQL
    select_W_ANAYLIZE_RESULT_VALUE_for_view = " SELECT av.model_no モデル "\
                                               "       ,av.first_car １号車 "\
                                               "       ,av.second_car ２号車 "\
                                               "       ,av.third_car ３号車 "\
                                               "       ,av.fourth_car ４号車 "\
                                               "       ,av.fifth_car ５号車 "\
                                               "       ,av.sixth_car ６号車 "\
                                               "       ,av.seventh_car ７号車 "\
                                               "       ,av.eighth_car ８号車 "\
                                               "   FROM auto.w_anaylize_result_value av "\
                                               "  WHERE av.dated = %s "\
                                               "    AND av.place = %s "\
                                               "    AND av.round = %s "

    # 分析用 SQL
    insert_W_ANAYLIZE_RESULT_RANK = " INSERT INTO auto.w_anaylize_result_rank ( "\
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

    # 分析用 SQL
    insert_W_ANAYLIZE_RESULT_VALUE = " INSERT INTO auto.w_anaylize_result_value ( "\
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

    # 分析用 SQL
    select_W_ANAYLIZE_RESULT_VALUE_for_anaylize = " SELECT SUM(av.first_car) １号車 "\
                                                   "       ,SUM(av.second_car) ２号車 "\
                                                   "       ,SUM(av.third_car) ３号車 "\
                                                   "       ,SUM(av.fourth_car) ４号車 "\
                                                   "       ,SUM(av.fifth_car) ５号車 "\
                                                   "       ,SUM(av.sixth_car) ６号車 "\
                                                   "       ,SUM(av.seventh_car) ７号車 "\
                                                   "       ,SUM(av.eighth_car) ８号車 "\
                                                   "   FROM auto.w_anaylize_result_value av "\
                                                   "  WHERE av.dated = %s "\
                                                   "    AND av.place = %s "\
                                                   "    AND av.round = %s "\
                                                   "    AND av.model_no IN (%s, %s, %s, %s, %s) "\
                                                   "  GROUP BY av.dated, av.place, av.round "
