from odk.database.model_observation import ModelObservation,\
    ObservationSubject,ObservationEncounter,ObservationCode,ObservationValueQuantity
from graphene_mongo.types import MongoengineObjectType
import graphene

from odk.utils.base64 import base64_decode


class ObservationSubjectAttribute(graphene.InputObjectType):
    reference = graphene.String()


class ObservationEncounterAttribute(graphene.InputObjectType):
    reference = graphene.String()


class ObservationCodeAttribute(graphene.InputObjectType):
    text = graphene.String()


class ObservationValueQuantityAttribute(graphene.InputObjectType):
    value = graphene.Float()
    unit = graphene.String()
    code = graphene.String()


class ObservationAttribute:
    subject = ObservationSubjectAttribute()
    encounter = ObservationEncounterAttribute()
    code = ObservationCodeAttribute()
    valueQuantity = ObservationValueQuantityAttribute()
    pass


class Observation(MongoengineObjectType):

    class Meta:
        model = ModelObservation


class ObservationNode(MongoengineObjectType):

    class Meta:
        model = ModelObservation
        interfaces = (graphene.relay.Node, )


class CreateObservationInput(graphene.InputObjectType, ObservationAttribute):
    # path = graphene.String(required=True)
    pass


class CreateObservation(graphene.Mutation):
    observation = graphene.Field(lambda: ObservationNode)

    class Arguments:
        input = CreateObservationInput(required=True)

    def mutate(self, info, input):
        print(input)
        observation = ModelObservation(**input)
        observation.save()
        return CreateObservation(observation=observation)


class UpdateObservationInput(graphene.InputObjectType, ObservationAttribute):
    id = graphene.ID(required=True)
    pass


class UpdateObservation(graphene.Mutation):
    observation = graphene.Field(lambda: ObservationNode)

    class Arguments:
        input = UpdateObservationInput(required=True)

    def mutate(self, info, input):
        id_ = input.pop("id")
        # PatientNode:5e994f1b85c72524e35a5db2
        id_ = base64_decode(id_)[16:]
        print(id_)
        print("---更新的id为:", id_)
        observation = ModelObservation.objects.get(id=id_)
        observation.update(**input)
        observation.save()
        return UpdateObservation(observation=observation)
