from odk.schema import schema_user
from odk.schema import schema_diabetes
import graphene
from graphene_mongo.fields import MongoengineConnectionField
from odk.database.base import connect

class Query(graphene.ObjectType):

    node = graphene.relay.Node.Field()

    users = MongoengineConnectionField(schema_user.UserNode)

    diabetes = MongoengineConnectionField(schema_diabetes.DiabetesNode)

class Mutation(graphene.ObjectType):
    create_user = schema_user.CreateUser.Field()
    create_diabetes = schema_diabetes.CreateDiabetes.Field()

    update_user = schema_user.UpdateUser.Field()
    update_diabetes = schema_diabetes.UpdateDiabetes.Field()



schema = graphene.Schema(query=Query, mutation=Mutation)