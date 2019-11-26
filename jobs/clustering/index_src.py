"""
TODO:
クラスタリング結果が保存されているndarrayの結果を参照して、
各クラスタのインデックスごとにディレクトリを作成、該当srcファイルをコピーする
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
import key



class SrcIndexer():
    PATH_SRC = key.PATH_SRC
    PATH_VECTOR_FILES = key.PATH_VECTOR_FILES
    PATH_PLOT_RESULTS = key.PATH_PLOT_RESULTS
    PATH_LEXICAL_INDEXED_SRC = key.PATH_LEXICAL_INDEXED_SRC
    NUM_LEXICAL_CLUSTERS = key.NUM_LEXICAL_CLUSTERS

    # metrics = ['braycurtis', 'canberra', 'chebyshev', 'cityblock', 'correlation', 'cosine', 'euclidean', 'hamming', 'jaccard']
    metrics = ['cosine']
    normal_methods = ['single', 'average', 'complete', 'weighted']
    euclidean_methods = ['single', 'average', 'complete', 'weighted', 'centroid', 'median', 'ward']

    # 問題idを引数にして、オリジナルのソースコードをクラスタのインデックスのディレクトリごとにコピーする
    def __init__(self, problem_id):
        self.make_directory(problem_id)

        # csvを読み込んできて、ファイル名の一覧を取得する
        # それぞれの行(解答)毎にforループを回して、ndarrayのインデックス値と照合する
        path_csv = '%s%s.csv' % (self.PATH_VECTOR_FILES, problem_id)
        with open(path_csv, "r", encoding="utf-8") as csv_file:
            f = csv.reader(csv_file, delimiter=",",  lineterminator='\n')
            next(f)
            row_count = -1
            for row in f:
                row_count += 1
                src_name = row[0]
                for metric in self.metrics:
                    if metric != 'euclidean':
                        methods = self.normal_methods
                    else:
                        methods = self.euclidean_methods
                    for method in methods:
                        path_ndarray =  '%s%s/%s/%s/%s.npy' % (self.PATH_PLOT_RESULTS, problem_id, metric, method, problem_id)
                        try:
                            indexs = np.load(path_ndarray)
                        except IOError:
                            print("%s npy Does not Exist" % problem_id)
                        tmp_index = indexs[row_count]
                        self.exec_copy(problem_id, src_name, metric, method, tmp_index)


    def exec_copy(self, problem_id, src_name, metric, method, tmp_index):
        PATH_SRC_file = '%s%s' % (self.PATH_SRC, src_name)
        if os.path.exists(PATH_SRC_file):
            try:
                path_copy_src_file = '%s%s/%s/%s/%s/%s' % (self.PATH_LEXICAL_INDEXED_SRC, problem_id, metric, method, tmp_index, src_name)
                shutil.copy(PATH_SRC_file, path_copy_src_file)
            except IOError:
                print("finotfound")




    # コピー先のディレクトリが存在しなければ作成する
    def make_directory(self, problem_id):
        # metrics = ['braycurtis', 'canberra', 'chebyshev', 'cityblock', 'correlation', 'cosine', 'euclidean', 'hamming', 'jaccard']
        metrics = ['cosine']
        normal_methods = ['single', 'average', 'complete', 'weighted']
        euclidean_methods = ['single', 'average', 'complete', 'weighted', 'centroid', 'median', 'ward']
        clusters = range(1, self.NUM_LEXICAL_CLUSTERS+1)
        for cluster in clusters:
            for metric in metrics:
                if metric != 'euclidean':
                    methods = normal_methods
                else:
                    methods = euclidean_methods
                for method in methods:
                    path_cluster = '%s%s/%s/%s/%s'% (self.PATH_LEXICAL_INDEXED_SRC, problem_id, metric, method, str(cluster))
                    if not os.path.exists(path_cluster):
                        os.makedirs(path_cluster)



def main():
    args = sys.argv
    # 引数がなければそのまま終了
    if len(args) != 1:
        for problem_id in args[1:]:
            SrcIndexer(problem_id)



if __name__ == '__main__':
    main()
