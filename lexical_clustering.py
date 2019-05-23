import sys
import os
from my_library import key
import csv
import pandas as pd
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.cluster.hierarchy import fcluster


class ExecLexicalCluster():
    def __init__(self, problem_id):
        self.PATH_VECTOR_FILES = key.PATH_VECTOR_FILES
        self.PATH_PLOT_RESULTS = key.PATH_PLOT_RESULTS
        self.NUM_LEXICAL_CLUSTERS = key.NUM_LEXICAL_CLUSTERS
        self.PATH_METRIC_VALUES = key.PATH_METRIC_VALUES 
        self.METRICS = ['cosine']
        self.METHODS = ['single', 'average', 'complete', 'weighted']

        self.make_directories(problem_id)

        
        path_csv_file = self.PATH_VECTOR_FILES + problem_id + '.csv'
        df = pd.read_csv(path_csv_file, delimiter=",", )
        length_culumns = len(df.columns)
        x = df.iloc[:,1:length_culumns]

        # ここでdfのフィルタリングが必要
        # メトリクス値がcsv内になければクラスタリング対象外にする
        PATH_METRIC_VALUES_CSV = "%s%s.csv" % (self.PATH_METRIC_VALUES, problem_id)
        submission_id_list = []
        with open(PATH_METRIC_VALUES_CSV, "r", encoding="utf-8") as metric_values_csv:
            f = csv.reader(metric_values_csv, delimiter=",", lineterminator="\n")
            h = next(f)
            for row in f:
                # submission_idはrow[1]で取得できる
                submission_id_list.append(row[1])

        print(df["submission_id"])


        for metric in self.METRICS:
            for method in self.METHODS:
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
                    cluster_index = fcluster(result, self.NUM_LEXICAL_CLUSTERS, criterion='maxclust')
                    
                    # path_cluster_index = '%s%s/%s/%s/%s.npy' % (self.PATH_PLOT_RESULTS, problem_id, metric, method, problem_id)
                    # np.save(path_cluster_index, cluster_index)
                    # print(cluster_index)
                    # self.make_index_csv(problem_id, metric, method, df.iloc[:,0:1], cluster_index)
                except Exception as e:
                    print(e)
                    continue


    def make_directories(self, problem_id):
        for metric in self.METRICS:
            for method in self.METHODS:
                result_path = '%s%s/%s/%s' % (self.PATH_PLOT_RESULTS, problem_id, metric, method)
                if not os.path.exists(result_path):
                    os.makedirs(result_path)

    def make_index_csv(self, problem_id, metric, method, src_list, cluster_index):
        return True


def main():
    args = sys.argv
    if len(args) > 0:
        for problem_id in args[1:]:
            ExecLexicalCluster(problem_id)

if __name__ == "__main__":
    main()