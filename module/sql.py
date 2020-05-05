class Sql:

    # 過去レースヘッダーテーブルから取得するSQL
    select_T_RACE_HEAD_by_racekey = " SELECT rh.race_name レース "\
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

    # 過去レース情報テーブルから取得するSQL
    select_T_RACE_RACER_by_racekey = " SELECT rr.car_no 車番 "\
                                     "       ,rr.racer 選手名 "\
                                     "       ,rr.hande ハンデ "\
                                     "       ,rr.trialrun 試走T "\
                                     "       ,rr.racetime 競争T "\
                                     "       ,rr.starttime ST "\
                                     "   FROM auto.t_race_racer rr "\
                                     "  WHERE rr.dated = %s "\
                                     "    AND rr.place = %s "\
                                     "    AND rr.round = %s "\
                                     "  ORDER BY rr.car_no "

    # 過去レース結果テーブルから取得するSQL
    select_T_RACE_RESULT_by_racekey = " SELECT rr.first_place １着 "\
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

    # 作業用レースヘッダーテーブルから取得するSQL
    select_W_RACE_HEAD_by_racekey = " SELECT rh.race_name レース "\
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

    # 作業用レース情報テーブルから取得するSQL
    select_W_RACE_RACER_by_racekey = " SELECT rr.car_no 車番 "\
                                     "       ,rr.racer 選手名 "\
                                     "       ,rr.represent 所属 "\
                                     "       ,rr.hande ハンデ "\
                                     "       ,rr.trialrun 試走T "\
                                     "       ,rr.deviation 試走偏差 "\
                                     "   FROM auto.w_race_racer rr "\
                                     "  WHERE rr.dated = %s "\
                                     "    AND rr.place = %s "\
                                     "    AND rr.round = %s "\
                                     "  ORDER BY rr.car_no "

    # 作業用レースヘッダーテーブルに挿入するSQL
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

    # 作業用レース情報テーブルに挿入するSQL
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
