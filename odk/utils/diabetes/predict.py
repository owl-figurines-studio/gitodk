import os

import pickle


def predict(dic, pwd=None):
    # pwd :代表odk的路径
    if pwd is None:
        pwd = os.getcwd()+"/odk/utils/diabetes/models/"
        print(pwd)
    with open(pwd+"diabetes_base.model", 'rb') as file:
       model = pickle.load(file)
    with open(pwd+"diabetes_base.std", 'rb') as file:
       std = pickle.load(file)
    with open(pwd+"columns", 'r') as f:
        col_str = f.read()
    col_lst = col_str.split(",")
    # print(col_lst)
    # data_in = [[148, 0, 33.6, 50]]
    data_in = [[dic[i] for i in col_lst]]
    data_in_tr = std.transform(data_in)
    # print(data_in_tr)
    ret = model.predict(data_in_tr)
    print("predict: ", ret)
    return ret[0]


if __name__ == '__main__':
    pwd = os.getcwd()
    # print(pwd)
    # father_path = os.path.abspath(os.path.dirname(pwd) + os.path.sep + "../")
    # print(father_path)
    pwd = pwd+'/models/'
    predict({"Glucose": 183, "Insulin": 0, "BMI": 23.4, "Age": 32, "phone": 19}, pwd)