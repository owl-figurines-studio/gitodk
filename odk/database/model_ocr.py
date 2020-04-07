from mongoengine import Document
from mongoengine import StringField, ListField


class ModelOcr(Document):

    meta = {"collection": "ocr"}

    path = StringField(required=True)

    result = ListField(required=True)

