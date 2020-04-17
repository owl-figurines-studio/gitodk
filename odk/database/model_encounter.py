from mongoengine import Document
from mongoengine import StringField, DictField, ListField
from mongoengine import EmbeddedDocumentField, EmbeddedDocument


class ClassModel(EmbeddedDocument):
    code = StringField()


class ModelEncounter(Document):
    meta = {"collection": "encounter"}

    resourceType = StringField(required=True, default="encounter")

    classmodel = EmbeddedDocumentField(ClassModel)

