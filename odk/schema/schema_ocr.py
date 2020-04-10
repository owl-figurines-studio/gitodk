from odk.database.model_ocr import ModelOcr
from graphene_mongo.types import MongoengineObjectType
import graphene

import os
from datetime import datetime

from odk.utils.ocr.ocr import rowOCR_path
from odk.utils.fastdfs.Images import save_image_path
from odk.utils.base64 import base64_decode


class OcrAttribute:
    pass
    # path = graphene.String()
    # result = graphene.List(graphene.String)
    # createtime = graphene.DateTime()
    # updatetime = graphene.DateTime()
    # imageurl = graphene.String()


class Ocr(MongoengineObjectType):

    class Meta:
        model = ModelOcr


class OcrNode(MongoengineObjectType):

    class Meta:
        model = ModelOcr
        interfaces = (graphene.relay.Node, )


class CreateOcrInput(graphene.InputObjectType, OcrAttribute):
    path = graphene.String(required=True)
    pass


class CreateOcr(graphene.Mutation):

    ocr = graphene.Field(lambda: OcrNode)

    class Arguments:
        input = CreateOcrInput(required=True)

    def mutate(self, info, input):
        """
        createocr的处理函数,
        :param info: 一般不使用
        :param input:
        :return:
        """
        based_path = input['path']
        path = base64_decode(based_path)
        now = datetime.now()
        input['createtime'] = now
        input['updatetime'] = now
        if os.path.exists(path):
            url = save_image_path(path)
            input['imageurl'] = url
            lst = rowOCR_path(path)
            input["result"] = lst
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
        id_ = base64_decode(id_)[8:]
        print("---更新的id为:", id_)
        ocr = ModelOcr.objects.get(id=id_)
        based_path = ocr['path']
        path = base64_decode(based_path)
        print("---path", path)
        if os.path.exists(path):
            lst = rowOCR_path(path)
            url = save_image_path(path)
            now = datetime.now()
            new_input = {"result": lst,
                         "updatetime": now,
                         "imageurl": url}
            ocr.update(**new_input)
            ocr.save()
        return UpdateOcr(ocr=ocr)
