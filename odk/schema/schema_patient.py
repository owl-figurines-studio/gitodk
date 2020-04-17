from odk.database.model_patient import ModelPatient
from graphene_mongo.types import MongoengineObjectType
import graphene

from odk.database.model_patient import SubInput as SubModel
import os
from datetime import datetime

from odk.utils.ocr.ocr import rowOCR_path
from odk.utils.fastdfs.Images import save_image_path
from odk.utils.base64 import base64_decode
# InputObjectType
class SubInput:
    subject = graphene.String()

class PatientAttribute:
    birthDate = graphene.String()
    code = SubInput()
    test = SubInput()
    # code = SubInput()
    # code = graphene.List(SubInput)
    pass
    # path = graphene.String()
    # result = graphene.List(graphene.String)
    # createtime = graphene.DateTime()
    # updatetime = graphene.DateTime()
    # imageurl = graphene.String()


class Patient(MongoengineObjectType):

    class Meta:
        model = ModelPatient

class SubInputNode(MongoengineObjectType):
    class Meta:
        model = SubModel
        interfaces = (graphene.relay.Node,)



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
        """
        createocr的处理函数,
        :param info: 一般不使用
        :param input:
        :return:
        """
        # print(input)
        # lst, input['code'] = input['code'], list()
        # for i in lst:
        #     input['code'].append(dict(i))
        print(input)
        patient = ModelPatient(**input)
        patient.save()
        return CreatePatient(patient=patient)


# class UpdateOcrInput(graphene.InputObjectType, OcrAttribute):
#     id = graphene.ID(required=True)
#     pass
#
#
# class UpdateOcr(graphene.Mutation):
#
#     ocr = graphene.Field(lambda: OcrNode)
#
#     class Arguments:
#         input = UpdateOcrInput(required=True)
#
#     def mutate(self, info, input):
#         id_ = input.pop("id")
#         id_ = base64_decode(id_)[8:]
#         print("---更新的id为:", id_)
#         ocr = ModelOcr.objects.get(id=id_)
#         based_path = ocr['path']
#         path = base64_decode(based_path)
#         print("---path", path)
#         if os.path.exists(path):
#             lst = rowOCR_path(path)
#             url = save_image_path(path)
#             now = datetime.now()
#             new_input = {"result": lst,
#                          "updatetime": now,
#                          "imageurl": url}
#             ocr.update(**new_input)
#             ocr.save()
#         return UpdateOcr(ocr=ocr)
