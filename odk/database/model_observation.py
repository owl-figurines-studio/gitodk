from datetime import datetime

from mongoengine import Document
from mongoengine import StringField, IntField, DictField, DateTimeField, ReferenceField, DecimalField

from .observationcode import obs_code
from mongoengine import EmbeddedDocumentField, EmbeddedDocument


class ObservationMeta(EmbeddedDocument):
    lastUpdated = DateTimeField(default=datetime.now())


class ObservationSubject(EmbeddedDocument):
    reference = StringField()


class ObservationEncounter(EmbeddedDocument):
    reference = StringField()


class ObservationCode(EmbeddedDocument):
    text = StringField(choices=obs_code.keys())


class ObservationValueQuantity(EmbeddedDocument):
    value = DecimalField()
    unit = StringField()
    code = StringField()


class ModelObservation(Document):

    meta = {"collection": "observation"}

    resourceType = StringField(required=True, default="observation")

    metamodel = EmbeddedDocumentField(ObservationMeta)

    subject = EmbeddedDocumentField(ObservationSubject)

    encounter = EmbeddedDocumentField(ObservationEncounter)

    code = EmbeddedDocumentField(ObservationCode)

    valueQuantity = EmbeddedDocumentField(ObservationValueQuantity)


