
# coding: utf-8

# ## P2P逾期预测建模

# In[1]:

# 导入所需库
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

get_ipython().magic('matplotlib inline')
plt.style.use("ggplot")

# 导入数据
riskdat =  pd.read_sas('riskdat.sas7bdat')
riskdat_c = riskdat.copy()

# 数据的维度: 2380个样本, 1033个自变量, 1个因变量
riskdat.shape


# In[2]:

# 查看数据
riskdat.head()


# In[3]:

# 目标变量在正负样本上的分布是不均匀的
riskdat.y.value_counts()


# In[4]:

# 每个样本的缺失变量数
riskdat.missing_var = riskdat.isnull().sum(axis=1)


# In[5]:

# 部分样本有90%以上的变量是缺失的, 直接删去这些样本
# 剩余2060个样本
riskdat = riskdat.loc[riskdat.missing_var < 100, :]
riskdat.shape


# In[6]:

riskdat.head()


# In[7]:

# 某些变量全部为0, 不能提供有效信息, 因此删除
riskdat = riskdat.loc[:, ~(riskdat == 0).all(axis=0)]
riskdat.shape


# In[8]:

# 非数值型变量
riskdat_sub2 = riskdat.select_dtypes(include=['object'])
riskdat_sub2.head(3)


# In[9]:

# 仅抽取数值型变量
riskdat_sub1 = riskdat.select_dtypes(exclude=['object'])
riskdat_sub1.head(3)


# In[10]:

# 用均值填补缺失的数值变量
riskdat_sub1 = riskdat_sub1.fillna(riskdat_sub1.mean())
riskdat_sub1.shape


# In[11]:

# 定义X与y方便建模
X1, y1 = riskdat_sub1.iloc[:, 1:-1], riskdat_sub1.y
X1.shape, y1.shape


# In[12]:

# 建模所需库
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, auc


# In[13]:

# 正负样本比例
np.mean(y1 == 0), np.mean(y1 == 1)


# In[14]:

# 训练集和测试集拆分
X1_train, X1_val, y1_train, y1_val = train_test_split(X1.values, y1.values, test_size=0.3, random_state=114)
X1_train.shape, y1_train.shape, X1_val.shape, y1_val.shape


# In[15]:

# 训练集中的正负样本比例
np.mean(y1_train == 0), np.mean(y1_train == 1)


# In[16]:

# 构建一个逻辑回归模型, 采用默认参数设置
lr_clf1 = LogisticRegression(class_weight={0: 0.03, 1: 0.97})
lr_clf1.fit(X1_train, y1_train)
y1_train_pred = lr_clf1.predict(X1_train)
print("Confusion matrix (training):\n {0}\n".format(confusion_matrix(y1_train, y1_train_pred)))
print("Classification report (training):\n {0}".format(classification_report(y1_train, y1_train_pred)))

y1_val_pred = lr_clf1.predict(X1_val)
print("Confusion matrix (validation):\n {0}\n".format(confusion_matrix(y1_val, y1_val_pred)))
print("Classification report (validation):\n {0}".format(classification_report(y1_val, y1_val_pred)))


# In[17]:

# parameter tuning
# lr_clf_tuned = LogisticRegression(class_weight={0: 0.03, 1: 0.97})
# lr_clf_params = {
#     "penalty": ["l1", "l2"],
#     "C": [1, 1.3, 1.5, 1.7, 2]
# }
# lr_clf_cv = GridSearchCV(lr_clf_tuned, lr_clf_params, cv=5)
# lr_clf_cv.fit(X1_train, y1_train)
# print(lr_clf_cv.best_params_)


# In[18]:

# 采用最优参数再次构建逻辑回归模型
lr_clf2 = LogisticRegression(penalty="l1", C=1.5, class_weight={0: 0.02, 1: 0.98})
lr_clf2.fit(X1_train, y1_train)
y1_train_pred = lr_clf2.predict(X1_train)
print("Confusion matrix (training):\n {0}\n".format(confusion_matrix(y1_train, y1_train_pred)))
print("Classification report (training):\n {0}".format(classification_report(y1_train, y1_train_pred)))

y1_val_pred = lr_clf2.predict(X1_val)
print("Confusion matrix (validation):\n {0}\n".format(confusion_matrix(y1_val, y1_val_pred)))
print("Classification report (validation):\n {0}".format(classification_report(y1_val, y1_val_pred)))


# In[19]:

# 绘制ROC曲线
y1_valid_score_lr1 = lr_clf1.predict_proba(X1_val)
y1_valid_score_lr2 = lr_clf2.predict_proba(X1_val)

fpr_lr1, tpr_lr1, thresholds_lr1 = roc_curve(y1_val, y1_valid_score_lr1[:, 1])
fpr_lr2, tpr_lr2, thresholds_lr2 = roc_curve(y1_val, y1_valid_score_lr2[:, 1])

roc_auc_lr1 = auc(fpr_lr1, tpr_lr1)
roc_auc_lr2 = auc(fpr_lr2, tpr_lr2)

plt.plot(fpr_lr1, tpr_lr1, fpr_lr2, tpr_lr2, lw=2, alpha=.6)
plt.plot([0, 1], [0, 1], lw=2, linestyle="--")
plt.xlim([0, 1])
plt.ylim([0, 1.05])
plt.xlabel("FPR")
plt.ylabel("TPR")
plt.title("ROC curve")
plt.legend(["Logistic Reg 1 (AUC {:.4f})".format(roc_auc_lr1),
            "Logistic Reg 2 (AUC {:.4f})".format(roc_auc_lr2)], fontsize=8, loc=2)

