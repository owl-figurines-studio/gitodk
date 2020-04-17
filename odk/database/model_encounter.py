from mongoengine import Document
from mongoengine import StringField
from mongoengine import EmbeddedDocumentField, EmbeddedDocument


class ClassModel(EmbeddedDocument):
    code = StringField()


class ModelEncounter(Document):
    meta = {"collection": "encounter"}

    resourceType = StringField(required=True, default="encounter")

    classmodel = EmbeddedDocumentField(ClassModel)

