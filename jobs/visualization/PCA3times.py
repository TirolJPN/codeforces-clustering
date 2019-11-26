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
    # setting for print np
    np.set_printoptions(threshold=np.inf)
    metric = "cosine"
    method = "complete" 

    path_cluster_index_csv = '%s%s/%s/%s/%s_boxplot.csv' % (key.PATH_PLOT_RESULTS, problem_id, metric, method, problem_id) 

    with open(path_cluster_index_csv, "r", encoding="utf-8") as cluster_index_csv:
        data_original = np.loadtxt(cluster_index_csv, delimiter=",", skiprows=1, usecols=(7, 8, 9, 10, 11, 12, 13, 16, 18, 19, 20, 21))
    with open(path_cluster_index_csv, "r", encoding="utf-8") as cluster_index_csv:
        target_original = np.loadtxt(cluster_index_csv, delimiter=",", skiprows=1, usecols=(3))

    # n_component: Dimension of the embeded space
    #PCAを用意                                                                                                                                                                           
    pca = PCA(n_components=2)
    #PCAで次元圧縮                                                                                                                                                                       
    pca.fit(data_original)
    #PCAの結果を元にデータを変換                                                                                                                                                         
    X_reduced_original = pca.transform(data_original)
    cmap = ['#550055', '#800099','#000099', '#008099', '#58FAF4', '#009900', '#999900', '#FF8000', '#990000']
    label = ["A-1", "A-2", "A-3", "B-1", "B-2", "B-3", "C-1", "C-2", "C-3", ]

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    for i in range(1, 10):
        X_reduced = np.insert(X_reduced_original, 2, target_original, axis=1)
        X = X_reduced[np.where(X_reduced[:, -1] == i)]
        ax.scatter(X[:, 0], X[:, 1] , c=cmap[i-1], s=15, alpha=1.0,label=label[i-1])
  
    ax.set_xlabel('First principal component')
    ax.set_ylabel('Second principal component')


    ax.legend(loc='upper right')
    fig.savefig( problem_id + '_result.png' )


    maxs = np.amax(X_reduced_original, axis=0)
    print(maxs)

    mins = np.amin(X_reduced_original, axis=0)
    print(mins)
    plt.clf()



    # digits = datasets.load_digits()
    for index in range(1, 4):

        # setting for print np
        np.set_printoptions(threshold=np.inf)
        metric = "cosine"
        method = "complete" 

        path_cluster_index_csv = '%s%s/%s/%s/%s_boxplot_%s.csv' % (key.PATH_PLOT_RESULTS, problem_id, metric, method, problem_id, str(index)) 

        with open(path_cluster_index_csv, "r", encoding="utf-8") as cluster_index_csv:
            data = np.loadtxt(cluster_index_csv, delimiter=",", skiprows=1, usecols=(7, 8, 9, 10, 11, 12, 13, 16, 18, 19, 20, 21))
        with open(path_cluster_index_csv, "r", encoding="utf-8") as cluster_index_csv:
            target = np.loadtxt(cluster_index_csv, delimiter=",", skiprows=1, usecols=(3))

        
        X_reduced = np.insert(X_reduced_original, 2, target_original, axis=1)
        X = X_reduced[np.where((X_reduced[:, -1] == (1 + (index - 1) * 3)) | (X_reduced[:, -1] == (2 + (index - 1) * 3)) | (X_reduced[:, -1] == (3 + (index - 1) * 3)))]
        # print X_reduced.shape
        # (1797, 2)
        # lcmap = colors.ListedColormap(['#FF99FF', '#8000FF','#0000FF', '#0080FF', '#58FAF4', '#00FF00', '#FFFF00', '#FF8000', '#FF0000'])
        cmap = ['#800099','#58FAF4',  '#FF8000']

        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        for i in range(1 , 4):
            X_reduced = np.insert(X_reduced_original, 2, target_original, axis=1)
            X = X_reduced[np.where(X_reduced[:, -1] == (index - 1) * 3 + i)]
            ax.scatter(X[:, 0], X[:, 1] , c=cmap[i-1], alpha=1.0, label=label[(index - 1) * 3 + i - 1])

        ax.axis(xmin=mins[0]-5,xmax=maxs[0]+5, ymin=mins[1]-5, ymax=maxs[1]+5)
        ax.set_xlabel('First principal component')
        ax.set_ylabel('Second principal component')

        ax.legend(loc='upper right')

        # plt.scatter(X_reduced[:, 0], X_reduced[:, 1], c=target, alpha=0.7)
        plt.savefig( problem_id + '_result_' + str(index) +'.png' )
        plt.clf()




if __name__ == "__main__":
    args = sys.argv
    if len(args) > 1:
        for problem_id in args[1:]:
            exec_tsne(problem_id)