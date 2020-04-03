from redis import Redis
import pymysql
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from celery import Celery

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


from config import config
from odk.utils.MyCoverter import MyCoverter
from odk.utils.Returns import ret_data

from fdfs_client.client import Fdfs_client
from pymongo import MongoClient

# 创建链接对象
client = MongoClient('39.107.238.66', 27017)

# 获取操作句柄
mongodb = client.odk01
pymysql.install_as_MySQLdb()
db = SQLAlchemy()
verify_rs = Redis(host='39.107.238.66',port=6379,db=8,decode_responses=True)
fastdfs_client = Fdfs_client('./odk/utils/fastdfs/client.conf')


from odk import models

# celery = Celery()

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery



def create_app(config_name):
    app = Flask(__name__)
    from odk.schema.schema import schema
    from flask_graphql import GraphQLView
    # from odk.database.base import connect
    app.add_url_rule("/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True))

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    jwt = JWTManager(app)

    @jwt.expired_token_loader
    @jwt.invalid_token_loader
    def my_expired_token_callback(expired_token):
        return ret_data(401,'身份信息有误',2004,)


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

    app.config.update(
        CELERY_BROKER_URL='redis://localhost:6379',
        CELERY_RESULT_BACKEND='redis://localhost:6379'
    )


    return app
# app = create_app('dev')
# celery = make_celery(app)
#
# @celery.task()
# def add_together(a, b):
#     return a + b