class Config(object):
    '''
    这是相关的配置
    '''
    SECRET_KEY = 'JSFJBJBFEHI,NKHOHIO'

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

    # when backend is elasticsearch, MSEARCH_INDEX_NAME is unused
    # flask-msearch will use table name as elasticsearch index name unless set __msearch_index__
    MSEARCH_INDEX_NAME = 'msearch'
    # simple,whoosh,elaticsearch, default is simple
    MSEARCH_BACKEND = 'whoosh'
    # table's primary key if you don't like to use id, or set __msearch_primary_key__ for special model
    MSEARCH_PRIMARY_KEY = 'id'
    # auto create or update index
    MSEARCH_ENABLE = True
    # SQLALCHEMY_TRACK_MODIFICATIONS must be set to True when msearch auto index is enabled
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # when backend is elasticsearch
    ELASTICSEARCH = {"hosts": ["127.0.0.1:3306"]}



class DevelopConfig(Config):
    DEBUG = True



class ProductionConfig(Config):
    pass


config = {
    'dev':DevelopConfig,
    'pro':ProductionConfig
}