import random
import os

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request

from . import api
from odk.utils.Returns import response_data
from odk.database.model_diabetes import ModelDiabetes
from odk.utils.diabetes.predict import predict


@api.route('/diabetes', methods=['POST'])
# @jwt_required
def diabetes_predict():
    data = request.form.to_dict()
    if 'id' not in data.keys():
        data['id'] = str(random.random()*1000000000000000)
    if 'phone' not in data.keys():
        data['phone'] = get_jwt_identity()
    if "BMI" not in data.keys():
        data['BMI'] = float(data['weight'])/(float(data['height'])**2)
    if "outcome" not in data.keys():
        data['outcome'] = -1
    if '' in data.keys():
        data.pop('')
    print("---整理后的data数据:", data)
    diabetes = ModelDiabetes(**data)
    diabetes.save()
    ret = predict(data)
    result = "1"
    if ret == 0:
        result = "0"
    return response_data(1008, result=result)


@api.route('/FhirDiabetes', methods=['POST'])
@jwt_required
def fhir_diabetes_predict():
    data = request.form.to_dict()
    if 'id' not in data.keys():
        data['id'] = str(random.random()*1000000000000000)
    if 'phone' not in data.keys():
        data['phone'] = get_jwt_identity()
    if "BMI" not in data.keys():
        data['BMI'] = float(data['weight'])/(float(data['height'])**2)
    if "outcome" not in data.keys():
        data['outcome'] = -1
    # print(data)
    # data = {i:v for i,v in data}
    print(data)
    diabetes = ModelDiabetes(**data)
    diabetes.save()
    pwd = os.getcwd()
    print("diabetes: pwd:",pwd)
    ret = predict(data, pwd+"/odk")
    result = "得病了"
    if ret == 0:
        result = "没有得病"
    return response_data(1008, result=result)




