# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

# from sklearn import metrics
# train = pd.read_csv('Train.csv')

# test = pd.read_csv('Test.csv') 


predictY = pd.DataFrame(np.random.uniform(0,1,10000).reshape(10000,1))
predictY.to_csv('Results_1.csv', encoding = 'utf-8', index=False , header=False) 

# print(predictY.shape) 
# Y = pd.read_csv("TestY.csv",header= None)
# print(Y.shape)
# y = Y[0]
# pred = predictY[0]

# print(y.shape, pred.shape)
# print(y)
# fpr, tpr, thresholds = metrics.roc_curve(y, pred, pos_label=1)
# y= pd.read_csv("TestY.csv")


# print(metrics.auc(fpr, tpr))




# from sklearn import tree
# X = [[0, 0], [1, 1]]
# Y = [0, 1]
# clf = tree.DecisionTreeClassifier()
# clf = clf.fit(X, Y)
 
# print(clf.predict([[2., 2.]]))
# print(clf.predict_proba([[1., -0.2]])  )



