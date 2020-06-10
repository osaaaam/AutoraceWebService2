import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../packages'))
import requests
from bs4 import BeautifulSoup


class Scraping:
    url_program = "http://autorace.jp/netstadium/Program/{}/{}_{}"
    url_result = "http://autorace.jp/netstadium/RaceResult/{}/{}_{}"

    # インスタンス変数のセットと、スクレイピングの実行
    # 複数urlのスクレイピングも考慮
    def __init__(self, url_, l_dated, l_place, l_round):
        self.l_l_race_key = []
        self.l_soup = []
        for dated in l_dated:
            for place in l_place:
                for round in l_round:
                    self.l_l_race_key.append([dated, place, round])
                    url = url_.format(place, dated, round)
                    html = requests.get(url)
                    self.l_soup.append(BeautifulSoup(html.text,"html.parser"))

    # soupデータから、目的とする値を取得する
    # 引数
    #  soup: BeautifulSoup(html.text,"html.parser")したもの
    #  tag_last: soupを解析し最終的にほしいhtmlタグ
    #  l_tag: soupを解析するhtmlタグを入れる
    #  l_tag_index: soupをhtmlタグで解析した後に絞るindexを入れる
    #                  （l_tagとl_tag_indexは同じ要素数）
    #  l_pop_index: 解析してできた配列の中で削除したいindexを入れる
    #                  （複数入れる場合、forで削除していくことを考慮必要）
    def from_soup_to_list(self, soup, tag_last, l_tag, l_tag_index, l_pop_index):
        l_result = []
        for i in range(len(l_tag)):
            soup = soup.find_all(l_tag[i])[l_tag_index[i]]
        soup = soup.find_all(tag_last)
        for pop_index in l_pop_index:
            soup.pop(pop_index)
        for tag in soup:
            if tag.string is None:
                l_result.append(None)
            else:
                if tag.string.strip() == "":
                    l_result.append(None)
                else:
                    l_result.append(tag.string.strip())
        return l_result

    # ヘッダー情報を取得
    def get_header(self, soup, l_hande):
        # レース名はタグ構成が異なるため単体で取得
        l_header_span = self.from_soup_to_list(soup, "span", ["table", "tr"], [0, 2], [])
        race_name = l_header_span[0] + " " + l_header_span[1] + "R"
        # レース名以外のヘッダー情報取得
        l_header_td = self.from_soup_to_list(soup, "td", ["table", "tr"], [0, 2], [1, 0])
        # 当日日付のurlと過去日付のurlでは、スクレイピングで取得するタグ数が異なるため、差分を削除
        if len(l_header_td) == 8:
            del l_header_td[1:3]
        # %とか不要なのを削除
        if l_header_td[0] is not None:
            l_header_td[0] = l_header_td[0][:-1]
        if l_header_td[2] is not None:
            l_header_td[2] = l_header_td[2][:-3]
        if l_header_td[3] is not None:
            l_header_td[3] = l_header_td[3][:-3]
        if l_header_td[4] is not None:
            l_header_td[4] = l_header_td[4][:-3]
        # 通常レースか7車制か取得
        car_count = len(self.from_soup_to_list(soup, "a", ["table", "tr"], [3, 1], []))
        race_system = str(car_count) + "車制"
        # レース種別
        race_type = "オープン戦"
        for i in range(len(l_hande)):
            if l_hande[i] is not None:
                if l_hande[0] != l_hande[i]:
                    race_type = "ハンデ戦"

        return [race_name] + l_header_td + [race_system] + [race_type]

    # 同ハンデ内での内順を取得
    def get_position_x(self, l_hande):
        l_position_x = []
        for i in range(len(l_hande)):
            # 1号車の場合
            if i == 0:
                l_position_x.append(1)
            # 2号車以降の場合
            else:
                if l_hande[i] == l_hande[i-1]:
                    l_position_x.append(l_position_x[i-1]+1)
                else:
                    l_position_x.append(1)
        return l_position_x

    # ハンデの少ない順を取得
    def get_position_y(self, l_hande):
        l_position_y = []
        for i in range(len(l_hande)):
            # 1号車の場合
            if i == 0:
                l_position_y.append(1)
            # 2号車以降の場合
            else:
                if l_hande[i] == l_hande[i-1]:
                    l_position_y.append(l_position_y[i-1])
                else:
                    l_position_y.append(l_position_y[i-1]+1)
        return l_position_y

    # スクレイピング結果からレース情報を取得する
    # エラーになった場合は、[]を格納
    def get_raceinfo_by_url_program(self):

        try:
            soup = self.l_soup[0]
            # ハンデ
            self.out_l_hande = self.from_soup_to_list(soup, "td", ["table", "tr"], [4, 1], [0])
            # 選手名
            self.out_l_racer = self.from_soup_to_list(soup, "a", ["table", "tr"], [3, 1], [])
            # 所属
            self.out_l_represent = self.from_soup_to_list(soup, "td", ["table", "tr"], [4, 4], [0])
            # 試走タイム
            self.out_l_trialrun = self.from_soup_to_list(soup, "td", ["table", "tr"], [4, 2], [0])
            # 試走偏差
            self.out_l_deviation = self.from_soup_to_list(soup, "td", ["table", "tr"], [4, 3], [0])
            # ポジション
            self.out_l_position_x = self.get_position_x(self.out_l_hande)
            # 縦ポジション
            self.out_l_position_y = self.get_position_y(self.out_l_hande)
            # ヘッダー
            self.out_l_header = self.get_header(soup, self.out_l_hande)

        except Exception as e:
            print(str(e))
            # 初期化
            self.out_l_header = []
            self.out_l_racer = []
            self.out_l_hande = []
            self.out_l_trialrun = []
            self.out_l_deviation = []
            self.out_l_represent = []
            self.out_l_position_x = []
            self.out_l_position_y = []
            # エラーメッセージセット
            self.out_err_msg = str(e)


    # スクレイピング結果からレース結果を取得する
    # エラーになった場合は、[]を格納
    def get_raceresult_by_url_result(self):
        # 結果格納用
        self.out_l_rank = []
        self.out_l_car_no = []
        self.out_l_racetime = []
        self.out_l_starttime = []
        self.out_l_payoff = []

        try:
            soup = self.l_soup[0]
            # 車分だけループ（7車制対応）
            car_count = len(self.from_soup_to_list(soup, "tr", ["table"], [3], []))-1
            for i in range(car_count):
                # 1着から、着順、車番、競争タイム、スタートタイムを取得
                l_result_wk = self.from_soup_to_list(soup, "td", ["table", "tr"], [3, i+1], [10, 7, 6, 5, 4, 3, 1])
                # 結果を格納
                self.out_l_rank.append(l_result_wk[0])
                self.out_l_car_no.append(l_result_wk[1])
                self.out_l_racetime.append(l_result_wk[2])
                self.out_l_starttime.append(l_result_wk[3])

            # 払戻額を取得（3連単、3連複、2連単、2連複、単勝）
            for i in [4, 5, 2, 3, 9]:
                l_payoff = self.from_soup_to_list(soup, "td", ["table", "tr"], [5, i], [3, 1, 0])
                self.out_l_payoff.append(l_payoff[0].replace(",","")[:-1])

        except Exception as e:
            print(str(e))
            # 初期化
            self.out_l_rank = []
            self.out_l_car_no = []
            self.out_l_racetime = []
            self.out_l_starttime = []
            self.out_l_payoff = []
            # エラーメッセージセット
            self.out_err_msg = str(e)


    # スクレイピング結果からレース場を取得する
    # エラーになった場合は、[]を格納
    def get_place_by_url_program(self):
        # 結果格納用
        self.out_list_place = []
        # まずはスクレイピングした分のレース場をセット
        for l_race_key in self.l_l_race_key:
            self.out_list_place.append(l_race_key[1])
        # 次に開催してないレース場を削除していく
        try:
            for i in range(len(self.l_soup)):
                soup = self.l_soup[i]
                #divタグのid=tabs3で検索（ある=未開催）
                soup = soup.find_all("div", id="tabs3")
                if len(soup) > 0:
                    self.out_list_place.remove(self.l_l_race_key[i][1])

        except Exception as e:
            print(str(e))
            # 初期化
            self.out_list_place = []
