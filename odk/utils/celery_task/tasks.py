import os
from celery import Celery

from config import config_constant
from ..ocr.ocr import rowOCR_path

# 运行命令如下
# celery -A odk.utils.celery_task.tasks worker -l debug -f logs/celery/celery_task.log &

# 文件的创建
log_path = "logs/celery/"
log_filename = "celery_task.log"
if not os.path.exists(log_path+log_filename):
    os.makedirs(log_path)
    os.mknod(log_filename)

# 创建celery
celery_app = Celery("odk_celery",
                    broker='redis://'+config_constant["REDIS_HOST"]\
                           + ':'+str(config_constant["REDIS_PORT"])\
                           + "/"+str(config_constant["REDIS_CELERY_DB"]),
                    backend='redis://'+config_constant["REDIS_HOST"]\
                           + ':'+str(config_constant["REDIS_PORT"])\
                           + "/"+str(config_constant["REDIS_CELERY_DB"]))


@celery_app.task()
def add_together(a, b):
    return a + b


@celery_app.task()
def celery_task_ocr(path):

    result = rowOCR_path(path)
    return {"ocr_result": result}


