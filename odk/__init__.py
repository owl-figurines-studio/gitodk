from redis import Redis
import pymysql
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


from config import config
from odk.utils.MyCoverter import MyCoverter
from odk.utils.Returns import ret_data

from fdfs_client.client import Fdfs_client

pymysql.install_as_MySQLdb()
db = SQLAlchemy()
verify_rs = Redis(host='127.0.0.1',port=6379,db=8,decode_responses=True)
fastdfs_client = Fdfs_client('./odk/utils/fastdfs/client.conf')


from odk import models




def create_app(config_name):
    app = Flask(__name__)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    jwt = JWTManager(app)

    @jwt.expired_token_loader
    @jwt.invalid_token_loader
    def my_expired_token_callback(expired_token):
        return ret_data(401,'身份信息有误',2005,)


    app.config.from_object(config[config_name])






    admin = Admin(app, name='luke', template_mode='bootstrap3')

    app.url_map.converters['myre'] = MyCoverter

    #关联当前的app
    db.init_app(app)



    #注册蓝图
    from odk.api_01_01 import api
    app.register_blueprint(api,url_prefix='/api')


    print('################')
    print(app.url_map)
    print('################')

    admin.add_view(ModelView(models.User, db.session,name='用户'))



    return app