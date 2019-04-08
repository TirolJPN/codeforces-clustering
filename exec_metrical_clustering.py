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
import key



class ExecMetricalCluster():
    PATH_SRC = key.PATH_SRC
    PATH_LEXICAL_INDEXED_SRC = key.PATH_LEXICAL_INDEXED_SRC
    PATH_METRICAL_INDEXED_SRC = key.PATH_METRICAL_INDEXED_SRC
    PATH_METRIC_VALUES = key.PATH_METRIC_VALUES
    NUM_LEXICAL_CLUSTERS = key.NUM_LEXICAL_CLUSTERS
    NUM_METRICAL_CLUSTERS = key.NUM_METRICAL_CLUSTERS

    # metrics = ['braycurtis', 'canberra', 'chebyshev', 'cityblock', 'correlation', 'cosine', 'euclidean', 'hamming', 'jaccard']
    metrics = ['cosine']
    normal_methods = ['single', 'average', 'complete', 'weighted']
    euclidean_methods = ['single', 'average', 'complete', 'weighted', 'centroid', 'median', 'ward']

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
        self.make_directory(problem_id)

        clusters = range(1, self.NUM_LEXICAL_CLUSTERS+1)
        metric_clusters = range(1, self.NUM_METRICAL_CLUSTERS+1)
        # メトリックスで未分類の問題について
        for metric in self.metrics:
            if metric != 'euclidean':
                methods = self.normal_methods
            else:
                methods = self.euclidean_methods
            for method in methods:
                for num_cluster in clusters:
                    # そのディレクトリに存在するファイル名の一覧を取得する
                    # 現在のループでフォルダが存在すれば
                    path_cluster = '%s%s/%s/%s/%s/'% (self.PATH_LEXICAL_INDEXED_SRC, problem_id, metric, method, str(num_cluster))
                    if os.path.exists(path_cluster):
                        print(path_cluster)
                        path_cluster = '%s%s/%s/%s/%s/*'% (self.PATH_LEXICAL_INDEXED_SRC, problem_id, metric, method, str(num_cluster))
                        src_list = [os.path.basename(r) for r in glob.glob(path_cluster)]

                        # src_listに存在するcsvの行だけ、dfに入れる
                        path_metric_csv = '%s%s.csv' % (self.PATH_METRIC_VALUES, problem_id)

                        # 探索対象のdfをこれに追加していく
                        data_frame = pd.DataFrame(index=[], columns=['file_name', 'M0', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M9', 'M11', 'M12', 'M13', 'M14'])

                        src_list_df = []
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
                                            src_list.remove(tmp_file_name)
                                        else:
                                            # listのextend()はNoneを返す
                                            # metric_list = [tmp_file_name].extend(tmp_metric_list)
                                            metric_list = [tmp_file_name]
                                            metric_list.extend(tmp_metric_list)
                                            series = pd.Series(metric_list, index=data_frame.columns)
                                            data_frame = data_frame.append(series, ignore_index = True)
                                            src_list_df.append(tmp_file_name)
                                    else:
                                        src_list.remove(tmp_file_name)
                        # クラスタリングの結果のラベルが帰ってくる
                        # exec_clustering()と同様にコピーを実行する
                        # ex. label が[1,2,3,2,1,2], src_listが['aaaa.src', 'hoge.src'. 'fuga.src']みたいな形なので、順序が同じことを前提にコピー
                        # print(data_frame)
                        # csv上にあり，src_list上だけに存在する要素を削除する
                
                        label = self.get_fcluster_result(data_frame, metric, method, num_cluster, problem_id)
                        print('len srclistdf: %d len label: %d' % (len(src_list_df), len(label)))
                        self.exec_copy(src_list_df, label, metric, method, num_cluster, problem_id)
                        print('-----------------------------------------------------------')


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
            print(cluster_index)
            plt.title("Dedrogram")
            plt.ylabel("Threshold")
            plot_file_name = '%s%s/%s/%s/%s/cluster.png' %(self.PATH_METRICAL_INDEXED_SRC, problem_id, metric, method, str(cluster))
            plt.savefig(plot_file_name, dpi = 1000)
            plt.clf()
            
            return cluster_index
        else:
            return [1]




    def exec_copy(self, src_list, label, metric, method, num_cluster, problem_id):
        index = 0
        for src_name in src_list:
            path_src_file = '%s%s' % (self.PATH_SRC, src_name)
            if os.path.exists(path_src_file):
                try:
                    path_copy_src_file = '%s/%s/%s/%s/%s/%s/%s' % (self.PATH_METRICAL_INDEXED_SRC, problem_id, metric, method, num_cluster ,  label[index], src_name)
                    shutil.copy(path_src_file, path_copy_src_file)
                    index = index + 1
                except Exception as e:
                    print(e)
                    index = index + 1
                    continue

                            


    # コピー先のディレクトリが存在しなければ作成する
    # 最終的な結果はPATH_METRICAL_INDEXED_SRC先にコピーする
    # この処理はproblem_idごとに行う
    def make_directory(self, problem_id):
        # metrics = ['braycurtis', 'canberra', 'chebyshev', 'cityblock', 'correlation', 'cosine', 'euclidean', 'hamming', 'jaccard']
        metrics = ['cosine']
        normal_methods = ['single', 'average', 'complete', 'weighted']
        euclidean_methods = ['single', 'average', 'complete', 'weighted', 'centroid', 'median', 'ward']
        clusters = range(1, self.NUM_LEXICAL_CLUSTERS+1)
        metric_clusters = range(1, self.NUM_METRICAL_CLUSTERS+1)
        for cluster in clusters:
            for metric_cluster in metric_clusters:
                for metric in metrics:
                    if metric != 'euclidean':
                        methods = normal_methods
                    else:
                        methods = euclidean_methods
                    for method in methods:
                        path_cluster = '%s%s/%s/%s/%s/%s'% (self.PATH_METRICAL_INDEXED_SRC, problem_id, metric, method, str(cluster), str(metric_cluster))
                        if not os.path.exists(path_cluster):
                            os.makedirs(path_cluster)



def main():
    args = sys.argv
    # 引数が0ならば実行しない
    if len(args) != 1:
        for problem_id in args[1:]:
            ExecMetricalCluster(problem_id)

if __name__ == '__main__':
    main() 