import sys
sys.path.append("..")

from mongoengine import Document
from mongoengine import (StringField, IntField,FloatField)
from datetime import datetime


class ModelDiabetes(Document):

    meta = {"collection": "diabetes"}

    id = StringField(primary_key=True)
    _in_time = StringField(required=True, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    _utime = StringField(required=True, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # 用于查询
    phone = StringField(required=True)
    # 年龄
    Age = IntField(required=True)
    # 血糖
    Glucose = FloatField(required=True)
    # 血压 (mm Hg)
    BloodPressure = FloatField(required=True)
    # 胰岛素 2小时血清胰岛素（mu U / ml
    Insulin = FloatField(required=True)
    # 体重
    weight = FloatField(required=True)
    # 身高
    height = FloatField(required=True)
    # BMI：体重指数 （体重/身高）^2
    BMI = FloatField(required=True, default=0)
    # 是否得病{-1:未确定,0:无病,1:有病}
    outcome=IntField(default=-1,required=True)
    # 删除标记 {0:未删除,1:删除}
    delete_flag = IntField(default=0, required=True)

