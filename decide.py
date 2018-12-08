import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn import tree

raw = pd.read_csv('winequality-red.csv',sep=';')
df = pd.DataFrame(raw)

xList = df[
    ['fixed acidity',
    'volatile acidity',
    'citric acid',
    'residual sugar',
    'chlorides',
    'free sulfur dioxide',
    'total sulfur dioxide',
    'density',
    'pH',
    'sulphates',
    'alcohol']
]
labels = df[['quality']]

xList = np.array(xList,dtype=float)
labels = np.array(labels,dtype=float)

wineTree = DecisionTreeRegressor(max_depth=10)
wineTree.fit(xList,labels)

winePredict = wineTree.predict(xList)
error = np.zeros(labels.shape[0])
for i in range(labels.shape[0]):
    error[i] = labels[i] - winePredict[i]
print(np.sum(error*error)/labels.shape[0])

with open('wineTree.dot','w') as f:
    f = tree.export_graphviz(wineTree,out_file=f)
