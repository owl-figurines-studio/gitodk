from mongoengine import Document
from mongoengine import StringField, IntField, DictField, DateTimeField, ReferenceField

from .model_patient import ModelPatient
from .model_encounter import ModelEncounter


class ModelObservation(Document):

    meta = {"collection": "observation"}

    resourceType = StringField(required=True, default="observation")

    meta_model = DictField(lastUpdated=DateTimeField(required=True),)

    subject = DictField(reference=ReferenceField(ModelPatient), required=True)

    encounter = DictField(reference=ReferenceField(ModelEncounter), required=True)

    code = DictField()

    valueQuantity = DictField()

    delete_flag = IntField(default=0, required=True)