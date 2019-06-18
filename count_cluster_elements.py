# coding: utf-8
import sys
import os
from my_library import  key


def count_cluster_elements(problem_id):
    
    PATH_PLOT_RESULTS = key.PATH_PLOT_RESULTS
    NUM_LEXICAL_CLUSTERS = key.NUM_LEXICAL_CLUSTERS
    NUM_METRICAL_CLUSTERS = key.NUM_METRICAL_CLUSTERS
    PATH_SRC = key.PATH_SRC
    METRICS = ['cosine']
    METHODS = ['single', 'average', 'complete', 'weighted']
    RANGE_LEXICAL_CLUSTERS = range(1, NUM_LEXICAL_CLUSTERS + 1)
    RANGE_METRICAL_CLUSTERS = range(1, NUM_METRICAL_CLUSTERS + 1)
    
    for metric in METRICS:
        for method in METHODS:
            LOG_FILE_NAME = '%s%s/%s/%s/count.txt' % (PATH_PLOT_RESULTS, problem_id, metric, method)
            with open(LOG_FILE_NAME, mode="w") as f:
                for index_lexical_cluster in RANGE_LEXICAL_CLUSTERS:
                    tmp_list = []
                    for index_mtrical_cluster in RANGE_METRICAL_CLUSTERS:
                        tmp_path = '%s%s/%s/%s/result/%d/%d/' % (PATH_PLOT_RESULTS, problem_id, metric, method, index_lexical_cluster, index_mtrical_cluster)
                        tmp_num =  len([name for name in os.listdir(tmp_path) if os.path.isfile(os.path.join(tmp_path, name))])
                        tmp_list.append(str(tmp_num))
                    f.write(' '.join(tmp_list))
                    f.write('\n')
                    print(tmp_list)

def main():
    args = sys.argv
    if len(args) > 0:
        for problem_id in args[1:]:
            count_cluster_elements(problem_id)

if __name__ == "__main__":
    main()
