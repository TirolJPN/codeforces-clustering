import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from matplotlib import colors
from my_library import key
import sys
import csv



def exec_tsne(problem_id):
    """
    TODO:
    digitsと同様にベクトル部分のdataとラベルを表すtargetを問題ごとに用意して，TSNEに投げる
    """
    # digits = datasets.load_digits()

    # setting for print np
    np.set_printoptions(threshold=np.inf)
    metric = "cosine"
    method = "complete" 

    path_cluster_index_csv = '%s%s/%s/%s/%s_boxplot.csv' % (key.PATH_PLOT_RESULTS, problem_id, metric, method, problem_id) 

    with open(path_cluster_index_csv, "r", encoding="utf-8") as cluster_index_csv:
        data = np.loadtxt(cluster_index_csv, delimiter=",", skiprows=1, usecols=(7, 8, 9, 10, 11, 12, 13, 16, 18, 19, 20, 21))
    with open(path_cluster_index_csv, "r", encoding="utf-8") as cluster_index_csv:
        target_original = np.loadtxt(cluster_index_csv, delimiter=",", skiprows=1, usecols=(3))

    # n_component: Dimension of the embeded space
    #PCAを用意                                                                                                                                                                           
    pca = PCA(n_components=2)
    #PCAで次元圧縮                                                                                                                                                                       
    pca.fit(data)
    #PCAの結果を元にデータを変換                                                                                                                                                         
    X_reduced_original = pca.transform(data)

    # t-SNEの場合
    # X_reduced_originals = TSNE(n_components=2, random_state=0).fit_transform(data)

    #因子寄与率
    print(pca.explained_variance_ratio_)
    
    file_name = problem_id + '_log.txt'
    np.savetxt( file_name, pca.explained_variance_ratio_ )

    # print X_reduced.shape
    # (1797, 2)
    cmap = ['#550055', '#800099','#000099', '#008099', '#5AFAF4', '#009900', '#999900', '#FF8000', '#990000']
    label = ["A-1", "A-2", "A-3", "B-1", "B-2", "B-3", "C-1", "C-2", "C-3", ]
    for i in range(1, 10):
        X_reduced = np.insert(X_reduced_original, 2, target_original, axis=1)
        X = X_reduced[np.where(X_reduced[:, -1] == i)]
        plt.scatter(X[:, 0], X[:, 1] , cmap=cmap[i-1], s=15, alpha=1.0,label=label[i-1])

    # plt.scatter(X_reduced[:, 0], X_reduced[:, 1], c=target_original, alpha=0.7)
    plt.legend(loc='upper right')
    plt.savefig( problem_id + '_result.png' )


if __name__ == "__main__":
    args = sys.argv
    if len(args) > 1:
        for problem_id in args[1:]:
            exec_tsne(problem_id)