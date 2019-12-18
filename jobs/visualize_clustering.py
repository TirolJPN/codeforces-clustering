from my_library import key
import os
import sys
import csv
from my_library import Connector
import shutil


# インデックス付けしたcsvを参照してフォルダ分けする
class visualizeClustering(Connector.Connector):
    def __init__(self, problem_id):
        super().__init__()

        FETCHED_CLUSTERING_ID = self.insert_into_qlustering(problem_id)
        if not FETCHED_CLUSTERING_ID:
            print("Failed to insert Clustering row")
            return
        self.PATH_PLOT_RESULTS = key.PATH_PLOT_RESULTS
        self.NUM_LEXICAL_CLUSTERS = key.NUM_LEXICAL_CLUSTERS
        self.NUM_METRICAL_CLUSTERS = key.NUM_METRICAL_CLUSTERS
        self.PATH_SRC = key.PATH_SRC
        self.METRICS = ['cosine']
        # self.METHODS = ['single', 'average', 'complete', 'weighted']
        self.METHODS = ['complete']
        self.RANGE_LEXICAL_CLUSTERS = range(1, self.NUM_LEXICAL_CLUSTERS + 1)
        self.RANGE_METRICAL_CLUSTERS = range(1, self.NUM_METRICAL_CLUSTERS + 1)
        # 全メソッド・メトリクス・インデックス番号でコピーを実行する
        for metric in self.METRICS:
            for method in self.METHODS:
                PATH_COPY_DIRECTORY = '%s%s/%s/%s/result/' % (self.PATH_PLOT_RESULTS, problem_id, metric, method)
                if not os.path.isdir(PATH_COPY_DIRECTORY):
                    os.mkdir(PATH_COPY_DIRECTORY)
                for index_lexical_cluster in self.RANGE_LEXICAL_CLUSTERS:
                    # 初期化としてディレクトリを作成する
                    self.make_directory(problem_id, metric, method, index_lexical_cluster)

                # 該当csvを開き，submissiocn_idの一覧を取得する
                    src_list = self.get_src_list(problem_id, metric, method, index_lexical_cluster)
                    # print('metric:%s / method:%s / lexical_index:%d' % (metric, method, index_lexical_cluster))
                    # print(src_list)

                    # src_original/(srcがすべてあるディレクトリ)で検索する
                    for src in src_list:
                        submission_id = src[0]
                        metrical_index = src[1]
                        # ファイルが存在すれば，作成したディレクトリにコピーする
                        SQL_STATEMENT = "SELECT * FROM File WHERE submission_id = %s" % submission_id
                        SQL_RESULT = super().exec_select_sql(SQL_STATEMENT)
                        FILE_NAME = SQL_RESULT[0]["file_name"]
                        SEARCH_PATH = "%s%s" % (self.PATH_SRC, FILE_NAME)
                        if os.path.exists(SEARCH_PATH):
                            # PATH_TO = '%s%s/%s/%s/result/%s/%s/%s' % (self.PATH_PLOT_RESULTS, problem_id, metric, method, index_lexical_cluster, metrical_index, FILE_NAME)
                            # shutil.copyfile(SEARCH_PATH, PATH_TO)
                            # print('Finish to copy %s' % PATH_TO)
                            self.insert_into_qlustering_index(FETCHED_CLUSTERING_ID, submission_id, index_lexical_cluster, metrical_index)
                            print("Successed to insert sql of %s" % FILE_NAME)
                        else:
                            # print('Failed to copy %s' % FILE_NAME)
                            print("Failed to insert sql of %s" % FILE_NAME)

    # Pri Keyのidを返り値とする
    def insert_into_qlustering(self, problem_id):
        SQL_STATAMENT = "INSERT INTO Clustering (problem_id) VALUES (\"%s\")" % (problem_id)
        print(SQL_STATAMENT)
        super().exec_insert_sql(SQL_STATAMENT)
        SQL_STATAMENT = "SELECT MAX(id) as id FROM Clustering WHERE problem_id = \"%s\"" % (problem_id)
        SQL_RESULT = super().exec_select_sql(SQL_STATAMENT)
        fetched_id = SQL_RESULT[0]["id"]
        if fetched_id != None:
            return fetched_id
        else:
            return False
    

    def insert_into_qlustering_index(self, clustering_id, problem_id, lexical_index, metrical_index):
        SQL_STATEMENT = "INSERT INTO ClusteringIndex (clustering_id, submission_id, lexical_id, metrical_id) VALUES (%s, %s, %s, %s)" % \
            (clustering_id, problem_id, lexical_index, metrical_index)
        print(SQL_STATEMENT)
        super().exec_insert_sql(SQL_STATEMENT)


    def make_directory(self, problem_id, metric, method, index_lexical_cluster):
        PATH_COPY_DIRECTORY = '%s%s/%s/%s/result/%s/' % (self.PATH_PLOT_RESULTS, problem_id, metric, method, index_lexical_cluster)
        if not os.path.isdir(PATH_COPY_DIRECTORY):
            os.mkdir(PATH_COPY_DIRECTORY)
        for index_metrical_cluster in self.RANGE_METRICAL_CLUSTERS:
            PATH_COPY_DIRECTORY = '%s%s/%s/%s/result/%s/%s/' % (self.PATH_PLOT_RESULTS, problem_id, metric, method, index_lexical_cluster, index_metrical_cluster)
            if not os.path.isdir(PATH_COPY_DIRECTORY):
                os.mkdir(PATH_COPY_DIRECTORY)


    # 与えられた引数から該当するsubmission_idとmetrical_indexの一覧を取得する
    def get_src_list(self, problem_id, metric, method, index_lexical_cluster):
        PATH_CSV = '%s%s/%s/%s/%s_%s.csv' % (self.PATH_PLOT_RESULTS, problem_id, metric, method, problem_id, index_lexical_cluster)
        try:
            with open(PATH_CSV, "r", encoding="utf-8") as csv_reader:
                f = csv.reader(csv_reader, delimiter=',', lineterminator="\n")
                next(f)
                src_list = []
                for row in f:
                    src_list.append([row[1], row[3]])
            return src_list

        except Exception as e:
            return []


def main():
    args = sys.argv
    if len(args) > 0:
        for problem_id in args[1:]:
            visualizeClustering(problem_id)


if __name__ == "__main__":
    main()
