from odk.database.model_patient import ModelPatient
from graphene_mongo.types import MongoengineObjectType
from graphene import String, List, Boolean, Date, ObjectType, InputObjectType, ID
from graphene.relay import Node
from graphene import Mutation
from graphene import Field

import os
from datetime import datetime

from odk.utils.ocr.ocr import rowOCR_path
from odk.utils.fastdfs.Images import save_image_path
from odk.utils.base64 import base64_decode


class PatientAttribute:
    # gender = String()
    birthday = String()
    # name = List(String)
    # address = List(String)
    # resourceType = String()
    # active = Boolean()


class Patient(MongoengineObjectType):

    class Meta:
        model = ModelPatient


class PatientNode(MongoengineObjectType):

    class Meta:
        model = ModelPatient
        interfaces = (Node, )


class CreatePatientInput(InputObjectType, PatientAttribute):
    # path = String(required=True)
    pass


class CreatePatient(Mutation):

    pat = Field(lambda: PatientNode)

    class Arguments:
        input = CreatePatientInput(required=True)

    def mutate(self, info, input):
        # str_p = '2019-01-30'
        # dateTime_p = datetime.strptime(str_p, '%Y-%m-%d')
        # print(dateTime_p)
        # must_keys = []

        # model_data = dict()
        print(input)
        pat = ModelPatient(**input)
        pat.save()
        return CreatePatient(pat=pat)


