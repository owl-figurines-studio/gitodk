from mongoengine import Document
from mongoengine import StringField, DictField, DateField, BooleanField, ListField, EmbeddedDocumentField,EmbeddedDocumentListField, EmbeddedDocument


class ModelPatient(Document):
    meta = {"collection": "patient"}

    resourceType = StringField(required=True, default="patient")

    active = BooleanField(required=True, default=True)

    gender = StringField(required=True, choices=['male', "female"])

    birthDate = StringField()

    name = ListField(StringField())

    telecom = StringField()