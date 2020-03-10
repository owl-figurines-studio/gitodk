import pickle
import os
def predict(dic,pwd=None):
    # pwd :代表odk的路径
    # pwd = os.getcwd()
    # father_path = os.path.abspath(os.path.dirname(pwd) + os.path.sep + ".")
    # print(pwd)
    with open(pwd+"/utils/diabetes/models/diabetes_base.model", 'rb') as file:
       model=pickle.load(file)
    with open(pwd+"/utils/diabetes/models/diabetes_base.std", 'rb') as file:
       std=pickle.load(file)
    with open(pwd+"/utils/diabetes/models/columns",'r') as f:
        col_str = f.read()
    col_lst = col_str.split(",")
    # print(col_lst)
    # data_in = [[148, 0, 33.6, 50]]
    data_in = [[dic[i] for i in col_lst]]
    data_in_tr = std.transform(data_in)
    # print(data_in_tr)
    ret = model.predict(data_in_tr)
    print("predict: ",ret)
    return ret[0]
if __name__ == '__main__':
    pwd = os.getcwd()
    # print(pwd)
    father_path = os.path.abspath(os.path.dirname(pwd) + os.path.sep + "../")
    # print(father_path)
    predict({"Glucose":183,"Insulin":0,"BMI":23.4,"Age":32,"phone":19},pwd=father_path)