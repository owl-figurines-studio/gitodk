from mongoengine import Document
from mongoengine import StringField, DictField, DateField, BooleanField, ListField


class ModelPatient(Document):
    meta = {"collection": "patient"}

    # resourceType = StringField(required=True, default="patient")
    #
    # active = BooleanField(required=True, default=True)
    #
    # gender = StringField(required=True) #, choices=['male', "female"])

    birthDate = StringField()
    #
    # name = ListField(StringField())
    #
    # address = ListField(StringField())
    # name = ListField(DictField(use=StringField(required=True, default="official"),
    #                            given=ListField(StringField()),
    #                            family=StringField()), required=True)
    #
    # address = ListField(DictField(use=StringField(required=True, default="official"),
    #                               city=StringField()))
