from mongoengine import Document
from mongoengine import StringField, ListField, ObjectIdField


class ModelOcr(Document):

    meta = {"collection": "ocr"}



    path = StringField(required=True)

    result = ListField(StringField())

