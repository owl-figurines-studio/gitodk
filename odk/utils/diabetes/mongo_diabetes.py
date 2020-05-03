from sklearn.feature_selection import SelectKBest     # 选择较好的k个特征
from sklearn.feature_selection import chi2            # 卡方检验
from sklearn.preprocessing import StandardScaler      # 标准化
from sklearn.model_selection import KFold             # K折交叉验证
from sklearn.model_selection import cross_val_score   # 交叉验证  过拟合的问题
from sklearn.model_selection import train_test_split  # 随机拆分训练集和测试集
from sklearn.metrics import confusion_matrix          # 混淆矩阵
from sklearn.metrics import classification_report     # 模型检测报告

# 相关训练算法的导入
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC

import pickle  # 模型导入导出工具
import pandas as pd
from pymongo import MongoClient
import seaborn as sns            # 画图
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')  # 消除警告


def get_best_model(pima):
    """
    输入pandas的dateframe,自动导出相关模型
    :param pima:
    :return:
    """
    # 拆分特征值和目标值
    X = pima.iloc[:, 0:-1]
    Y = pima.iloc[:, -1]
    # print(X.describe())  # 显示描述信息

    # 画出箱型图
    # X.plot(kind='box', subplots=True, layout=(3, 3), sharey=False, figsize=(16, 14))

    # corr = pima.corr()              # 计算变量的相关系数，得到一个 N*N 的矩阵
    # print("corr = ",corr)
    # plt.subplots(figsize=(14,12))   # 可以先试用plt设置画布的大小，然后在作图，修改
    # sns.heatmap(corr, annot = True) # 使用热度图可视化这个相关系数矩阵

    # plt.show()  # 显示图片

    select_top_4 = SelectKBest(score_func=chi2, k=4)  # 通过卡方检验选择4个得分最高的特征
    fit = select_top_4.fit(X, Y)  # 获取特征信息和目标值信息
    features = fit.transform(X)  # 特征转换

    # 构造新特征DataFrame
    col = [X.columns[i] for i in fit.get_support(indices=True)]
    X_features = pd.DataFrame(data=features, columns=col)

    # 它将属性值更改为 均值为0，标准差为1 的 高斯分布.
    # 当算法期望输入特征处于高斯分布时，它非常有用
    std = StandardScaler()
    # 通过sklearn的preprocessing数据预处理中StandardScaler特征缩放 标准化特征信息
    rescaledX = std.fit_transform(X_features)
    X = pd.DataFrame(data=rescaledX, columns=X_features.columns)  # 构建新特征DataFrame

    # 切分数据集为：特征训练集、特征测试集、目标训练集、目标测试集
    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, random_state=2019, test_size=0.2)
    # print(X_train.head())  # 显示最开始的几个数据

    # 构建多个算法的字典
    models = dict()
    models["LogisticRegression"] = LogisticRegression          # 逻辑回归
    models["GaussianNB"] = GaussianNB                          # 高斯朴素贝叶斯
    models["KNeighborsClassifier"] = KNeighborsClassifier      # K近邻分类
    models["DecisionTreeClassifier"] = DecisionTreeClassifier  # 决策树分类
    models["SVM"] = SVC                                        # 支持向量机分类

    all_results = {}
    avg_results = {}
    best_result = {"name": '', "result": 0}
    for name, model in models.items():
        # 10折交叉验证
        kflod = KFold(n_splits=10, random_state=2020)
        cv_result = cross_val_score(model(), X_train, Y_train,
                                    cv=kflod, scoring='accuracy')
        mean_ret = cv_result.mean()  # 求10次结果的平均值
        if best_result["result"] < mean_ret:  # 找到平均值最好的结果
            best_result["name"] = name
            best_result["result"] = mean_ret
        all_results[name] = cv_result
        avg_results[name] = mean_ret

    # 打印全部结果,平均值结果,平均值最好的结果
    import matplotlib.pyplot as plt
    print("all_result: ---")
    x_data = [i for i in range(1,11)]
    color = ['red','blue','green','gray','black']
    i = 0
    for name, result in all_results.items():
        print("---", name, ":", result)
        # plt.plot(x_data, result, color=color[i], linestyle='-.',label=name)
        # i += 1
    # plt.legend()
    # plt.show()

    from sklearn.model_selection import GridSearchCV


    print("avg_result: ===")
    for name, result in avg_results.items():
        print("===", name, ":", result)

    print("best_result: +++")
    for name, result in best_result.items():
        print("+++", name, ":", result)

    # 重新进行分割
    # x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.25, random_state=5)
    # 将最好的算法进行训练和预测
    best_classifier_name = models[best_result["name"]]
    best_classifier_name = LogisticRegression
    print(best_classifier_name)
    best_classifier = best_classifier_name()
    param_grid = dict()
    if best_classifier_name is LogisticRegression:
        print("---LogisticRegression")
        param_grid = {'C': range(1, 100), "solver": ['newton-cg', 'lbfgs', 'liblinear', 'sag']}
    elif best_classifier_name is GaussianNB:
        param_grid = {'var_smoothing': [1e-8,1e-9,1e-10]}
        print("---GaussianNB")
    elif best_classifier_name is KNeighborsClassifier:
        print("---KNeighborsClassifier")
        param_grid = {"n_neighbors": range(3, 10, 2),
                      "weights": ['uniform', 'distance'],
                      "algorithm": ['auto', 'ball_tree', 'kd_tree', 'brute'],
                      "leaf_size": range(10,100,10),
                      "p": range(1,10)}

        diabetes = pima
        x_train, x_test, y_train, y_test = train_test_split(diabetes.loc[:, diabetes.columns != 'Outcome'],
                                                            diabetes['Outcome'],
                                                            stratify=diabetes['Outcome'], random_state=66)

        training_accuracy = []
        test_accuracy = []
        # try n_neighbors from 1 to 10
        neighbors_settings = range(1, 11)

        for n_neighbors in neighbors_settings:
            # build the model
            knn = KNeighborsClassifier(n_neighbors=n_neighbors)
            knn.fit(x_train, y_train)
            # record training set accuracy
            training_accuracy.append(knn.score(x_train, y_train))
            # record test set accuracy
            test_accuracy.append(knn.score(x_test, y_test))
        plt.plot(neighbors_settings, training_accuracy, label="training accuracy")
        plt.plot(neighbors_settings, test_accuracy, label="test accuracy")
        plt.ylabel("Accuracy")
        plt.xlabel("n_neighbors")
        plt.legend()
        plt.savefig('knn_compare_model')
        plt.show()
    elif best_classifier_name is DecisionTreeClassifier:
        print("---DecisionTreeClassifier")
        param_grid = {"criterion": ["gini", "entropy"]}
    elif best_classifier_name is SVC:
        param_grid = {'C': [0.1,0.5,1,5,10,100],
                      "kernel":['linear', 'poly', 'rbf', 'sigmoid']}
        print("---SVC")

    best_classifier_gcv = GridSearchCV(best_classifier, param_grid, refit=True, verbose=2, scoring='roc_auc',n_jobs=-1)
    best_classifier_gcv.fit(X_train, Y_train)

    print("---best_params:", best_classifier_gcv.best_params_)
    # print("---得到的最佳模型:", best_classifier_gcv.estimator)
    print("---score:", best_classifier_gcv.best_score_)
    # 预测
    y_predict = best_classifier_gcv.predict(X_test)

    # 分类报告
    print(classification_report(Y_test, y_predict))
    # best_classifier.fit(x_train, y_train)
    # y_predict = best_classifier.predict(x_test)
    from sklearn import metrics
    # 画出ROC曲线
    fpr, tpr, threshold = metrics.roc_curve(Y_test, y_predict)
    roc_auc = metrics.auc(fpr, tpr)
    plt.figure(figsize=(6, 6))
    plt.title('Validation ROC')
    plt.plot(fpr, tpr, 'b', label='Val AUC = %0.3f' % roc_auc)
    plt.legend(loc='lower right')
    plt.plot([0, 1], [0, 1], 'r--')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.show()


    # cm = confusion_matrix(Y_test, y_predict)  # 得到混淆矩阵
    # print(cm)
    # label = ["1","0"]
    # # 画出混淆矩阵的热力图
    # sns.heatmap(cm, annot = True,  fmt='.20g', xticklabels=label, yticklabels=label)
    # plt.show()

    # cr = classification_report(y_test,y_predict)
    # print("检测报告为:")
    # print(cr)  # 打印模型的检测报告

    # 导出较好的特征
    with open("models/columns", 'w') as f:
        f.write(",".join(col))

    # 导出标准化模型
    with open("models/diabetes_base.std", 'wb') as file:
        pickle.dump(std, file)

    # 导出训练好的模型
    with open("models/diabetes_base.model", 'wb') as file:
        pickle.dump(best_classifier_gcv, file)

    return std, best_classifier_gcv


if __name__ == '__main__':
    # 创建链接对象
    client = MongoClient('127.0.0.1', 27017)
    mongodb = client.odk01

    # 找到outcome不为-1的数据,-1表示用户未填写结果
    mongo_data = pd.DataFrame(list(mongodb.diabetes.find({'Outcome': {"$ne": -1}})))
    pima = mongo_data.loc[:, ['Glucose', 'Insulin', 'BMI', 'Age', 'BloodPressure', 'Outcome']]

    std, best_classifier = get_best_model(pima)
    data_in = [[148, 0, 33.6, 50]]
    data_in_tr = std.transform(data_in)
    # print(data_in_tr)
    ret = best_classifier.predict(data_in_tr)
    print(ret)


