# import os
import sys
import json
import datetime
import csv

import requests
import lxml.html

# loggerの設定
# https://qiita.com/amedama/items/b856b2f30c2f38665701
from logging import basicConfig, getLogger, DEBUG

import config
from item import ShoheiBattingScore

# loggerのconfig
fmt = "%(asctime)s %(levelname)s %(name)s :%(message)s"
basicConfig(filename='logs/req2url.log', level=DEBUG, format=fmt)
logger = getLogger(__name__)


def main():
    '''
    main process
    '''
    # 開始
    logger.debug('start')

    # 固定パラメータ取得
    URL = config.TARGET_URL
    CSV_SAVEPATH = config.CSV_SAVEPATH

    # Parse the URL text(from def) by lxml
    tree = lxml.html.fromstring(fetch_txt_from_req(URL))

    # スクレイプ処理
    scrape_shohei_batting_score(tree, CSV_SAVEPATH)

    # 終了
    logger.debug('end')


def fetch_txt_from_req(url: str) -> str:
    '''
    GET request from recived URL
    Return: str type HTML(encoded)
    '''
    # GET
    r = requests.get(url)
    # get encode
    encoding = r.headers['Content-Encoding']
    # encode
    r.encoding = encoding
    # log
    logger.debug('got text from url')
    # return encoded text
    return r.text



def scrape_shohei_batting_score(tree: lxml.html.HtmlElement, csv_savepath: str) -> None:
    '''
    スクレイプ関係の処理をまとめて行う、CSSセレクタは本関数で固定値処理している
    メンテが必要になった場合本関数を変更
    Return: None
    '''
    # 対象テーブルの絞り込み
    target_divchild_list = []
    # 月単位の取得位置であるdiv:nth-childの確認
    # 12ヶ月以上のデータは表示されないという前提で12回回す
    for i in range(12):
        current_selector = tree.cssselect(f'#main2 > div:nth-child({i}) > h3')
        # 「7月」など見出しの有る表のnth-child番号をリスト化しておく
        if len(current_selector) >= 1:
            target_divchild_list.append(i)

    # 初回フラグ
    has_saved_csv = False

    # 絞り込んだ対象テーブルの情報をもとに、各月ごとのデータを取得
    for target_num in target_divchild_list:
        # 対象月のlog
        logger.debug(tree.cssselect(f'#main2 > div:nth-child({target_num}) > h3')[0].text_content())
        # print(tree.cssselect(f'#main2 > div:nth-child({target_num}) > h3')[0].text_content())
        # 対象試合日の絞り込み
        # target_date_list = []
        # 対象月のデータ業があるのはtarget_divchild_listに記載されている番号の+1なので
        target_num += 1
        # 1ヶ月30試合以上は表示されないという前提で30回回す
        for i in range(30):
            # 表の右端にある「盗塁」列が取得できるセレクタだけ回す（合計行は盗塁列がない）
            current_selector = tree.cssselect(f'#main2 > div:nth-child({target_num})  > table > tr:nth-child({i}) > td:nth-child(18)')
            if len(current_selector) == 1:
                # リスト追記(確認用)
                # target_date_list.append(i)
                # 以下、取得対象の列データを取得
                shohei_batting_score= ShoheiBattingScore(
                    # game_date(試合日)
                    tree.cssselect(f'#main2 > div:nth-child({target_num}) > table > tr:nth-child({i}) > th')[0].text_content()
                    # at_bat(打数)
                    , tree.cssselect(f'#main2 > div:nth-child({target_num}) > table > tr:nth-child({i}) > td:nth-child(6)')[0].text_content()
                    # run(得点)
                    , tree.cssselect(f'#main2 > div:nth-child({target_num}) > table > tr:nth-child({i}) > td:nth-child(7)')[0].text_content()
                    # hit(ヒット)
                    , tree.cssselect(f'#main2 > div:nth-child({target_num}) > table > tr:nth-child({i}) > td:nth-child(7)')[0].text_content()
                    # home_run(hr)
                    , tree.cssselect(f'#main2 > div:nth-child({target_num}) > table > tr:nth-child({i}) > td:nth-child(11)')[0].text_content()
                    # strikeout(三振)
                    , tree.cssselect(f'#main2 > div:nth-child({target_num}) > table > tr:nth-child({i}) > td:nth-child(13)')[0].text_content()
                    # bb(四球)
                    , tree.cssselect(f'#main2 > div:nth-child({target_num}) > table > tr:nth-child({i}) > td:nth-child(14)')[0].text_content()
                    # steal(盗塁)
                    , tree.cssselect(f'#main2 > div:nth-child({target_num}) > table > tr:nth-child({i})  > td:nth-child(18)')[0].text_content()
                )
                # 初回のみヘッダ作成
                if has_saved_csv is False:
                    shohei_batting_score.generate_csv(csv_savepath)
                    has_saved_csv = True
                # csv保存
                shohei_batting_score.save2csv(csv_savepath)


if __name__ == '__main__':
    main()

