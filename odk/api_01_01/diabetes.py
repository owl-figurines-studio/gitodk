from flask_jwt_extended import jwt_required,jwt_optional,get_jwt_identity
from flask import request
import json

from . import api
from odk.utils.Returns import ret_data
from odk import mongodb
import fhirclient.models.patient as p
import fhirclient.models.humanname as hn
import fhirclient.models.fhirdate as fdate
import fhirclient.models.address as ad

from odk.database.model_diabetes import ModelDiabetes
from fhirclient.models import observation
import random,os
from odk.utils.diabetes.predict import predict

@api.route('/diabetes',methods=['POST'])
@jwt_required
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
    # print(data)
    # data = {i:v for i,v in data}
    print(data)
    diabetes = ModelDiabetes(**data)
    diabetes.save()
    pwd = os.getcwd()
    # print("diabetes: pwd:",pwd)
    ret = predict(data,pwd+"/odk")
    result = "得病了"
    if ret == 0:
        result="没有得病"
    return ret_data(200,'请求成功',1008,result=result)

@api.route('/FhirDiabetes',methods=['POST'])
@jwt_required
def fhirdiabetes_predict():
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
    # print("diabetes: pwd:",pwd)
    ret = predict(data,pwd+"/odk")
    result = "得病了"
    if ret == 0:
        result="没有得病"
    return ret_data(200,'请求成功',1008,result=result)




