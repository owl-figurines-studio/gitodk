from odk.database.model_ocr import ModelOcr
from graphene_mongo.types import MongoengineObjectType
import graphene


class OcrAttribute:

    path = graphene.String()
    result = graphene.List(graphene.String)


class Ocr(MongoengineObjectType):

    class Meta:
        model = ModelOcr


class OcrNode(MongoengineObjectType):

    class Meta:
        model = ModelOcr
        interfaces = (graphene.relay.Node, )


class CreateOcrInput(graphene.InputObjectType, OcrAttribute):
    pass


class CreateOcr(graphene.Mutation):

    ocr = graphene.Field(lambda: OcrNode)

    class Arguments:
        input = CreateOcrInput(required=True)

    def mutate(self, info, input):
        ocr = ModelOcr(**input)
        ocr.save()
        return CreateOcr(ocr=ocr)


class UpdateOcr(graphene.Mutation):

    ocr = graphene.Field(lambda: OcrNode)

    class Arguments:
        input = CreateOcrInput(required=True)

    def mutate(self, _, input):
        path = input.pop("path")
        ocr = ModelOcr.objects.get(path=path)
        ocr.update(**input)
        ocr.save()
        return UpdateOcr(ocr=ocr)
