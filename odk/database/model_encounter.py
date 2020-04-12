from mongoengine import Document
from mongoengine import StringField, IntField, DictField, DateField, BooleanField, ListField


class ModelEncounter(Document):
    meta = {"collection": "encounter"}

    resourceType = StringField(required=True, default="encounter")

    identifier = ListField(DictField(identifer=StringField(required=True)))

    class_model = DictField(code=StringField(required=True))

