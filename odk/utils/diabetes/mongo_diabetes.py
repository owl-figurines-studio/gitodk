import pymongo
import pandas as pd

client = pymongo.MongoClient('127.0.0.1', 27017)

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



X = pima.loc[:,['Glucose','Insulin','BMI','Age','BloodPressure']]  # 特征列 0-7列，不含第8列
Y = pima.loc[:,'outcome']  # 目标列为第8列
print("##################")
print(X.head())
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
print(X_train.head())
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

models["LR"] = LogisticRegression     # 逻辑回归
models["NB"] = GaussianNB             # 高斯朴素贝叶斯
models["KNN"]= KNeighborsClassifier   # K近邻分类
models["DT"] = DecisionTreeClassifier # 决策树分类
models["SVM"]= SVC                    # 支持向量机分类

import warnings
warnings.filterwarnings('ignore')  #消除警告

results = []
names = []
results_={}
best_name = ''
best_ret = 0
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



from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test,y_predict)

from sklearn.metrics import classification_report
cr = classification_report(y_test,y_predict)

import pickle

# with open("models/columns",'w') as f:
#     f.write(",".join(col))
#
#
# with open("models/diabetes_base.std", 'wb') as file:
#     pickle.dump(std, file)
#
# with open("models/diabetes_base.model", 'wb') as file:
#     pickle.dump(gaussiannb_classifier, file)


data_in = [[148,0,33.6,50]]
data_in_tr = std.transform(data_in)
print(data_in_tr)
ret = gaussiannb_classifier.predict(data_in_tr)
print(ret)


