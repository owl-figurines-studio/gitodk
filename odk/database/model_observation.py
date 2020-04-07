# import sys
# sys.path.append("..")

from mongoengine import Document
from mongoengine import (StringField, IntField,DictField)


class ModelObservation(Document):

    meta = {"collection": "observation"}

    id = StringField(primary_key=True)

    resourceType = StringField(required=True)

    meta_ = DictField()

    subject = DictField()

    encounter = DictField()

    code = DictField()

    valueQuantity = DictField()

    delete_flag = IntField(default=0, required=True)