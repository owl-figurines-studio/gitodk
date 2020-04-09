# 原生包
import random
import base64
import io
from datetime import datetime
import os

# 第三方
from flask import request
from PIL import Image

# 自己写
from . import api
from odk.utils.fastdfs.Images import save_Image
from odk.utils.Returns import ret_data
from odk.utils.ocr.ocr import rowOCR_path
from odk.utils.fastdfs.Images import save_image_url
from odk.utils.base64 import base64_decode, base64_encode
from odk.database.model_ocr import ModelOcr


@api.route('/acquisition/imagebase64', methods=['POST'])
def test_image_base64():
    xxx = request.form['imageBase64']
    img_b64decode = base64.b64decode(xxx)  # base64解码
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
    xxx = request.files
    try:
        file = xxx['UploadImage']
    except KeyError as e:
        return ret_data(200, '请求成功', 2007)
    all_path, url = save_image_url(file)
    based_all_path = base64_encode(all_path)
    now = datetime.now()
    model_msg = {"path": based_all_path,
                 "createtime": now,
                 "updatetime": now,
                 "imageurl": url}
    ocr_model = ModelOcr(**model_msg)
    ocr_model.save()
    return_msg = {"id": str(ocr_model.id),
                  "image_url": url}
    return ret_data(200, '请求成功', 1012, **return_msg)


@api.route('/acquisition/ocr', methods=['POST'])
def acquisition_getocr():
    request_data = request.form.to_dict()
    ocr_id = request_data['id']
    update = False
    if "update" in request_data.keys() and request_data["update"] == "true":
        update = True
    ocr_model = ModelOcr.objects.get(id=ocr_id)
    get_path = ocr_model["path"]
    all_path = base64_decode(get_path)
    if os.path.exists(all_path):
        if update or ocr_model['result'] == []:
            lst = rowOCR_path(all_path)
            # if os.path.exists(all_path):  # 如果文件存在
            #    # 删除文件，可使用以下两种方法。
            #     os.remove(all_path)
            ocr_model.update(result=lst, updatetime=datetime.now())
            ocr_model.save()
            return ret_data(200, '请求成功', 1011, result=lst)
        return ret_data(200, '请求成功', 2014, result=ocr_model['result'])
    return ret_data(200, '请求成功', 2013)

# from odk import celery
# @celery.task()
# def add_together(a, b):
#     return a + b
#
# @api.route('/acquisition/asyocr', methods=['POST'])
# def acquisition_asyocr():
#     a = request.form['a']
#     b = request.form['b']
#     ret = add_together.delay(a,b)
#     print(ret)
#     return ret_data(200,'请求成功',1000)
