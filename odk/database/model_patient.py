from mongoengine import Document
from mongoengine import StringField, IntField, DictField, DateField, BooleanField, ListField


class ModelPatient(Document):
    meta = {"collection": "patient"}

    resourceType = StringField(required=True, default="patient")

    active = BooleanField(required=True, default=True)

    gender = StringField(required=True, choices=['male', "female"])

    birthDate = DateField()

    name = ListField(DictField(use=StringField(required=True),
                               given=ListField(StringField()),
                               family=StringField()), required=True)

    address = ListField(DictField(use=StringField(required=True),
                                  city=StringField()))
