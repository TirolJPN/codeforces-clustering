"""
TODO:
ngweightでで作成した特徴語のリストから、そのN-gramの種類の数だけの次元の特徴ベクトルを
決まったフォーマットで作成する。
クラスタリング・可視化は別のスクリプトで行う。
pythonにおける階層クラスタリングは次を参照 https://qiita.com/suecharo/items/20bad5f0bb2079257568
問題の種類によっては次元数がアホみたいなことになるが、気にしないでとりあえず実行する
クラスタリング手法には最長距離法、メトリクスにはコサイン類似度(コサイン距離)を用いる

引数のproblem_idごとに以下を実行する
1. 入力ファイル(input_files/hoge.txt)を参照する。1解答ごとに
    0x02[file_name]0x03 {単語群} 0x02[file_name]0x03 {単語群} 0x02[file_name]0x03 {単語群}...
    の形式になっているので、0x02[file_name]0x03を区切りに、1解答づつの文章を取得
2. output_filesの特徴語のリストと照らし合わせて、特徴語の種類(outputfileの行数と同じ)の次元を持つ特徴ベクトルを作成
    文字列検索をN-gramの種類だけやるので相当時間かかりそう 
    ベクトルはCSVの方が良い(ioの数を少なくするため。縦軸がファイル名、横軸が、N-gramの項目を取る)
"""

import os
import mysql.connector as cn
from pyquery import PyQuery as pq
from enum import  Enum
import re
import subprocess
import sys
import csv
from my_library import key
from my_library import Connector
import pandas as pd
from itertools import chain

"""
出現した特徴N-gramの数をカウントする
"""
class VectorCreater(Connector.Connector):
    """
    problem_idを引数として、前解答の特徴ベクトルの情報を持つCSVファイルを作成する
    """
    def __init__(self, problem_id):
        self.PATH_INPUT_FILES = key.PATH_INPUT_FILES
        self.PATH_OUTPUT_FILES = key.PATH_OUTPUT_FILES
        self.PATH_VECTOR_FILES = key.PATH_VECTOR_FILES
        self.PATH_METRIC_VALUES = key.PATH_METRIC_VALUES
        keywords_list = self.get_keywords_list(problem_id)
        # N-gram一覧の取得に成功したら
        vector_csv_path = self.PATH_VECTOR_FILES + problem_id + '.csv'
        if (keywords_list != False):
            with open(vector_csv_path, 'w', encoding='utf-8') as f_csv_file:
                # 1行目に各N-Gramの項目を入れておく
                writer = csv.writer(f_csv_file, lineterminator='\n')
                keywords_list.insert(0, 'submission_id')
                writer.writerow(keywords_list)
                keywords_list.pop(0)

                # 各提出毎にN-Gramをカウントし、csvに入れる
                self.create_keyword_vectors(problem_id, keywords_list, writer)


    """
    problem_idを引数として、output_filesの特徴語一覧のlistを返り値とする
    失敗したら，falseを返す
    """
    def get_keywords_list(self, problem_id):
        path_output_file = self.PATH_OUTPUT_FILES + problem_id + '_output'
        # ファイルが存在すれば、N-gramの一覧を取得する
        if os.path.isfile(path_output_file):
            list = []
            with open(path_output_file, mode='r', encoding='utf-8') as f_output_file:
                # output_file から一行ずつ取得する
                keyword_row = f_output_file.readline()
                while keyword_row:
                    keyword = keyword_row.split(chr(9))[5].strip()
                    # keywordがN-gramに該当
                    list.append(keyword)
                    keyword_row = f_output_file.readline()
            return list
        else:
            return False


    """
    problem_id、N-gramのリスト、出力csvファイルのファイルポインタを引数にして、該当解答の一覧を返す
    ソースコードはinput_filesの解答を利用する

    0x02[ファイル名]0x03[本文]0x02[ファイル名]0x03[本文]0x02[ファイル名]0x03[本文]...

    の状態になっているので、それで、分割する
    """
    def create_keyword_vectors(self, problem_id, n_gram_list, writer):
        input_file_path = self.PATH_INPUT_FILES + problem_id + '.txt'

        path_metric_values_csv = '%s%s.csv' % (self.PATH_METRIC_VALUES, problem_id)
        df = pd.read_csv(path_metric_values_csv, usecols=[1])
        target_submission_ids = list(chain.from_iterable(df.values.tolist()))
        # source monoitorの計測値があるsubmission_idの一覧を取得

        # ファイルが存在するならば
        if os.path.isfile(input_file_path):
            with open(input_file_path, 'r', encoding='utf-8') as f_input_file:
                code_contents = f_input_file.read()
            splited_code_contents = [i for i in re.split(chr(2), code_contents ) if i != '']
            for splited_code_content in splited_code_contents:
                tmp = splited_code_content.split(chr(3))

                file_name = tmp[0].split('_')[-2]

                if int(file_name) in target_submission_ids:
                    code = tmp[1]
                    # n-gramごとに探索する
                    n_gram_count_list = [file_name]
                    for n_gram in n_gram_list:
                        count = code.count(n_gram)
                        n_gram_count_list.append(count)
                    writer.writerow(n_gram_count_list)
                else:
                    continue


def main():
    args = sys.argv
    if len(args) != 1:
        for problem_id in args[1:]:
            VectorCreater(problem_id)
        

if __name__ == '__main__':
    main()