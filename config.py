class Config(object):
    """
    配置信息
    """
    # 秘钥配置,随机乱码
    SECRET_KEY = 'JSFJBJBFEHI,NKHOHIO'

    # redis配置
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_DB = 8

    # 配置mysql
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/odk'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 配置jwt
    JWT_SECRET_KEY = 'lksjdflkjslfjlkjdsflk'
    JWT_ACCESS_TOKEN_EXPIRES = 3600

    # 后台管理站点配置
    FLASK_ADMIN_SWATCH = 'cerulean'

    # celery配置
    CELERY_BROKER_URL = 'redis://localhost:6379'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379'


class DevelopConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    pass


config = {
    'dev': DevelopConfig,
    'pro': ProductionConfig
}