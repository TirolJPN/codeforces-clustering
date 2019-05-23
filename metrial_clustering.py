import sys
from my_library import key
import csv
import pandas as pd
from itertools import chain

class ExecNetricalClustering():

    def __init__(self, problem_id):
        # 各定数の初期化
        self.PATH_SRC = key.PATH_SRC
        self.PATH_LEXICAL_INDEXED_SRC = key.PATH_LEXICAL_INDEXED_SRC
        self.PATH_METRICAL_INDEXED_SRC = key.PATH_METRICAL_INDEXED_SRC
        self.PATH_METRIC_VALUES = key.PATH_METRIC_VALUES
        self.PATH_PLOT_RESULTS = key.PATH_PLOT_RESULTS
        self.NUM_LEXICAL_CLUSTERS = key.NUM_LEXICAL_CLUSTERS
        self.NUM_METRICAL_CLUSTERS = key.NUM_METRICAL_CLUSTERS

        self.METRICS = ['cosine']
        self.METHODS = ['single', 'average', 'complete', 'weighted']
        self.RANGE_LEXICAL_CLUSTER = range(1, self.NUM_LEXICAL_CLUSTERS + 1)
        self.RANGE_METRICAL_CLUSTER = range(1, self.NUM_METRICAL_CLUSTERS + 1)

        for metric in self.METRICS:
            for method in self.METHODS:
                for index_lexical_cluster in self.RANGE_LEXICAL_CLUSTER:
                    """
                    * lexical_clusteringの実行結果csvから各インデックスのファイル名だけ取得
                    * source metricsの計測結果があるか確かめ，なければ除外する
                    * この時点で，値がそろっているものだけでDFの作成
                    * fclusterの実行
                    * lexical, metricalの両者の結果を格納するcsvに追記する
                    """
                    path_cluster_index_csv = '%s%s/%s/%s/%s.csv' % (self.PATH_PLOT_RESULTS, problem_id, metric, method, problem_id) 
                    df = pd.read_csv(path_cluster_index_csv, usecols=[0])
                    target_src_list = list(chain.from_iterable(df.values.tolist()))

                    # 語彙的特徴で分類を行った対象のsubmission_idの一覧を取得する
                    target_submission_ids = list(map(lambda src_name: src_name.split('_')[-2], target_src_list))
                    print(target_submission_ids)


                        
                    PATH_METRICS_VALUES_CSV = '%s%s.csv' % (self.PATH_METRIC_VALUES, problem_id)
                    with open(PATH_METRICS_VALUES_CSV, "r", encoding="utf-8") as metrics_values_csv:
                        # fの各行はsource monitorの計測結果が一行ずつ格納されている
                        f = csv.reader(metrics_values_csv, delimiter=",", lineterminator="\n")
                        for t in f:
                            print(t[1] in target_submission_ids)
     

def main():
    args = sys.argv
    if len(args) > 1:
        for problem_id in args[1:]:
            ExecNetricalClustering(problem_id)

if __name__ == "__main__":
    main()