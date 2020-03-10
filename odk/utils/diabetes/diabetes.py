import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
pima=pd.read_csv('diabetes.csv')
del pima['Pregnancies']
# print(pima.columns)
# print(pima.head())

# 导入和特征选择相关的包
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

# SelectKBest() 只保留K个最高分的特征
# SelectPercentile() 只保留用户指定百分比的最高得分的特征
# 使用常见的单变量统计检验：假正率SelectFpr，错误发现率SelectFdr，或者总体错误率SelectFwe
# GenericUnivariateSelect通过结构化策略进行特征选择，通过超参数搜索估计器进行特征选择

# SelectKBest()和SelectPercentile()能够返回特征评价的得分和P值
#
# sklearn.feature_selection.SelectPercentile(score_func=<function f_classif>, percentile=10)
# sklearn.feature_selection.SelectKBest(score_func=<function f_classif>, k=10)

# 其中的参数score_func有以下选项：

#【1】回归：f_regression:相关系数，计算每个变量与目标变量的相关系数，然后计算出F值和P值
#          mutual_info_regression:互信息，互信息度量X和Y共享的信息：
#         它度量知道这两个变量其中一个，对另一个不确定度减少的程度。
#【2】分类：chi2：卡方检验
#          f_classif:方差分析，计算方差分析（ANOVA）的F值（组间均方/组内均方）；
#          mutual_info_classif:互信息，互信息方法可以捕捉任何一种统计依赖，但是作为非参数方法，
#                              需要更多的样本进行准确的估计。

X = pima.iloc[:, 0:7]  # 特征列 0-7列，不含第8列
Y = pima.iloc[:, 7]  # 目标列为第8列

select_top_4 = SelectKBest(score_func=chi2, k=4)  # 通过卡方检验选择4个得分最高的特征


fit = select_top_4.fit(X, Y)  # 获取特征信息和目标值信息
features = fit.transform(X)  # 特征转换
# print(features)
# print("$$$$$$$$$$$$$$$$$$$$$$$$")
# print(fit.get_support(indices=True))
# print(pima.columns)
# print([pima.columns[i] for i in fit.get_support(indices=True)])
# 构造新特征DataFrame
col = [pima.columns[i] for i in fit.get_support(indices=True)]
X_features = pd.DataFrame(data = features, columns=col)

# X_features.head()

# 它将属性值更改为 均值为0，标准差为1 的 高斯分布.
# 当算法期望输入特征处于高斯分布时，它非常有用

from sklearn.preprocessing import StandardScaler

# StandardScaler
# 作用：去均值和方差归一化。且是针对每一个特征维度来做的，而不是针对样本。
#StandardScaler对每列分别标准化，
# 因为shape of data: [n_samples, n_features]
# 【注：】 并不是所有的标准化都能给estimator带来好处。

std = StandardScaler()
rescaledX =std.fit_transform(X_features)  # 通过sklearn的preprocessing数据预处理中StandardScaler特征缩放 标准化特征信息
X = pd.DataFrame(data=rescaledX, columns=X_features.columns)  # 构建新特征DataFrame
X.head()

from sklearn.model_selection import KFold  # K折交叉验证
from sklearn.model_selection import cross_val_score  # 交叉验证  过拟合的问题
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split

# 切分数据集为：特征训练集、特征测试集、目标训练集、目标测试集
X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, random_state=2019, test_size=0.2)
print(X_train.head())
models = []
models.append(("LR", LogisticRegression()))     # 逻辑回归
models.append(("NB", GaussianNB()))             # 高斯朴素贝叶斯
models.append(("KNN", KNeighborsClassifier()))  # K近邻分类
models.append(("DT", DecisionTreeClassifier())) # 决策树分类
models.append(("SVM", SVC()))                   # 支持向量机分类

import warnings
warnings.filterwarnings('ignore')  #消除警告

results = []
names = []
for name, model in models:
    kflod = KFold(n_splits=10, random_state=2020)
    cv_result = cross_val_score(
        model, X_train, Y_train, cv=kflod, scoring='accuracy')
    names.append(name)
    results.append(cv_result)
# print(results,names)

print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
# for i in range(len(names)):
#     print("mean",names[i], results[i].mean())
#     print("max",names[i], results[i].max())
#     print()


# best_model=None
# for name,model in models:
#     if name=="NB":
#         best_model=model
# print(best_model)
# best_model.predict([[-0.653939,0.904762,0.584771,1.085644]])



from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(X,Y,test_size=0.25,random_state=5)
gaussiannb_classifier = GaussianNB()
gaussiannb_classifier.fit(x_train,y_train)
y_predict = gaussiannb_classifier.predict(x_test)
# accuracy= 100*(y_predict==y_test).sum()/x_test.shape[0]


from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test,y_predict)
print(cm)
from sklearn.metrics import classification_report
cr = classification_report(y_test,y_predict)
print(cr)
# print("Accuracy of the GuassianNb Classifier:  ",round(accuracy,4),'%')

import pickle

with open("models/columns",'w') as f:
    f.write(",".join(col))


with open("models/diabetes_base.std", 'wb') as file:
    pickle.dump(std, file)

with open("models/diabetes_base.model", 'wb') as file:
    pickle.dump(gaussiannb_classifier, file)


data_in = [[148,0,33.6,50]]
data_in_tr = std.transform(data_in)
print(data_in_tr)
ret = gaussiannb_classifier.predict(data_in_tr)
print(ret)



