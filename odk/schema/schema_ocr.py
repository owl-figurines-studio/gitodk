from odk.database.model_ocr import ModelOcr
from graphene_mongo.types import MongoengineObjectType
import graphene

import cv2, base64
import os

from odk.utils.ocr.ocr import rowOCR


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
        path = input['path']
        all_path = base64.b64decode(path.encode('utf-8')).decode("utf-8")
        if os.path.exists(all_path):
            img = cv2.imread(all_path, 0)
            lst = rowOCR(img)
            input["result"] = lst

            # os.remove(all_path)
        ocr = ModelOcr(**input)
        ocr.save()

        return CreateOcr(ocr=ocr)


class UpdateOcrInput(graphene.InputObjectType, OcrAttribute):
    id = graphene.ID(required=True)
    pass


class UpdateOcr(graphene.Mutation):

    ocr = graphene.Field(lambda: OcrNode)

    class Arguments:
        input = UpdateOcrInput(required=True)

    def mutate(self, info, input):
        id_ = input.pop("id")
        id_ = base64.b64decode(id_.encode('utf-8')).decode("utf-8")[8:]
        print(id_)
        ocr = ModelOcr.objects.get(id=id_)
        path = ocr['path']
        # print(path)
        all_path = base64.b64decode(path.encode('utf-8')).decode("utf-8")
        # print(all_path)
        if os.path.exists(all_path):
            img = cv2.imread(all_path, 0)
            lst = rowOCR(img)
            new_input = {"result": lst}
            # new_input["result"] = lst
            # print(input)
            # os.remove(all_path)

            # print(ocr)
            ocr.update(**new_input)
            ocr.save()


        # ocr.update(**input)
        # ocr.save()
        return UpdateOcr(ocr=ocr)
