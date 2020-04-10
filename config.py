config_constant = {
    # 微信登录需要的配置文件
    "WECHAT_APP_ID": "wxc49a36275e75991b",
    "WECHAT_SECRET": "c5d0a6c4d637728f0d602ec5d9a6c99e",
    "WECHAT_URL": "https://api.weixin.qq.com/sns/jscode2session",
    # redis配置
    "REDIS_HOST": '127.0.0.1',
    "REDIS_PORT": 6379,
    "REDIS_VERIFY_DB": 8,
    # mongodb配置
    "MONGODB_HOST": "127.0.0.1",
    "MONGODB_PORT": 27017,
    "MONGODB_DB": "odk01",
    # fasrdfs配置
    "FASTDFS_CONFIG": './odk/utils/fastdfs/client.conf',
}


class Config(object):
    """
    配置信息
    """
    # 秘钥配置,随机乱码
    SECRET_KEY = 'JSFJBJBFEHINKHOHIO'

    # 配置mysql
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/odk'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 配置jwt
    JWT_SECRET_KEY = 'lksjdflkjslfjlkjdsflk'
    JWT_ACCESS_TOKEN_EXPIRES = 7200

    # 后台管理站点配置
    FLASK_ADMIN_SWATCH = 'cerulean'

    # celery配置
    CELERY_BROKER_URL = 'redis://'+config_constant["REDIS_HOST"]+':'+str(config_constant["REDIS_PORT"])
    CELERY_RESULT_BACKEND = 'redis://'+config_constant["REDIS_HOST"]+':'+str(config_constant["REDIS_PORT"])


class DevelopConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    pass


config = {
    'dev': DevelopConfig,
    'pro': ProductionConfig
}


