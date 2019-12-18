
import subprocess
import sys
from my_library import Connector
from create_io_files_for_ngweight import FilesCreater
from create_vectors_of_ngram import VectorCreater
from lexical_clustering import ExecLexicalCluster
from metrical_clustering import ExecMetricalClustering
from save_clustering import SaveClustering

def main():
    args = sys.argv
    if len(args) != 1:
        for problem_id in args[1:]:     
            FilesCreater(problem_id)
            VectorCreater(problem_id)
            ExecLexicalCluster(problem_id)
            ExecMetricalClustering(problem_id)
            SaveClustering(problem_id)
    else:
        print("arguments are needed.")

if __name__ == '__main__':
    main()
