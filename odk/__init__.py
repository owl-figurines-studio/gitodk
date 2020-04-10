from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_admin import Admin
from flask_graphql import GraphQLView
from redis import Redis
from pymongo import MongoClient

from config import config,config_constant
from odk.utils.MyCoverter import MyCoverter
from odk.utils.Returns import response_data
# fdfs_client安装包在./odk/utils/fastdfs/fdfs_client-py-master.zip中
# pip install fdfs_client-py-master.zip
from fdfs_client.client import Fdfs_client


# 创建链接对象
client = MongoClient(config_constant["MONGODB_HOST"],
                     config_constant["MONGODB_PORT"])

# 获取操作句柄
mongodb = client.odk01

redis_verify = Redis(host=config_constant["REDIS_HOST"],
                     port=config_constant["REDIS_PORT"],
                     db=config_constant["REDIS_VERIFY_DB"],
                     decode_responses=True)
fastdfs_client = Fdfs_client(config_constant["FASTDFS_CONFIG"])


def create_app(config_name):
    # 因关联较大,所以这里导入
    from odk.schema.schema import schema
    from odk.api_01_01 import api

    app = Flask(__name__)

    app.add_url_rule("/graphql",
                     view_func=GraphQLView.as_view("graphql",
                                                   schema=schema,
                                                   graphiql=True))

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    jwt = JWTManager(app)

    @jwt.expired_token_loader
    @jwt.invalid_token_loader
    def my_expired_token_callback(expired_token):
        return response_data(2004, 401, '身份信息有误')

    app.config.from_object(config[config_name])

    admin = Admin(app, name='luke', template_mode='bootstrap3')

    app.url_map.converters['myre'] = MyCoverter

    # 注册蓝图
    app.register_blueprint(api, url_prefix='/api')

    print('################')
    print(app.url_map)
    print('################')

    # admin.add_view(ModelView(models.User, db.session,name='用户'))

    return app

