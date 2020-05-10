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
                                     "       ,rh.temperature 気温 "\
                                     "       ,rh.humidity 湿度 "\
                                     "       ,rh.runway_temperature 走路温度 "\
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
                                    "   FROM auto.w_race_racer rr "\
                                    "  INNER JOIN auto.w_race_head rh "\
                                    "     ON rr.dated = rh.dated "\
                                    "    AND rr.place = rh.place "\
                                    "    AND rr.round = rh.round "\
                                    "  WHERE rr.dated = %s "\
                                    "    AND rr.place = %s "\
                                    "    AND rr.round = %s "\
                                    "    AND rr.car_no = %s "
