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

        PATH_VECTOR_FILES = key.PATH_VECTOR_FILES
        PATH_PLOT_RESULTS = key.PATH_PLOT_RESULTS
        NUM_LEXICAL_CLUSTERS = key.NUM_LEXICAL_CLUSTERS

        # make_directory()でも同様のディレクトリを用意するためにインスタンス変数に実行するmethod・metricを格納
        # self.metrics = ['cosine']
        # self.metrics = ['braycurtis', 'canberra', 'chebyshev', 'cityblock', 'correlation', 'cosine', 'euclidean', 'hamming', 'jaccard']
        self.metrics = ['cosine']
        self.normal_methods = ['single', 'average', 'complete', 'weighted']
        self.euclidean_methods = ['single', 'average', 'complete', 'weighted', 'centroid', 'median', 'ward']

        self.make_directories(problem_id)

        path_csv_file = PATH_VECTOR_FILES + problem_id + '.csv'
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
                    cluster_index = fcluster(result, NUM_LEXICAL_CLUSTERS, criterion='maxclust')
                    # plt.title("Dedrogram")
                    # plt.ylabel("Threshold")
                    # plot_file_name = '%s%s/%s/%s/%s.png' % (PATH_PLOT_RESULTS, problem_id, metric, method, problem_id)
                    # plt.savefig(plot_file_name, dpi = 1000)
                    # plt.clf()
                    
                    path_cluster_index = '%s%s/%s/%s/%s.npy' % (PATH_PLOT_RESULTS, problem_id, metric, method, problem_id)
                    np.save(path_cluster_index, cluster_index)
                    path_cluster_index_log = '%s%s/%s/%s/%s.txt' % (PATH_PLOT_RESULTS, problem_id, metric, method, problem_id)
                    print(cluster_index)
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
                plot_file_name = '%s%s/%s/' % (PATH_PLOT_RESULTS, metric, method)
                if not os.path.exists(plot_file_name):
                    os.makedirs(plot_file_name)    



def main():
    args = sys.argv
    # 引数がなければそのまま終了
    if len(args) != 1:
        for problem_id in args[1:]:
            ExecLexicalCluster(problem_id)



if __name__ == "__main__":
    main()