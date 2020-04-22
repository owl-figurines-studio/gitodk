from odk.database.model_patient import ModelPatient
from graphene_mongo.types import MongoengineObjectType
import graphene

import os
from datetime import datetime

from odk.utils.ocr.ocr import rowOCR_path
from odk.utils.fastdfs.Images import save_image_path
from odk.utils.base64 import base64_decode
# InputObjectType


class PatientAttribute:
    birthDate = graphene.String()
    gender = graphene.String()
    name = graphene.List(graphene.String)
    telecom = graphene.String()

    # code = SubInput()
    # code = graphene.List(SubInput)
    pass


class Patient(MongoengineObjectType):

    class Meta:
        model = ModelPatient


class PatientNode(MongoengineObjectType):

    class Meta:
        model = ModelPatient
        interfaces = (graphene.relay.Node, )


class CreatePatientInput(graphene.InputObjectType, PatientAttribute):
    # path = graphene.String(required=True)
    pass


class CreatePatient(graphene.Mutation):

    patient = graphene.Field(lambda: PatientNode)

    class Arguments:
        input = CreatePatientInput(required=True)

    def mutate(self, info, input):
        print(input)
        patient = ModelPatient(**input)
        patient.save()
        return CreatePatient(patient=patient)


class UpdatePatientInput(graphene.InputObjectType, PatientAttribute):
    id = graphene.ID(required=True)
    pass


class UpdatePatient(graphene.Mutation):
    patient = graphene.Field(lambda: PatientNode)

    class Arguments:
        input = UpdatePatientInput(required=True)

    def mutate(self, info, input):
        id_ = input.pop("id")
        # PatientNode:5e994f1b85c72524e35a5db2
        id_ = base64_decode(id_)[12:]
        print(id_)
        print("---更新的id为:", id_)
        patient = ModelPatient.objects.get(id=id_)
        patient.update(**input)
        patient.save()
        patient = ModelPatient.objects.get(id=id_)
        return UpdatePatient(patient=patient)
