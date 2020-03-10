from odk.database.model_diabetes import ModelDiabetes
from graphene_mongo.types import MongoengineObjectType
import graphene
from datetime import datetime
import random

class DiabetesAttribute:
    id = graphene.String()
    _in_time = graphene.String()
    _utime = graphene.String()
    phone = graphene.String()
    # 年龄
    Age = graphene.Int()
    # 血糖
    Glucose = graphene.Float()
    # 血压 (mm Hg)
    BloodPressure = graphene.Float()
    # 胰岛素 2小时血清胰岛素（mu U / ml
    Insulin = graphene.Float()
    # 体重
    weight = graphene.Float()
    # 身高
    height = graphene.Float()
    # BMI：体重指数 （体重/身高）^2
    BMI = graphene.Float()

    outcome = graphene.Int()
    # 删除标记 {0:未删除,1:删除}
    delete_flag = graphene.Int()


class Diabetes(MongoengineObjectType):

    class Meta:
        model = ModelDiabetes


class DiabetesNode(MongoengineObjectType):

    class Meta:
        model = ModelDiabetes
        interfaces = (graphene.relay.Node, )

class CreateDiabetesInput(graphene.InputObjectType, DiabetesAttribute):
    pass


class CreateDiabetes(graphene.Mutation):
    diabetes = graphene.Field(lambda: DiabetesNode)

    class Arguments:
        input = CreateDiabetesInput(required=True)

    def mutate(self, info, input):
        # print(dict(input))
        if 'id' not in dict(input).keys():
            input['id']=str(random.random()*1000000000000000)
        if 'BMI' not in dict(input).keys():
            input['BMI'] = float(input['weight'])/(float(input['height'])**2)
        diabetes = ModelDiabetes(**input)
        diabetes.save()
        return CreateDiabetes(diabetes=diabetes)


class UpdateDiabetes(graphene.Mutation):

    diabetes = graphene.Field(lambda: DiabetesNode)

    class Arguments:
        input = CreateDiabetesInput(required=True)

    def mutate(self, info, input):
        phone = input.pop("phone")
        diabetes = ModelDiabetes.objects.get(phone=phone)
        diabetes._utime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        diabetes.update(**input)
        diabetes.save()
        return UpdateDiabetes(diabetes=diabetes)