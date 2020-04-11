from mongoengine import Document
from mongoengine import (StringField, IntField)
from datetime import datetime


class ModelUser(Document):

    meta = {"collection": "user"}

    id = StringField(primary_key=True)
    _in_time = StringField(required=True, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    _utime = StringField(required=True, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    nickname = StringField(required=True)
    photo = StringField(required=True)
    sex = StringField(default="unknown", required=True)
    delete_flag = IntField(default=0, required=True)
