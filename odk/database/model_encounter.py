from mongoengine import Document
from mongoengine import StringField, DictField, ListField


class ModelEncounter(Document):
    meta = {"collection": "encounter"}

    resourceType = StringField(required=True, default="encounter")

    class_model = DictField(code=StringField(required=True))

