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


"""
csvの全データを読み込んで、返す
"""
def get_csv_contents(problem_id):
    path_file = path_result + problem_id + '.csv'
    df_header = pd.read_csv(path_file)
    return df_header



def initalize_an_csv(problem_id, metric, method):
    path_cluster = '%s%s/%s/%s/' % (PATH_METRICAL_INDEXED_SRC, problem_id, metric, method)
    file_path = path_cluster + problem_id + '.csv'
    if os.path.isfile(file_path):
        with open(file_path, 'w') as f:
            writer = csv.writer(f, lineterminator='\n')
            list = ['src_name', 'lexical_cluster', 'metrical_cluster', 'M0', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9', 'M10', 'M11', 'M12', 'M13', 'M14']
            writer.writerow(list)

# 問題ごとの集計結果を格納するcsvファイルが存在するか確認し、存在しなければ[problem_id].csvのファイルを作成する
def create_an_csv(problem_id, metric, method):
    path_cluster = '%s%s/%s/%s/' % (PATH_METRICAL_INDEXED_SRC, problem_id, metric, method)
    file_path = path_cluster + problem_id + '.csv'
    if not os.path.isfile(file_path):
        with open(file_path,"w"):pass
        return False
    else:
        return True

def add_row_to_csv(list, problem_id, metric, method):
    path_cluster = '%s%s/%s/%s/' % (PATH_METRICAL_INDEXED_SRC, problem_id, metric, method)
    file_path = path_cluster + problem_id + '.csv'
    if os.path.isfile(file_path):
        with open(file_path, 'a') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(list)


"""
提出時期を横軸、各メトリクス値を縦軸とする散布図をコンテスト中のみかそ1うでないかの2種類の散布図を作成する
"""
def create_plot_scatters(problem_id):
    global cur
    header = get_csv_contents(problem_id)

    metrics = ['cosine']
    methods = ['complete']



    for metric in metrics:
        for method in methods:
            if(not create_an_csv(problem_id, metric, method)):
                initalize_an_csv(problem_id, metric, method)
                for lexical_cluster in range(1,8):
                    for metrical_cluster in range(1,3):
                        path_cluster = '%s%s/%s/%s/%s/'% (PATH_METRICAL_INDEXED_SRC, problem_id, metric, method, str(lexical_cluster))
                        src_list = [os.path.basename(r) for r in glob.glob(path_cluster+str(metrical_cluster)+'/*')]
                        for name, row in header.iterrows():
                            sql =  "SELECT * FROM File WHERE submission_id = %s" % row['submission_id']
                            cur.execute(sql)
                            query_result = cur.fetchone()
                            if query_result['file_name'] in src_list:
                                list = [query_result['file_name'], lexical_cluster, metrical_cluster, row['M0'], row['M1'], row['M2'], row['M3'], row['M4'], row['M5'], row['M6'], row['M7'], row['M8'], row['M9'], row['M10'], row['M11'], row['M12'], row['M13'], row['M14']]
                                add_row_to_csv(list, problem_id, metric, method)
                        """
                        src_list = [os.path.basename(r) for r in glob.glob(path_cluster+'2/*')]
                        for name, row in header.iterrows():
                            sql =  "SELECT * FROM File WHERE submission_id = %s" % row['submission_id']
                            cur.execute(sql)
                            query_result = cur.fetchone()
                            if query_result['file_name'] in src_list:
                                metric_list = [query_result['file_name']]
                                tmp_metric_list = [row['M1'], row['M14']]
                                metric_list.extend(tmp_metric_list)
                                series = pd.Series(metric_list, index=df.columns)
                                df = df.append(series, ignore_index = True)
                            plt.scatter(df['M1'], df['M14'],label='metrics scatter',color='#FF002B', alpha=0.7, s=2)
                        src_list = [os.path.basename(r) for r in glob.glob(path_cluster+'3/*')]
                        for name, row in header.iterrows():
                            sql =  "SELECT * FROM File WHERE submission_id = %s" % row['submission_id']
                            cur.execute(sql)
                            query_result = cur.fetchone()
                            if query_result['file_name'] in src_list:
                                metric_list = [query_result['file_name']]
                                tmp_metric_list = [row['M1'], row['M14']]
                                metric_list.extend(tmp_metric_list)
                                series = pd.Series(metric_list, index=df.columns)
                                df = df.append(series, ignore_index = True)
                            plt.scatter(df['M1'], df['M14'],label='metrics scatter',color='#00FF2B', alpha=0.7, s=2)
                        file_path = "%s%s/%s/%s/%s/%s" % (path_scatter_plot, problem_id, metric, method, lexical_cluster ,filename_scatterplot_advanced)
                        plt.xlabel("metric1")
                        plt.ylabel("metric2")
                        plt.savefig(file_path, dpi=300)
                        plt.clf()
                        """


               

def main():
    args = sys.argv
    # 引数が0ならば実行しない
    if len(args) != 1:
        for problem_id in args[1:]:
            create_plot_scatters(problem_id)
            print('finish to create scatter plots of ' + problem_id)

if __name__ == '__main__':
    main()