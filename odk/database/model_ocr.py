from mongoengine import Document
from mongoengine import StringField, ListField, DateTimeField


class ModelOcr(Document):

    meta = {"collection": "ocr"}

    path = StringField(required=True)

    result = ListField(StringField())

    createtime = DateTimeField(required=True)

    updatetime = DateTimeField(required=True)

    imageurl = StringField(required=True)

