from bhtsne import tsne
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt
import numpy as np

iris = load_iris()
Y = tsne(iris.data)
plt.scatter(Y[:, 0], Y[:, 1], c=iris.target)
# plt.show()
plt.savefig('figure.png')   