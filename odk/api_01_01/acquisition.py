# 原生包
import random
import base64
import io
from datetime import datetime

# 第三方
from flask import request
from PIL import Image

# 自己写
from . import api
from odk.utils.fastdfs.Images import save_Image
from odk.utils.Returns import response_data
from odk.utils.ocr.ocr import rowOCR_path
from odk.utils.fastdfs.Images import save_image_local, save_image_path
from odk.utils.base64 import base64_decode, base64_encode
from odk.database.model_ocr import ModelOcr
from odk.utils.celery_task.tasks import add_together,celery_task_ocr


@api.route('/acquisition/imagebase64', methods=['POST'])
def test_image_base64():
    """
    将经过base64编码过的图片存储到fastdfs上
    :return: 图片的url地址
    """
    based_image = request.form['imageBase64']
    img_b64decode = base64.b64decode(based_image)  # base64解码
    image = io.BytesIO(img_b64decode)
    # 随机的文件名
    random_str = "%06d.jpg" % random.randint(0, 999999)
    img = Image.open(image)
    img = img.convert('RGB')
    img.filename = random_str
    return save_Image(img)


# @api.route('/acquisition/image', methods=['POST'])
# def test_image():
#     xxx = request.files
#     try:
#         file = xxx['UploadImage']
#         print(file)
#     except KeyError as e:
#         return ret_data(200, '请求成功', 2007)
#     return save_Image(file)


@api.route('/acquisition/uploadimage', methods=['POST'])
def acquisition_upload_ocr():
    """
    上传识别的图片
    :return: 经过base64加密的存储路径
    """
    files = request.files
    try:
        file = files['UploadImage']
    except KeyError:
        return response_data(2007)
    path = save_image_local(file)
    based_path = base64_encode(path)
    return response_data(1012, path=based_path)


@api.route('/acquisition/ocr', methods=['POST'])
def acquisition_getocr():
    """
    获取到path,进行图像识别
    :return: 模型的id,fastdfs的url地址,识别的结果
    """
    request_data = request.form.to_dict()
    if "path" not in request_data.keys():
        return response_data(2015)
    based_path = request_data['path']
    path = base64_decode(based_path)
    result_list = rowOCR_path(path)
    url = save_image_path(path)
    now = datetime.now()
    model_msg = {"path": based_path,
                 "createtime": now,
                 "updatetime": now,
                 "imageurl": url,
                 "result": result_list}
    ocr_model = ModelOcr(**model_msg)
    ocr_model.save()
    return_msg = {"id": str(ocr_model.id),
                  "image_url": url,
                  "result": result_list}
    return response_data(1012, **return_msg)


@api.route('/acquisition/asyocr', methods=['POST'])
def acquisition_asyocr():
    files = request.files
    try:
        file = files['UploadImage']
    except KeyError:
        return response_data(2007)
    path = save_image_local(file)
    task = celery_task_ocr.delay(path)
    print("---task.id:", task.id)
    return response_data(1000, task_id=task.id)


@api.route('/acquisition/asyocr_result', methods=['POST'])
def acquisition_asyocr_result():
    task_id = request.form['task_id']
    task = celery_task_ocr.AsyncResult(task_id)
    response = {"state": task.state}
    if task.state == 'SUCCESS':
        response['result'] = task.info["ocr_result"]
    return response_data(1011, **response)


@api.route('/acquisition/add', methods=['POST'])
def acquisition_add():
    a = request.form['a']
    b = request.form['b']
    task = add_together.delay(int(a), int(b))
    print("---task.id:", task.id)
    return response_data(1000, task_id=task.id)


@api.route('/acquisition/add_result', methods=['POST'])
def acquisition_add_result():
    task_id = request.form['task_id']
    task = add_together.AsyncResult(task_id)
    if task.state == 'PENDING':
        #  job did not start yet
        response = {
            'state': task.state,
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'result': task.info
        }
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
        }
    return response_data(1011, **response)