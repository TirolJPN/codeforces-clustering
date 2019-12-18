import sys
from my_library import key
import csv
import pandas as pd
from itertools import chain
from scipy.cluster.hierarchy import linkage, dendrogram
import numpy as np
from scipy.cluster.hierarchy import fcluster

class ExecMetricalClustering():

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
        # self.METHODS = ['single', 'average', 'complete', 'weighted']
        self.METHODS = ['complete']
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
                    print("-------------------------%s/%s/%s--------------------------------" % (metric, method, index_lexical_cluster))
                    path_cluster_index_csv = '%s%s/%s/%s/lexicalresult_%s.csv' % (self.PATH_PLOT_RESULTS, problem_id, metric, method, problem_id) 
                    df = pd.read_csv(path_cluster_index_csv, usecols=[0,1])
                    tmp_df = df[df["lexical_id"] == index_lexical_cluster]
                    target_submission_id_list = tmp_df['submission_id'].values.tolist()
                    # 語彙的特徴で分類を行った対象のsubmission_idの一覧を取得する

                    # 探索対象のdfをこれに追加していく
                    data_frame = pd.DataFrame(index=[], columns=['submission_id', 'M0', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M9', 'M11', 'M12', 'M13', 'M14'])
                    src_list_df = []
                    PATH_METRICS_VALUES_CSV = '%s%s.csv' % (self.PATH_METRIC_VALUES, problem_id)
                    with open(PATH_METRICS_VALUES_CSV, "r", encoding="utf-8") as metrics_values_csv:
                        # fの各行はsource monitorの計測結果が一行ずつ格納されている
                        f = csv.reader(metrics_values_csv, delimiter=",", lineterminator="\n")
                        next(f)
                        for csv_row in f:
                            if int(csv_row[1]) in target_submission_id_list:
                                # 全要素が0だと類似度が計算できないので除外する
                                tmp_metric_list = [csv_row[3], csv_row[4], csv_row[5], csv_row[6], csv_row[7], csv_row[8], csv_row[9], csv_row[12], csv_row[14], csv_row[15], csv_row[16], csv_row[17]]
                                if not all(str(int(float(elem))) == '0' for elem in tmp_metric_list):
                                    if any('+' in elem for elem in tmp_metric_list):
                                        # src_list.remove(tmp_file_name)
                                        print("failed to fetch values. submission_id: %s" % csv_row[1])
                                    else:
                                        # listのextend()はNoneを返す
                                        metric_list = [csv_row[1]]
                                        metric_list.extend(tmp_metric_list)
                                        series = pd.Series(metric_list, index=data_frame.columns)
                                        data_frame = data_frame.append(series, ignore_index = True)
                                        src_list_df.append(csv_row[1])
                                else:
                                    # src_list.remove(tmp_file_name)
                                    print("failed to fetch values. submission_id: %s" % csv_row[1])
                    self.create_clustering_csv(data_frame, metric, method, index_lexical_cluster, problem_id)


    def create_clustering_csv(self, df, metric, method, index_lexical_cluster, problem_id):
        length_culumns = len(df.columns)
        x = df.iloc[:,1:length_culumns]
        if len(df) >= 2:
            result = linkage(x,
                        metric = metric,
                        method = method)
            dendrogram(
                        result,
                        truncate_mode='lastp',  # show only the last p merged clusters
                        p=20,  # show only the last p merged clusters
                        leaf_rotation=90.,
                        leaf_font_size=12.,
                        show_contracted=True,  # to get a distribution impression in truncated branches
                    )
            label = fcluster(result, self.NUM_METRICAL_CLUSTERS, criterion='maxclust')
            print(label)
            new_data_frame = pd.DataFrame(index=[], columns=['submission_id', 'lexical_id', 'metrical_id'])
            new_data_frame['submission_id'] = df['submission_id']
            new_data_frame['lexical_id'] = index_lexical_cluster
            new_data_frame['metrical_id'] = label
            print(new_data_frame)
        else:
            new_data_frame = pd.DataFrame(index=[], columns=['submission_id', 'lexical_id', 'metrical_id'])
            new_data_frame['submission_id'] = df['submission_id']
        path_cluster_index_csv = '%s%s/%s/%s/%s_%s.csv' % (self.PATH_PLOT_RESULTS, problem_id, metric, method, problem_id, index_lexical_cluster)
        new_data_frame.to_csv(path_cluster_index_csv) 

def main():
    args = sys.argv
    if len(args) > 1:
        for problem_id in args[1:]:
            ExecMetricalClustering(problem_id)

if __name__ == "__main__":
    main()