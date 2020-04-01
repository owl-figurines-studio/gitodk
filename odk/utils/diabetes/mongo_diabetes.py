import pymongo
import pandas as pd

client = pymongo.MongoClient('39.107.238.66', 27017)

# 获取操作句柄
mongodb = client.odk01
# ret = mongodb.diabetes.find()
pima = pd.DataFrame(list(mongodb.diabetes.find({'outcome':{"$ne":-1}})))
# pima = pd.DataFrame(list(mongodb.diabetes.find({'outcome':-1})))
# print(ret)
del pima['_id']
# print(pima)



from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

pima = pima.loc[:,['Glucose','Insulin','BMI','Age','BloodPressure','outcome']]

X = pima.loc[:,['Glucose','Insulin','BMI','Age','BloodPressure']]  # 特征列 0-7列，不含第8列
Y = pima.loc[:,'outcome']  # 目标列为第8列

import seaborn as sns
import matplotlib.pyplot as plt
# X.plot(kind='box', subplots=True, layout=(3,3), sharex=False,sharey=False, figsize=(16,14))

# corr = pima.corr()  # 计算变量的相关系数，得到一个N * N的矩阵
#
# print("corr = ",corr)
# plt.subplots(figsize=(14,12)) # 可以先试用plt设置画布的大小，然后在作图，修改
# sns.heatmap(corr, annot = True) # 使用热度图可视化这个相关系数矩阵
#
# plt.show()

# print("##################")
# print(X.describe())
select_top_4 = SelectKBest(score_func=chi2, k=4)  # 通过卡方检验选择4个得分最高的特征


fit = select_top_4.fit(X, Y)  # 获取特征信息和目标值信息
features = fit.transform(X)  # 特征转换

# 构造新特征DataFrame
col = [X.columns[i] for i in fit.get_support(indices=True)]
X_features = pd.DataFrame(data = features, columns=col)


# 它将属性值更改为 均值为0，标准差为1 的 高斯分布.
# 当算法期望输入特征处于高斯分布时，它非常有用

from sklearn.preprocessing import StandardScaler



std = StandardScaler()
rescaledX =std.fit_transform(X_features)  # 通过sklearn的preprocessing数据预处理中StandardScaler特征缩放 标准化特征信息
X = pd.DataFrame(data=rescaledX, columns=X_features.columns)  # 构建新特征DataFrame


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
# print(X_train.head())

# models = []
# models.append(("LR", LogisticRegression()))     # 逻辑回归
# models.append(("NB", GaussianNB()))             # 高斯朴素贝叶斯
# models.append(("KNN", KNeighborsClassifier()))  # K近邻分类
# models.append(("DT", DecisionTreeClassifier())) # 决策树分类
# models.append(("SVM", SVC()))                   # 支持向量机分类
models={}
# models["LR"] = LogisticRegression()  # 逻辑回归
# models["NB"] = GaussianNB()          # 高斯朴素贝叶斯
# models["KNN"]= KNeighborsClassifier() # K近邻分类
# models["DT"] = DecisionTreeClassifier() # 决策树分类
# models["SVM"]= SVC()                   # 支持向量机分类

models["LogisticRegression"] = LogisticRegression     # 逻辑回归
models["GaussianNB"] = GaussianNB             # 高斯朴素贝叶斯
models["KNeighborsClassifier"]= KNeighborsClassifier   # K近邻分类
models["DecisionTreeClassifier"] = DecisionTreeClassifier # 决策树分类
models["SVM"]= SVC                    # 支持向量机分类

import warnings
warnings.filterwarnings('ignore')  #消除警告

results = []
names = []
results_={}
best_name = ''
best_ret = 0
from sklearn import metrics
for name, model in models.items():
    kflod = KFold(n_splits=10, random_state=2020)
    cv_result = cross_val_score(
        model(), X_train, Y_train, cv=kflod, scoring='accuracy')
    mean_ret = cv_result.mean()
    if best_ret<mean_ret:
        best_ret=mean_ret
        best_name=name
    results_[name]=mean_ret
    names.append(name)
    results.append(cv_result)


# print(results,names)
# for i in range(len(names)):
#     print(names[i], results[i].mean())
print(results_)
print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
print(best_name,best_ret)



from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(X,Y,test_size=0.25,random_state=5)
gaussiannb_classifier = models[best_name]()
gaussiannb_classifier.fit(x_train,y_train)
y_predict = gaussiannb_classifier.predict(x_test)


# fpr, tpr, threshold = metrics.roc_curve(y_test, y_predict)
# roc_auc = metrics.auc(fpr, tpr)
# plt.figure(figsize=(6, 6))
# plt.title('Validation ROC')
# plt.plot(fpr, tpr, 'b', label='Val AUC = %0.3f' % roc_auc)
# plt.legend(loc='lower right')
# plt.plot([0, 1], [0, 1], 'r--')
# plt.xlim([0, 1])
# plt.ylim([0, 1])
# plt.ylabel('True Positive Rate')
# plt.xlabel('False Positive Rate')
# plt.show()

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test,y_predict)
print(cm)

label = ["1","0"] #
sns.heatmap(cm, annot = True,  fmt='.20g',xticklabels=label, yticklabels=label)
plt.show()

from sklearn.metrics import classification_report
cr = classification_report(y_test,y_predict)
print(cr)

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


