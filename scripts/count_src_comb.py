"""
TODO
提出日時を横軸、各メトリクス値を縦軸に取る散布図の作成を行う
(実行時間のやつはべつふぁいるでおこなう)
"""

import os
import mysql.connector as cn
from pyquery import PyQuery as pq
import glob
import shutil
import xml.etree.ElementTree as ET
import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import key
import itertools
import sys

path_result = './../../miningscripts/CodeForcesCrawler/result/'
path_scatter_plot = './../outputs/metrical_indexed_src/'
filename_scatterplot_advanced = "scatterplot_advanced.png"
filename_scatterplot_beginner = "scatterplot_beginner.png"


cnx = cn.connect(
        host='127.0.0.1',
        user='kosuke',
        password='localhost',
        port='3306',
        database='codeforces')
cur = cnx.cursor(buffered=True, dictionary=True)


PATH_SRC = key.PATH_SRC
PATH_LEXICAL_INDEXED_SRC = key.PATH_LEXICAL_INDEXED_SRC
PATH_METRICAL_INDEXED_SRC = key.PATH_METRICAL_INDEXED_SRC
PATH_METRIC_VALUES = key.PATH_METRIC_VALUES
NUM_LEXICAL_CLUSTERS = key.NUM_LEXICAL_CLUSTERS
NUM_METRICAL_CLUSTERS = key.NUM_METRICAL_CLUSTERS



def get_src_list(problem_id, metric, method):
    src_path_base = '%s%s/%s/%s/' % (PATH_LEXICAL_INDEXED_SRC, problem_id, metric, method)
    src_list = []
    for index_cluster in range(1, NUM_LEXICAL_CLUSTERS+1):
        src_path = '%s%s/*' %  (src_path_base, str(index_cluster))
        # print(src_path)
        tmp_src_list = [os.path.basename(r) for r in glob.glob(src_path)]
        src_list.extend(tmp_src_list)
    return src_list


def search_cluster_comb(problem_id, metric, method, src_a, src_b, src_path_base):
    found_src_a = False
    found_src_b = False
    for index_lexical_cluster in range(1, NUM_LEXICAL_CLUSTERS+1):
        for index_metrical_cluster in range(1, NUM_METRICAL_CLUSTERS+1):
            src_path = '%s%s/%s/%s' % (src_path_base, index_lexical_cluster, index_metrical_cluster, src_a)
            if os.path.isfile(src_path):
                found_src_a = True
                cluster_src_a = '%d-%d' % (index_lexical_cluster, index_metrical_cluster)
            
            src_path = '%s%s/%s/%s' % (src_path_base, index_lexical_cluster, index_metrical_cluster, src_b)
            if os.path.isfile(src_path):
                found_src_b = True
                cluster_src_b = '%d-%d' % (index_lexical_cluster, index_metrical_cluster)

            if (found_src_a and found_src_b):
                break
    
    if not (found_src_a and found_src_b):
        cluster_src_a = 'null'
        cluster_src_b = 'null'
    
    # print ('found! at %s and %s' % (cluster_src_a, cluster_src_b))
    return [cluster_src_a, cluster_src_b]
                



def count_src_comb(problem_id):
    global cur

    metric = 'cosine'
    method = 'complete'

    # srcの一覧を取得する
    src_list = get_src_list(problem_id, metric, method)
    # print(src_list)

    src_comb_list = list(itertools.combinations(src_list, 2))

    result = []

    """
    tt:my_methodでもtambaでも同じクラスタとして見つかった
    tf:my_methodでは同じクラスタ内で見つかったが，tambaでは違うクラスタとして見つかった
    (ry)
    """
    tt = 0
    tf = 0
    ft = 0
    ff = 0
    not_found = 0

    count = 0
    for src_a, src_b in src_comb_list:
        # print('Start to search file of %s and %s' % (src_a, src_b))

        src_path_base = '%s%s/%s/%s/' % (PATH_METRICAL_INDEXED_SRC, problem_id, metric, method)
        comb_my_method = search_cluster_comb(problem_id, metric, method, src_a, src_b, src_path_base)

        src_path_base = './../../code_clustering_pre/outputs/metrical_indexed_src/%s/%s/%s/' % (problem_id, metric, method)
        comb_tamba = search_cluster_comb(problem_id, metric, method, src_a, src_b, src_path_base)

        if((comb_my_method is not None) and (comb_tamba is not None)):
            tmp_list = comb_tamba
            tmp_list.extend(comb_my_method)

            if any(x == 'null' for x in tmp_list):
                not_found += 1
                continue
            
            if(comb_my_method[0] == comb_my_method[1] and comb_tamba[0] == comb_tamba[1]):
                tt += 1
            elif(comb_my_method[0] == comb_my_method[1] and not(comb_tamba[0] == comb_tamba[1])):
                tf += 1
            elif(not(comb_my_method[0] == comb_my_method[1]) and comb_tamba[0] == comb_tamba[1]):
                ft += 1
            elif(not(comb_my_method[0] == comb_my_method[1]) and not(comb_tamba[0] == comb_tamba[1])):
                ff += 1
            count += 1
            print(count)
            result.append([[src_a, src_b], comb_my_method, comb_tamba])
    
    print('Finish to search all combinations!')

    with open("./count_result.txt", "w") as f:
        print(result, file=f)
    

    # for row in result:
    #     tmp_list = row[1].extend(row[2])
    #     if any(x == 'null' for x in tmp_list):
    #         not_found += 1
    #         continue
    #     if(row[1][0] == row[1][1] and row[2][0] == row[2][1]):
    #         tt += 1
    #     if(row[1][0] == row[1][1] and not(row[2][0] == row[2][1])):
    #         tf += 1
    #     if(not(row[1][0] == row[1][1]) and row[2][0] == row[2][1]):
    #         ft += 1
    #     if(not(row[1][0] == row[1][1]) and not(row[2][0] == row[2][1])):
    #         ff += 1
        
        

    print('OO:%d' % tt)
    print('OX:%d' % tf)
    print('XO:%d' % ft)
    print('XX:%d' % ff)
    print('not found:%d' % not_found)
    print('-------------------------------------------------------------------')


             

def main():
    args = sys.argv
    # 引数が0ならば実行しない
    if len(args) != 1:
        for problem_id in args[1:]:
            count_src_comb(problem_id)
            print('-------------------------------------------------------------------')

if __name__ == '__main__':
    main()