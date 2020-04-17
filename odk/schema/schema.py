import graphene
from graphene_mongo.fields import MongoengineConnectionField

from odk.schema import schema_user
from odk.schema import schema_diabetes
from odk.schema import schema_ocr
from odk.schema import schema_patient
from odk.database.base import connect # 必要,不知道为啥

from odk.database.model_patient import ModelPatient

class Query(graphene.ObjectType):

    node = graphene.relay.Node.Field()
    users = MongoengineConnectionField(schema_user.UserNode)
    diabetes = MongoengineConnectionField(schema_diabetes.DiabetesNode)
    ocr = MongoengineConnectionField(schema_ocr.OcrNode)
    patient = MongoengineConnectionField(schema_patient.PatientNode)
    # patient_all = graphene.List(ModelPatient)
    #
    # def resolve_users(self, info):
    #     return list(ModelPatient.objects.all())

class Mutation(graphene.ObjectType):
    create_user = schema_user.CreateUser.Field()
    create_diabetes = schema_diabetes.CreateDiabetes.Field()
    create_ocr = schema_ocr.CreateOcr.Field()
    create_patient = schema_patient.CreatePatient.Field()

    update_user = schema_user.UpdateUser.Field()
    update_diabetes = schema_diabetes.UpdateDiabetes.Field()
    update_ocr = schema_ocr.UpdateOcr.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)