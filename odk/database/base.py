from mongoengine import connect

from config import config_constant

connect(config_constant["MONGODB_DB"],
        host=config_constant["MONGODB_HOST"]+":"+str(config_constant["MONGODB_PORT"]))
