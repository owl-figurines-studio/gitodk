from odk.database.model_observation import ModelObservation,\
    ObservationSubject,ObservationEncounter,ObservationCode,ObservationValueQuantity
from graphene_mongo.types import MongoengineObjectType
import graphene

from odk.utils.base64 import base64_decode


class ObservationSubjectAttribute(graphene.InputObjectType):
    reference = graphene.String()


class ObservationSubjectNode(MongoengineObjectType):
    class Meta:
        model = ObservationSubject
        interfaces = (graphene.relay.Node, )


class ObservationEncounterAttribute(graphene.InputObjectType):
    reference = graphene.String()


class ObservationEncounterNode(MongoengineObjectType):
    class Meta:
        model = ObservationEncounter
        interfaces = (graphene.relay.Node, )


class ObservationCodeAttribute(graphene.InputObjectType):
    text = graphene.String()


class ObservationCodeNode(MongoengineObjectType):
    class Meta:
        model = ObservationCode
        interfaces = (graphene.relay.Node, )


class ObservationValueQuantityAttribute(graphene.InputObjectType):
    value = graphene.Float()
    unit = graphene.String()
    code = graphene.String()


class ObservationValueQuantityNode(MongoengineObjectType):
    class Meta:
        model = ObservationValueQuantity
        interfaces = (graphene.relay.Node, )


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
    pass


class CreateObservation(graphene.Mutation):
    observation = graphene.Field(lambda: ObservationNode)

    class Arguments:
        input = CreateObservationInput(required=True)

    def mutate(self, info, input):
        print("---input:", input)
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
        # ObservationNode:5e994f1b85c72524e35a5db2
        id_ = base64_decode(id_)[16:]
        print("---更新的id为:", id_)
        observation = ModelObservation.objects.get(id=id_)
        observation.update(**input)
        observation.save()
        return UpdateObservation(observation=observation)
