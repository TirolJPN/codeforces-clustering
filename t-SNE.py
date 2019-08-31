import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets
from sklearn.manifold import TSNE

digits = datasets.load_digits()

np.set_printoptions(threshold=np.inf)

print(digits.data.shape)
# (1797, 64)
print (digits.target.shape)
# (1797,)
print(digits.data)
print(type(digits.data))
print(digits.target)
print(type(digits.target))
exit()

# n_component: Dimension of the embeded space
X_reduced = TSNE(n_components=2, random_state=0).fit_transform(digits.data)

# print X_reduced.shape
# (1797, 2)

plt.scatter(X_reduced[:, 0], X_reduced[:, 1], c=digits.target)
plt.colorbar()
plt.savefig('figure.png')
# <matplotlib.colorbar.Colorbar at 0x7ff21173ee90>