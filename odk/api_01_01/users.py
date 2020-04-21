import random
import requests

from flask import request, make_response
from flask_jwt_extended import create_access_token, jwt_required

from . import api
from odk import redis_verify, mongodb
from odk.libs.yuntongxun.sms import CCP
from odk.utils.Returns import response_data
from odk.utils.check import check_form_key
from config import config_constant


@api.route('/user/test', methods=['GET', 'POST', 'DELETE', 'PUT'])
# @jwt_required
def test_test():
    """
    测试
    :return:
    """
    return_data = {"test": ''}
    if request.method == 'POST':
        return_data["test"] = 'post method'
    elif request.method == 'GET':
        return_data["test"] = 'get method'
    elif request.method == 'DELETE':
        return_data["test"] = 'delete method'
    elif request.method == 'PUT':
        return_data["test"] = 'put method'
    return response_data(1000, **return_data)


@api.route('/user/code2session', methods=['POST'])
def wechat_login():
    """
    微信登录,获取token
    request.form = {
        "code": "043sT4oa1CKHuM1LkVpa1ns4oa1sT4oE"
    }
    :return: 头部包含token的响应
    """
    must_keys = ["code"]
    form_data = request.form.to_dict()
    errmsg = check_form_key(form_data, must_keys)
    if errmsg:
        return response_data(2016, errmsg=errmsg)
    js_code = form_data['code']
    appid = config_constant["WECHAT_APP_ID"]
    secret = config_constant["WECHAT_SECRET"]
    grant_type = "authorization_code"

    wechat_request_data = {"js_code": js_code,
                           "appid": appid,
                           "secret": secret,
                           "grant_type": grant_type}
    response = requests.get(config_constant["WECHAT_URL"], params=wechat_request_data)
    ret = response.json()
    print("---response:", ret)
    if 'errcode' in ret:
        return response_data(2012, errmsg=ret['errmsg'])
    # ret = {
    #     "session_key": "4xtv9zkCLF9eB7zQWSedgA==",
    #     "openid": "oRVrU5PzUZ4DEIdT3qKP4wNzJlmc"
    # }
    access_token = create_access_token(identity=ret['openid'])
    print("---token:", access_token)
    # 构建新的response
    response, state = response_data(1010)
    return_response = make_response(response)
    # 添加头部token
    return_response.headers['token'] = access_token
    return_response.state = state
    return return_response


@api.route('/user/verify', methods=['POST'])
@jwt_required
def verify():
    """
    短信验证码获取,需要登录
    request.form = {
        "userphone": "12312341234"
    }
    :return:
    """
    must_keys = ["userphone"]
    form_data = request.form.to_dict()
    errmsg = check_form_key(form_data, must_keys)
    if errmsg:
        return response_data(2016, errmsg=errmsg)

    userphone = form_data['userphone']
    print("---userphone:", userphone)

    if userphone == '' or len(userphone) != 11:
        return response_data(2002)

    # 生成短信验证码
    phone_code = '%06d' % random.randint(0, 999999)
    print('---短信验证码:', phone_code)

    # 将生成的短信验证码存入在redis 中
    # 设置过期时间并保存
    redis_verify.setex(userphone, 120, phone_code)

    # 发送短信验证码
    ccp = CCP()
    ccp.send_template_sms(userphone, [phone_code, 1], 1)

    return response_data(1000)


@api.route('/user/verifyok', methods=['POST'])
@jwt_required
def verify_ok():
    """
    判断验证码是否正确
    request.form = {
        "userphone" = "11122223333"
        "verification_code" = "123456"
    }
    :return:
    """
    must_keys = ["userphone", "verification_code"]
    form_data = request.form.to_dict()
    errmsg = check_form_key(form_data, must_keys)
    if errmsg:
        return response_data(2016, errmsg=errmsg)

    verification_code = form_data['verification_code']
    userphone = form_data['userphone']

    # 从redis中取出验证码
    redis_verification_code = redis_verify.get(userphone)

    # 判断验证码是不是正确
    if verification_code != redis_verification_code:
        return response_data(2003, 403, '访问被禁止')

    return response_data(1001)



# 短信登录,不需要了
# @api.route('/user/login', methods=['POST'])
# def login():
#     """
#     登录
#     request.form = {
#         "userphone" = "11122223333"
#         "verification_code" = "
#     }
#     :return:
#     """
#     try:# 获取手机号和验证码
#         qian_vercode=request.form['verification_code']
#         qian_userphone = request.form['userphone']
#         get_redis_verify = verify_rs.get(qian_userphone)
#     except:
#         print('前端输入错误')
#         return response_data(2003, 403, '访问被禁止')
#         # return {'code':403,'message':'访问被禁止','data':{'verifyStateCode':2003,'message':'验证码错误'}},403
#     # 判断验证码是不是正确
#     if qian_vercode != get_redis_verify:
#         return response_data(2003, 403, '访问被禁止')
#         # return {'code':403,'message':'访问被禁止','data':{'verifyStateCode':2003,'message':'验证码错误'}},403
#     # 从数据库中查找用户
#     user_lst=User.query.filter_by(user_phone=qian_userphone).all()
#     # 查找结果为空,则新建
#     print(user_lst)
#     if user_lst == []:
#         print('新创建一个user')
#         obj = User(user_phone=qian_userphone)
#         db.session.add(obj)
#         db.session.commit()
#     else:
#         print('已有user,不操作')
#     # 新建jwt,并返回个前端
#     access_token = create_access_token(identity=qian_userphone)
#     ret,state = response_data(1007)
#     response = make_response(ret)
#     response.headers['token'] = access_token
#     response.state = state
#
#     return response
