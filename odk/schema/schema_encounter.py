from odk.database.model_encounter import ModelEncounter,ClassModel
from graphene_mongo.types import MongoengineObjectType
import graphene

from odk.utils.base64 import base64_decode


class ClassAttribute(graphene.InputObjectType):
    code = graphene.String()


class EncounterAttribute:
    classmodel = ClassAttribute()
    pass


class Encounter(MongoengineObjectType):

    class Meta:
        model = ModelEncounter


class ClassNode(MongoengineObjectType):
    class Meta:
        model = ClassModel
        interfaces = (graphene.relay.Node, )


class EncounterNode(MongoengineObjectType):

    class Meta:
        model = ModelEncounter
        interfaces = (graphene.relay.Node, )


class CreateEncounterInput(graphene.InputObjectType, EncounterAttribute):
    pass


class CreateEncounter(graphene.Mutation):
    encounter = graphene.Field(lambda: EncounterNode)

    class Arguments:
        input = CreateEncounterInput(required=True)

    def mutate(self, info, input):
        print("---input:", input)
        encounter = ModelEncounter(**input)
        encounter.save()
        return CreateEncounter(encounter=encounter)


class UpdateEncounterInput(graphene.InputObjectType, EncounterAttribute):
    id = graphene.ID(required=True)
    pass


class UpdateEncounter(graphene.Mutation):
    encounter = graphene.Field(lambda: EncounterNode)

    class Arguments:
        input = UpdateEncounterInput(required=True)

    def mutate(self, info, input):
        id_ = input.pop("id")
        # EncounterNode:5e994f1b85c72524e35a5db2
        id_ = base64_decode(id_)[14:]
        print("---更新的id为:", id_)
        encounter = ModelEncounter.objects.get(id=id_)
        encounter.update(**input)
        encounter.save()
        return UpdateEncounter(encounter=encounter)
