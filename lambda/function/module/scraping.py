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
        self.l_race_key = []
        self.l_soup = []
        for dated in l_dated:
            for place in l_place:
                for round in l_round:
                    self.l_race_key.append([dated, place, round])
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
    def get_header(self, soup):
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
        return [race_name] + l_header_td

    # 同ハンデ内での内順を取得
    def get_position(self, l_hande):
        l_position = []
        for i in range(len(l_hande)):
            # 1号車の場合
            if i == 0:
                l_position.append(1)
            # 2号車以降の場合
            else:
                if l_hande[i] == l_hande[i-1]:
                    l_position.append(l_position[i-1]+1)
                else:
                    l_position.append(1)
        return l_position

    # スクレイピング結果からレース情報を取得する
    # エラーになった場合は、[]を格納
    def get_raceinfo_url_program(self):
        # 結果格納用
        self.out_lists_header = []
        self.out_lists_racer = []
        self.out_lists_hande = []
        self.out_lists_trialrun = []
        self.out_lists_deviation = []
        self.out_lists_represent = []
        self.out_lists_position = []

        for i in range(len(self.l_soup)):
            try:
                soup = self.l_soup[i]
                # ヘッダー
                l_header = self.get_header(soup)
                # 選手名
                l_racer = self.from_soup_to_list(soup, "a", ["table", "tr"], [3, 1], [])
                # 所属
                l_represent = self.from_soup_to_list(soup, "td", ["table", "tr"], [4, 4], [0])
                # ハンデ
                l_hande = self.from_soup_to_list(soup, "td", ["table", "tr"], [4, 1], [0])
                # 試走タイム
                l_trialrun = self.from_soup_to_list(soup, "td", ["table", "tr"], [4, 2], [0])
                # 試走偏差
                l_deviation = self.from_soup_to_list(soup, "td", ["table", "tr"], [4, 3], [0])
                # ポジション
                l_position = self.get_position(l_hande)

                # 結果を格納
                self.out_lists_header.append(l_header)
                self.out_lists_racer.append(l_racer)
                self.out_lists_represent.append(l_represent)
                self.out_lists_hande.append(l_hande)
                self.out_lists_trialrun.append(l_trialrun)
                self.out_lists_deviation.append(l_deviation)
                self.out_lists_position.append(l_position)

            except Exception as e:
                print(str(e))
                # []を格納
                self.out_lists_header.append([])
                self.out_lists_racer.append([])
                self.out_lists_represent.append([])
                self.out_lists_hande.append([])
                self.out_lists_trialrun.append([])
                self.out_lists_deviation.append([])
                self.out_lists_position.append([])
