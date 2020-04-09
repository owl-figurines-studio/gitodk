# 第三方包
from flask import Blueprint

# 蓝图设置
api = Blueprint('api', __name__)

# 自己写的方法
from . import users
from . import patients
from . import diabetes
from . import acquisition




