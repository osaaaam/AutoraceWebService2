import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../packages'))
from bs4 import BeautifulSoup
import requests


class Scraping:

    url_program = "http://autorace.jp/netstadium/Program/{}/{}_{}"
    url_result = "http://autorace.jp/netstadium/RaceResult/{}/{}_{}"

    # コンストラクタ
    # インスタンス変数のセットと、スクレイピングの実行
    # 複数urlのスクレイピングも考慮
    def __init__(self, url, list_dated, list_place, list_round):
        self.list_race_key = []
        self.list_soup = []
        for dated in list_dated:
            for place in list_place:
                for round in list_round:
                    self.list_race_key.append([dated, place, round])
                    url = url.format(place, dated, round)
                    html = requests.get(url)
                    self.list_soup.append(BeautifulSoup(html.text,"html.parser"))

    # soupデータから、目的とする値を取得する
    # 引数
    #  soup: BeautifulSoup(html.text,"html.parser")したもの
    #  tag_last: soupを解析し最終的にほしいhtmlタグ
    #  list_tag: soupを解析するhtmlタグを入れる
    #  list_tag_index: soupをhtmlタグで解析した後に絞るindexを入れる
    #                  （list_tagとlist_tag_indexは同じ要素数）
    #  list_pop_index: 解析してできた配列の中で削除したいindexを入れる
    #                  （複数入れる場合、forで削除していくことを考慮必要）
    def from_soup_to_list(self, soup, tag_last, list_tag, list_tag_index, list_pop_index):
        list = []
        soup_wk = soup
        for i in range(len(list_tag)):
            soup_wk = soup_wk.find_all(list_tag[i])[list_tag_index[i]]
        soup_wk = soup_wk.find_all(tag_last)
        for pop_index in list_pop_index:
            soup_wk.pop(pop_index)
        for tag in soup_wk:
            if tag.string is None:
                list.append(None)
            else:
                if tag.string.strip() == "":
                    list.append(None)
                else:
                    list.append(tag.string.strip())
        return list

    # スクレイピング結果からレース情報を取得する
    # エラーになった場合は、[]を格納
    def get_raceinfo_url_program(self):
        # 結果格納用
        self.out_list_header = []
        self.out_list_racer = []
        self.out_list_hande = []
        self.out_list_trialrun = []
        self.out_list_deviation = []
        self.out_list_represent = []

        for i in range(len(self.list_soup)):
            try:
                soup = self.list_soup[i]

                # ヘッダー
                # レース名はタグ構成が異なるため単体で取得
                wk_span_list_header = self.from_soup_to_list(soup, "span", ["table", "tr"], [0, 2], [])
                race_name = wk_span_list_header[0] + " " + wk_span_list_header[1] + "R"
                # レース名以外のヘッダー情報取得
                wk_td_list_header = self.from_soup_to_list(soup, "td", ["table", "tr"], [0, 2], [1, 0])
                # 当日日付のurlと過去日付のurlでは、スクレイピングで取得するタグ数が異なるため、差分を削除
                if len(wk_td_list_header) == 8:
                    del wk_td_list_header[1:3]
                # %とか不要なのを削除
                if wk_td_list_header[0] is not None:
                    wk_td_list_header[0] = wk_td_list_header[0][:-1]
                if wk_td_list_header[2] is not None:
                    wk_td_list_header[2] = wk_td_list_header[2][:-3]
                if wk_td_list_header[3] is not None:
                    wk_td_list_header[3] = wk_td_list_header[3][:-3]
                if wk_td_list_header[4] is not None:
                    wk_td_list_header[4] = wk_td_list_header[4][:-3]
                list_header = [race_name] + wk_td_list_header

                # 選手名
                list_racer = self.from_soup_to_list(soup, "a", ["table", "tr"], [3, 1], [])
                # 所属
                list_represent = self.from_soup_to_list(soup, "td", ["table", "tr"], [4, 4], [0])
                # ハンデ
                list_hande = self.from_soup_to_list(soup, "td", ["table", "tr"], [4, 1], [0])
                # 試走タイム
                list_trialrun = self.from_soup_to_list(soup, "td", ["table", "tr"], [4, 2], [0])
                # 試走偏差
                list_deviation = self.from_soup_to_list(soup, "td", ["table", "tr"], [4, 3], [0])

                # 結果を格納
                self.out_list_header.append(list_header)
                self.out_list_racer.append(list_racer)
                self.out_list_represent.append(list_represent)
                self.out_list_hande.append(list_hande)
                self.out_list_trialrun.append(list_trialrun)
                self.out_list_deviation.append(list_deviation)

            except Exception as e:
                print(e)
                # []を格納
                self.out_list_header.append([])
                self.out_list_racer.append([])
                self.out_list_represent.append([])
                self.out_list_hande.append([])
                self.out_list_trialrun.append([])
                self.out_list_deviation.append([])
