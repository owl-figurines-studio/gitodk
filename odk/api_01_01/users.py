from flask_jwt_extended import create_access_token,jwt_required,jwt_optional,get_jwt_identity
from flask import request,make_response
import random

from . import api
from odk.models import User
from odk import db,verify_rs,mongodb
from odk.libs.yuntongxun.sms import CCP
from odk.utils.Returns import ret_data #,ret_upload_data,ret_user_data
from odk.utils.fastdfs.Images import save_Image

# @api01.route('/userinfo/<myre("\d{5}"):user_id>')
# def userinfo(user_id):
#     return '这是用户'

@api.route('/user/verify',methods=['POST'])
# 获取手机验证
# 前端 : POST  表单: userphone=19957892906
# 后端 : 返回   "验证码获取成功"
def verify():
    userphone = request.form.get('userphone')
    print(userphone)
    print(type(userphone))
    if userphone is None:
        return ret_data(403, '访问被禁止', 2002)
        # return {'code':403,'message':'访问被禁止','data':{'verifyStateCode':2001,'message':'手机号为空'}},403

    if userphone == '' or len(userphone)!=11:
        return ret_data(403,'访问被禁止',2002)
        # return {'code':403,'message':'访问被禁止','data':{'verifyStateCode':2002,'message':'手机号格式错误'}},403
    # todo 生成短信验证码
    phone_code = '%06d' % random.randint(0, 999999)
    # phone_code = 123456
    print('短信验证码', phone_code)

    # todo 将生成的短信验证码存入在redis 中
    # 设置过期时间并保存
    verify_rs.setex(userphone,120,phone_code)

    # 发送短信验证码
    ccp = CCP()
    ccp.send_template_sms(userphone, [phone_code ,1], 1)

    return ret_data(200,'请求成功',1000)
    # return {'code':200,'message':'请求成功','data':{'message':'获取验证码成功','verifyStateCode':1000}},200

@api.route('/user/login',methods=['POST'])
# 用户登录
def login():
    try:# 获取手机号和验证码
        qian_vercode=request.form['verification_code']
        qian_userphone = request.form['userphone']
        get_redis_verify=verify_rs.get(qian_userphone)
    except:
        print('前端输入错误')
        return ret_data(403, '访问被禁止', 2003)
        # return {'code':403,'message':'访问被禁止','data':{'verifyStateCode':2003,'message':'验证码错误'}},403
    # 判断验证码是不是正确
    if qian_vercode!=get_redis_verify:
        return ret_data(403, '访问被禁止', 2003)
        # return {'code':403,'message':'访问被禁止','data':{'verifyStateCode':2003,'message':'验证码错误'}},403
    # 从数据库中查找用户
    user_lst=User.query.filter_by(user_phone=qian_userphone).all()
    # 查找结果为空,则新建
    print(user_lst)
    if user_lst == []:
        print('新创建一个user')
        obj = User(user_phone=qian_userphone)
        db.session.add(obj)
        db.session.commit()
    else:
        print('已有user,不操作')
    # 新建jwt,并返回个前端
    access_token = create_access_token(identity=qian_userphone)
    ret,state = ret_data(200, '请求成功', 1007)
    response = make_response(ret)
    response.headers['token'] = access_token
    response.state = state

    return response
    # return {'code':200,'message':'请求成功','data':{'verifyStateCode':1001,'message':'验证通过,可登录','access_token':access_token}},200


@api.route('/user/test',methods=['GET','POST','DELETE','PUT'])
@jwt_optional
def test_test():
    user = get_jwt_identity()
    print(user)
    if user is None:
        return ret_data(403, '访问被禁止', 2004,)
        # return {'code':403,'message':'访问被禁止','data':{'verifyStateCode':2004,'message':'没有登录'}},401
    if request.method=='POST':
        return ret_data(200, '请求成功', 1000, test='post method')
    elif request.method=='GET':
        return ret_data(200, '请求成功', 1000, test='get method')
    elif request.method=='DELETE':
        return ret_data(200, '请求成功', 1000, test='delete method')
    elif request.method=='PUT':
        return ret_data(200, '请求成功', 1000, test='put method')
    return ret_data(200, '请求成功', 1000,test='hello world')
    # return {'code':200,'message':'请求成功','data':{'verifyStateCode':1000,'message':'登录成功','data':'hello world'}},200



@api.route('/user/image',methods=['POST'])
def test_image():
    xxx = request.files
    try:
        file = xxx['UploadImage']
        print(file)
        # if file
    except KeyError as e:
        return ret_data(200,'请求成功',2007)
    return save_Image(file)


# 微信登录
@api.route('/user/wlogin')
def wlogin():
    import odk.utils.const.login_const
    import requests  # 导入request模块
    url = 'https://api.weixin.qq.com/sns/jscode2session'
    response = requests.get(url)  # 用导入的request模块的get方法访问URL
    print(response.status_code)  # 调用response里的status_code方法查看状态码
    print(response.text)  # 调用response里的text #字符串方式的响应体，会自动根据响应头部的字符编码进行解码

# 测试git
@api.route('/user/fhir')
def fhir():
    import fhirclient.models.patient as p
    import fhirclient.models.humanname as hn
    patient = p.Patient({'id': 'patient-1'})
    print(patient.id)
    # prints `patient-1`

    name = hn.HumanName()
    name.given = ['Peter']
    name.family = 'Parker'
    patient.name = [name]


    print(mongodb)

    print(patient.as_json())
    dict01 = patient.as_json()
    ret = mongodb.a.insert_one(dict01)
    print(ret)
    ret = mongodb.a.find()
    for i in ret:
        print(i)
    print('111111111111111111')

    import json
    import fhirclient.models.patient as p
    with open('/home/python/Desktop/odk/patient-example.json', 'r') as h:
        pjs = json.load(h)
    patient = p.Patient(pjs)
    dict02 = patient.as_json()

    ret = mongodb.a.insert_one(dict02)
    print(ret)
    ret = mongodb.a.find()
    for i in ret:
        print(i)
    print('2222222222222222')
    print(patient.name[0].given)
    print(patient.name)
    print(patient.gender)
    print(patient.photo)
    print(patient.address)
    print("-------------------------")
    # prints patient's given name array in the first `name` property
    return ret_data(200,'请求成功',1000)

