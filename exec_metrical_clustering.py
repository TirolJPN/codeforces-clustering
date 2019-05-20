"""
各ディレクトリ毎にスクリプトを実行、copyを行う
やること
各ディレクトリ：ある問題のあるmetricのあるmethodでクラスタリングされた1つのクラスター。
              分類された問題の一覧がある

それぞれのディレクトリに対して以下の処理を行う
1. ファイル名をリストにする
2. miningscripts/CodeForceCrawler/resultから、SourceMonitorのメトリクス値を読みこんでくる
3. pandaのライブラリに読み込んでくる
4. クラスタリングを実行。fclusterでクラスターのラベリング。
5. 再コピー。

4, 5はリファクタリングの時点で一緒にする(？)
各出力のディレクトリの流れを確認する。
"""
import os
import mysql.connector as cn
from pyquery import PyQuery as pq
from enum import  Enum
import re
import subprocess
import sys
import csv
import pandas as pd
import copy
import matplotlib.pyplot as plt
import sys
from pandas.plotting import scatter_matrix
from scipy.cluster.hierarchy import linkage, dendrogram
import numpy as np
from scipy.cluster.hierarchy import fcluster
import shutil
import glob
from my_library import key



class ExecMetricalCluster():

    def __init__(self, problem_id):
        """
        それぞれのディレクトリに対して以下の処理を行う
        1. ファイル名をリストにする
        2. miningscripts/CodeForceCrawler/resultから、SourceMonitorのメトリクス値を読みこんでくる
        3. pandaのライブラリに読み込んでくる
        4. クラスタリングを実行。fclusterでクラスターのラベリング。
        5. 再コピー。
        """


        super().__init__()

        self.PATH_SRC = key.PATH_SRC
        self.PATH_LEXICAL_INDEXED_SRC = key.PATH_LEXICAL_INDEXED_SRC
        self.PATH_METRICAL_INDEXED_SRC = key.PATH_METRICAL_INDEXED_SRC
        self.PATH_METRIC_VALUES = key.PATH_METRIC_VALUES
        self.PATH_PLOT_RESULTS = key.PATH_PLOT_RESULTS
        self.NUM_LEXICAL_CLUSTERS = key.NUM_LEXICAL_CLUSTERS
        self.NUM_METRICAL_CLUSTERS = key.NUM_METRICAL_CLUSTERS

        # metrics = ['braycurtis', 'canberra', 'chebyshev', 'cityblock', 'correlation', 'cosine', 'euclidean', 'hamming', 'jaccard']
        metrics = ['cosine']
        normal_methods = ['single', 'average', 'complete', 'weighted']
        euclidean_methods = ['single', 'average', 'complete', 'weighted', 'centroid', 'median', 'ward']

        clusters = range(1, self.NUM_LEXICAL_CLUSTERS+1)
        metric_clusters = range(1, self.NUM_METRICAL_CLUSTERS+1)
        for metric in metrics:
            if metric != 'euclidean':
                methods = normal_methods
            else:
                methods = euclidean_methods

            for method in methods:

                for lexical_cluster in clusters:

                    # path_cluster = '%s%s/%s/%s/%s/*'% (self.PATH_LEXICAL_INDEXED_SRC, problem_id, metric, method, str(lexical_cluster))
                    # src_list = [os.path.basename(r) for r in glob.glob(path_cluster)]
                    src_list, src_index = self.get_src_list(problem_id, metric, method, lexical_cluster)

                    # src_listに存在するcsvの行だけ、dfに入れる
                    path_metric_csv = '%s%s.csv' % (self.PATH_METRIC_VALUES, problem_id)

                    # 探索対象のdfをこれに追加していく
                    data_frame = pd.DataFrame(index=[], columns=['file_name', 'M0', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M9', 'M11', 'M12', 'M13', 'M14'])

                    src_list_df = []
                    success_clustering_flag = True
                    with open(path_metric_csv, "r", encoding="utf-8") as csv_file:
                        f = csv.reader(csv_file, delimiter=",",  lineterminator='\n')
                        next(f)
                        for csv_row in f:
                            tmp_file_name = '%s_%s_%s.src' % (csv_row[0], csv_row[1], csv_row[2])
                            # ディレクトリに注目している行のファイルが存在すれば
                            # print(tmp_file_name)
                            if tmp_file_name in src_list:
                                # 全要素が0だと類似度が計算できないので除外する
                                tmp_metric_list = [csv_row[3], csv_row[4], csv_row[5], csv_row[6], csv_row[7], csv_row[8], csv_row[9], csv_row[12], csv_row[14], csv_row[15], csv_row[16], csv_row[17]]
                                if not all(str(int(float(elem))) == '0' for elem in tmp_metric_list):
                                    if any('+' in elem for elem in tmp_metric_list):
                                        # src_list.remove(tmp_file_name)
                                        success_clustering_flag = False
                                    else:
                                        # listのextend()はNoneを返す
                                        # metric_list = [tmp_file_name].extend(tmp_metric_list)
                                        metric_list = [tmp_file_name]
                                        metric_list.extend(tmp_metric_list)
                                        series = pd.Series(metric_list, index=data_frame.columns)
                                        data_frame = data_frame.append(series, ignore_index = True)
                                        src_list_df.append(tmp_file_name)
                                else:
                                    # src_list.remove(tmp_file_name)
                                    success_clustering_flag = False

                    # クラスタリングの結果のラベルが帰ってくる
                    # exec_clustering()と同様にコピーを実行する
                    # ex. label が[1,2,3,2,1,2], src_listが['aaaa.src', 'hoge.src'. 'fuga.src']みたいな形なので、順序が同じことを前提にコピー
                    # print(data_frame)
                    # csv上にあり，src_list上だけに存在する要素を削除する
                    if(success_clustering_flag):
                        label = self.get_fcluster_result(data_frame, metric, method, lexical_cluster, problem_id)
                        print('len srclistdf: %d len label: %d' % (len(src_list_df), len(label)))
                        self.update_clustering_csv(src_list, label, metric, method, lexical_cluster, problem_id, src_index)
                        # self.exec_copy(src_list_df, label, metric, method, lexical_cluster, problem_id)
                        print('-----------------------------------------------------------')
                    else:
                        self.update_clustering_csv(src_list, [-1]*len(src_list), metric, method, lexical_cluster, problem_id, src_index)


    def get_fcluster_result(self, df, metric, method, cluster, problem_id):
        length_culumns = len(df.columns)
        x = df.iloc[:,1:length_culumns]
        print(x)
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
            cluster_index = fcluster(result, self.NUM_METRICAL_CLUSTERS, criterion='maxclust')
            
            return cluster_index
        else:
            return [1]
    

    def update_clustering_csv(self, src_list, label, metric, method, lexical_cluster, problem_id, src_index):
        path_cluster_index_csv = '%s%s/%s/%s/%s.csv' % (self.PATH_PLOT_RESULTS, problem_id, metric, method, problem_id)
        df = pd.read_csv(path_cluster_index_csv)
        index = 0
        for src_name in src_list:
            df.at[src_name, 'metrical_id'] = label[index]
        # df.to_csv(path_cluster_index_csv, columns=['metrical_id'])
        print(label)




    # 引数のlexical_clusterに対応するファイル名の一覧を返す
    def get_src_list(self, problem_id, metric, method, lexical_cluster):
        path_cluster_index_csv = '%s%s/%s/%s/%s.csv' % (self.PATH_PLOT_RESULTS, problem_id, metric, method, problem_id)
        with open(path_cluster_index_csv, mode="r", encoding='utf-8') as f_csv:
            reader = csv.reader(f_csv)
            header = next(reader)
            file_list = []
            file_index = []
            row_index = 0 
            for row in reader:
                if (row[1] == lexical_cluster):
                    file_list.append(row[1])
                    file_index.append(row_index)
                    row_index += 1
        return file_list, file_index



def main():
    args = sys.argv
    # 引数が0ならば実行しない
    if len(args) != 1:
        for problem_id in args[1:]:
            ExecMetricalCluster(problem_id)

if __name__ == '__main__':
    main() 