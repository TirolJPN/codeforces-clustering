"""
ToDo
lexicalな方法で3つのファイルに、metricalな方法でインデックス付されている
箱ひげ図の作成のため、submission_id, lexical_id, metrical_id, 全メトリクス値を持った
1つのcsvファイルが必要

作業の流れとしては、
- 新規csvファイルを作成する
- 3つのcsvファイル(クラスタリングの結果が格納されている)を読み込んできて、下記をループ
    - submission_idをもとに、M1 ~ M12を取得
    - submission_id、lexical_id, metrical_idをそのままコピーする

手作業で箱ひげ図の作成を行う。
"""

import sys
import csv
from my_library import key

class ExecCreateBoxPlotCSV():
    def __init__(self, problem_id):
        # initialize all constants
        self.PATH_SRC = key.PATH_SRC
        self.PATH_LEXICAL_INDEXED_SRC = key.PATH_LEXICAL_INDEXED_SRC
        self.PATH_METRICAL_INDEXED_SRC = key.PATH_METRICAL_INDEXED_SRC
        self.PATH_METRIC_VALUES = key.PATH_METRIC_VALUES
        self.PATH_PLOT_RESULTS = key.PATH_PLOT_RESULTS
        self.NUM_LEXICAL_CLUSTERS = key.NUM_LEXICAL_CLUSTERS
        self.NUM_METRICAL_CLUSTERS = key.NUM_METRICAL_CLUSTERS

        self.METRICS = ['cosine']
        # self.METHODS = ['single', 'average', 'complete', 'weighted']
        self.METHODS = ['complete']
        self.RANGE_LEXICAL_CLUSTER = range(1, self.NUM_LEXICAL_CLUSTERS + 1)
        self.RANGE_METRICAL_CLUSTER = range(1, self.NUM_METRICAL_CLUSTERS + 1)

        # read 3 target csv files
        # the name of target csv is like [pronlem_id]_[lexical_id].csv
        for metric in self.METRICS:
            for method in self.METHODS:
                for lexical_id in self.RANGE_LEXICAL_CLUSTER:
                    # print(lexical_id)
                    INDEXED_CSV_NAME = '%s%s/%s/%s/%s_%s.csv' % (self.PATH_PLOT_RESULTS, problem_id, metric, method, problem_id, lexical_id)
                    with open(INDEXED_CSV_NAME, "r", encoding="utf-8") as INDEXED_CSV:
                        INDEXED_CSV_F = csv.reader(INDEXED_CSV, delimiter=",", lineterminator="\n")
                        next(INDEXED_CSV_F)
                        for row_indexed_csv in INDEXED_CSV_F:
                            print(row_indexed_csv)
                     




def main():
    args = sys.argv
    if len(args) > 1:
        for problem_id in args[1:]:
            ExecCreateBoxPlotCSV(problem_id)

if __name__ == "__main__":
    main() 