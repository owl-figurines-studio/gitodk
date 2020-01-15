from odk import db
import datetime




class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer,primary_key=True)
    # 逻辑删除
    is_deleted = db.Column(db.Boolean, default=False)
    # 创建时间
    createtime = db.Column(db.DateTime, default=datetime.datetime.now)
    # 更新时间
    updatetime = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

# 普通用户表
class User(BaseModel):
    __tablename__ ='users'
    id = db.Column(db.Integer,primary_key=True)

    # 普通用户的手机号
    user_phone = db.Column(db.String(11),unique=True)
    # 性别
    gender = db.Column(db.String(11),default='未定义')
