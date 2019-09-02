import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
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
        target = np.loadtxt(cluster_index_csv, delimiter=",", skiprows=1, usecols=(3))

    # n_component: Dimension of the embeded space
    #PCAを用意                                                                                                                                                                           
    pca = PCA(n_components=2)
    #PCAで次元圧縮                                                                                                                                                                       
    pca.fit(data)
    #PCAの結果を元にデータを変換                                                                                                                                                         
    X_reduced = pca.transform(data)

    # t-SNEの場合
    # X_reduced = TSNE(n_components=2, random_state=0).fit_transform(data)

    #因子寄与率
    print(pca.explained_variance_ratio_)

    # print X_reduced.shape
    # (1797, 2)
    plt.scatter(X_reduced[:, 0], X_reduced[:, 1], c=target)
    plt.colorbar()
    plt.savefig('figure.png')


if __name__ == "__main__":
    args = sys.argv
    if len(args) > 1:
        for problem_id in args[1:]:
            exec_tsne(problem_id)