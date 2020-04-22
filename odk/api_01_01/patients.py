from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
import fhirclient.models.patient as p
import fhirclient.models.humanname as hn
import fhirclient.models.fhirdate as fdate
import fhirclient.models.address as ad

from . import api
from odk.utils.Returns import response_data
from odk import mongodb
from odk.database.model_patient import ModelPatient


@api.route('/patient', methods=['GET', 'POST', 'DELETE', 'PUT'])
@jwt_required
def patient():
    user = get_jwt_identity()
    print("user:", user)

    if user is None:
        return response_data(2004, 403, '访问被禁止')
    # user = 19957892910
    patient_list = mongodb.basic_information.find({'id': str(user)})
    print(patient_list)

    if request.method == 'POST':
        count = 0
        for i in patient_list:
            print(i['active'])
            if i['active'] is True:
                count += 1
        if count == 0:
            patient_ = p.Patient({'id': str(user)})
            # 设置名字
            name = hn.HumanName()
            name.given = [request.form["name_given"]]
            name.family = request.form["name_family"]
            patient_.name = [name]
            # 设置性别 只能是male或者female
            patient_.gender=request.form["gender"] if request.form["gender"] == "男" or request.form["女"] == "female"\
                else ""
            # 设置生日
            patient_.birthDate = fdate.FHIRDate().with_json(request.form["birthDate"])
            # 设置逻辑删除
            patient_.active = True
            # 设置地址
            patient_.address = [ad.Address({"city":request.form["city"]})]
            ret = mongodb.basic_information.insert_one(patient_.as_json())
            print(ret)
            return response_data(1003)
        else:
            return response_data(2008)

    elif request.method == 'GET':
        dict01 = mongodb.basic_information.find_one({'id': str(user), 'active': True})
        if dict01 is None:
            return response_data(2011)
        dict02 = {}
        del dict01['_id']
        dict02['city'] = dict01['address'][0]['city']
        dict02['birthDate']=dict01['birthDate']
        dict02['gender'] = dict01['gender']
        dict02['name'] = str(dict01['name'][0]['family'])+str(dict01['name'][0]['given'][0])
        return response_data(1005, **dict02)

    elif request.method=='DELETE':
        count = 0
        for i in patient_list:
            print(i['active'])
            if i['active'] is True:
                count += 1
        if count >= 1:
            mongodb.basic_information.update_one({'id': str(user),'active':True}, {'$set':{'active':False}})
            # mongodb.basic_information.delete_one({'id':str(user)})
            return response_data(1004)
        else:
            return response_data(2010)

    elif request.method=='PUT':
        count = 0
        for i in patient_list:
            print(i['active'])
            if i['active'] is True:
                count += 1
        if count==1:
            patient = p.Patient({'id': str(user)})
            # 设置名字
            name = hn.HumanName()
            name.given = [request.form["name_given"]]
            name.family = request.form["name_family"]
            patient.name = [name]
            # 设置性别 只能是male或者female
            patient.gender = request.form["gender"] if request.form["gender"] == "男" or request.form[
                "女"] == "female" else ""
            # 设置生日
            patient.birthDate = fdate.FHIRDate().with_json(request.form["birthDate"])
            # 设置逻辑删除
            patient.active = True
            # 设置地址
            patient.address = [ad.Address({"city": request.form["city"]})]
            mongodb.basic_information.update_one({'id':str(user)}, {'$set': patient.as_json()})
            return response_data(1006)
        else:
            return response_data(2009)
    return response_data(1000, test='hello world')

