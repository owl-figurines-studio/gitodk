import graphene
from graphene_mongo.fields import MongoengineConnectionField

from odk.schema import schema_user
from odk.schema import schema_diabetes
from odk.schema import schema_ocr
from odk.schema import schema_patient
from odk.schema import schema_encounter
from odk.schema import schema_observation
from odk.database.base import connect # 必要,不知道为啥


class Query(graphene.ObjectType):

    node = graphene.relay.Node.Field()
    users = MongoengineConnectionField(schema_user.UserNode)
    diabetes = MongoengineConnectionField(schema_diabetes.DiabetesNode)
    ocr = MongoengineConnectionField(schema_ocr.OcrNode)
    patient = MongoengineConnectionField(schema_patient.PatientNode)
    encounter = MongoengineConnectionField(schema_encounter.EncounterNode)
    encounterclass = MongoengineConnectionField(schema_encounter.ClassNode)
    observation = MongoengineConnectionField(schema_observation.ObservationNode)

class Mutation(graphene.ObjectType):
    create_user = schema_user.CreateUser.Field()
    create_diabetes = schema_diabetes.CreateDiabetes.Field()
    create_ocr = schema_ocr.CreateOcr.Field()
    create_patient = schema_patient.CreatePatient.Field()
    create_encounter = schema_encounter.CreateEncounter.Field()
    create_observation = schema_observation.CreateObservation.Field()

    update_user = schema_user.UpdateUser.Field()
    update_diabetes = schema_diabetes.UpdateDiabetes.Field()
    update_ocr = schema_ocr.UpdateOcr.Field()
    update_patient = schema_patient.UpdatePatient.Field()
    update_encounter = schema_encounter.UpdateEncounter.Field()
    update_observation = schema_observation.UpdateObservation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
