"""
TODO:
問題ごとに階層クラスタリングをlinkage()で実行。
fcluster()でクたスター番号の索引付けを行う。
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
from my_library.Connector import Connector
from my_library import key

sys.setrecursionlimit(10000)


class ExecLexicalCluster(Connector):
    # problem_idを引数にして、クラスタリングを実行する
    def __init__(self, problem_id):
        super().__init__()

        self.PATH_VECTOR_FILES = key.PATH_VECTOR_FILES
        self.PATH_PLOT_RESULTS = key.PATH_PLOT_RESULTS
        self.NUM_LEXICAL_CLUSTERS = key.NUM_LEXICAL_CLUSTERS

        # make_directory()でも同様のディレクトリを用意するためにインスタンス変数に実行するmethod・metricを格納
        # self.metrics = ['cosine']
        # self.metrics = ['braycurtis', 'canberra', 'chebyshev', 'cityblock', 'correlation', 'cosine', 'euclidean', 'hamming', 'jaccard']
        self.metrics = ['cosine']
        self.normal_methods = ['single', 'average', 'complete', 'weighted']
        self.euclidean_methods = ['single', 'average', 'complete', 'weighted', 'centroid', 'median', 'ward']

        self.make_directories(problem_id)

        path_csv_file = self.PATH_VECTOR_FILES + problem_id + '.csv'
        df = pd.read_csv(path_csv_file, delimiter=",", )
        length_culumns = len(df.columns)
        x = df.iloc[:,1:length_culumns]

        for metric in self.metrics:
            if metric != 'euclidean':
                methods = self.normal_methods
            else:
                methods = self.euclidean_methods
            for method in methods:
                try:

                    '''
                    階層クラスタリングを行い、プロット
                    reference: https://joernhees.de/blog/2015/08/26/scipy-hierarchicalclustering-and-dendrogram-tutorial/
                    '''
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
                    # このfcluster()の返り値のリストの各要素の順番は生データの順番と同じ
                    cluster_index = fcluster(result, self.NUM_LEXICAL_CLUSTERS, criterion='maxclust')
                    
                    path_cluster_index = '%s%s/%s/%s/%s.npy' % (self.PATH_PLOT_RESULTS, problem_id, metric, method, problem_id)
                    np.save(path_cluster_index, cluster_index)
                    print(cluster_index)
                    self.make_index_csv(problem_id, metric, method, df.iloc[:,0:1], cluster_index)
                except Exception as e:
                    print(e)
                    continue



    def make_directories(self, problem_id):
        PATH_PLOT_RESULTS = "%s%s/" % ( key.PATH_PLOT_RESULTS , problem_id)
        # デンドログラムの結果を保存するディレクトリの作成

        for metric in self.metrics:
            if metric != 'euclidean':
                methods = self.normal_methods
            else:
                methods = self.euclidean_methods
            for method in methods:
                plot_file_name = '%s%s/%s/' % (self.PATH_PLOT_RESULTS, metric, method)
                if not os.path.exists(plot_file_name):
                    os.makedirs(plot_file_name)
    
    # submission_id, lexical_index, metrical_indexの列を持つcsvを各ディレクトリで作成し、更新する
    def make_index_csv(self, problem_id, metric, method, src_list, cluster_index):
        path_cluster_index_csv = '%s%s/%s/%s/%s.csv' % (self.PATH_PLOT_RESULTS, problem_id, metric, method, problem_id)
        with open(path_cluster_index_csv, mode="w", encoding='utf-8') as f_csv:
            writer = csv.writer(f_csv, lineterminator='\n')
            header = ['submmission_id', 'lexical_id', 'metrical_id']
            writer.writerow(header)
            for i in range(0, len(src_list)):
                filename_and_lexical_clustering_id = []
                filename_and_lexical_clustering_id.append(src_list['submission_id'][i])
                filename_and_lexical_clustering_id.append(cluster_index[i])
                writer.writerow(filename_and_lexical_clustering_id)





def main():
    args = sys.argv
    # 引数がなければそのまま終了
    if len(args) != 1:
        for problem_id in args[1:]:
            ExecLexicalCluster(problem_id)



if __name__ == "__main__":
    main()