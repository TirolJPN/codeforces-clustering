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
import pandas as pd
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

        metric_values_list_df = self.load_mtric_values(problem_id)
        print(metric_values_list_df)
        if not(metric_values_list_df.empty):
            for metric in self.METRICS:
                for method in self.METHODS:
                    for lexical_id in self.RANGE_LEXICAL_CLUSTER:
                        
                        # read 3 target csv files
                        # the name of target csv is like [pronlem_id]_[lexical_id].csv
                        try:
                            INDEXED_CSV_NAME = '%s%s/%s/%s/%s_%s.csv' % (self.PATH_PLOT_RESULTS, problem_id, metric, method, problem_id, lexical_id)
                            target_indexed_csv_df = pd.read_csv(INDEXED_CSV_NAME, delimiter=",")
                            # print(target_indexed_csv_df)
                            # tmp_df = pd.merge(target_indexed_csv_df, metric_values_list_df, on='submission_id')
                            # print(tmp_df)
                        except:
                            print("cannot read df")
                        # merge two target dfs

                        

    # function to read metric values
    def load_mtric_values(self, problem_id):
        METRIC_VALUES_CSV_NAME = '%s%s.csv' % (self.PATH_METRIC_VALUES, problem_id)
        try:
            df = pd.read_csv(METRIC_VALUES_CSV_NAME, delimiter=",")
            return df
        except:
            return pd.DataFrame(index=[], columns=cols)

def main():
    args = sys.argv
    if len(args) > 1:
        for problem_id in args[1:]:
            ExecCreateBoxPlotCSV(problem_id)

if __name__ == "__main__":
    main() 