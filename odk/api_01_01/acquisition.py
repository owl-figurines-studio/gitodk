from flask import request
import random
import base64
import io
from PIL import Image
import os
import cv2

from . import api
from odk.utils.fastdfs.Images import save_Image
from odk.utils.Returns import ret_data
from odk.utils.ocr import ocr
from odk import mongodb


@api.route('/acquisition/imagebase64', methods=['POST'])
def test_image_base64():
    xxx = request.form['imageBase64']
    # print(xxx)

    img_b64decode = base64.b64decode(xxx)  # base64解码

    image = io.BytesIO(img_b64decode)
    random_str = "%06d.jpg" % random.randint(0, 999999)
    img = Image.open(image)
    img = img.convert('RGB')
    img.filename = random_str
    return save_Image(img)


@api.route('/acquisition/image', methods=['POST'])
def test_image():
    xxx = request.files
    try:
        file = xxx['UploadImage']
        print(file)
    except KeyError as e:
        return ret_data(200, '请求成功', 2007)
    return save_Image(file)


@api.route('/acquisition/uploadimage', methods=['POST'])
def acquisition_upload_ocr():
    xxx = request.files
    try:
        file = xxx['UploadImage']
        # print(file)
    except KeyError as e:
        return ret_data(200, '请求成功', 2007)
    filename = file.filename
    dir_path = "./odk/images/"
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
    path = dir_path + filename  # 文件路径
    file.save(path)
    pwd = os.getcwd()
    # print("pwd:",pwd)
    # print("path:",path)

    all_path = pwd+path[1:]
    # print(all_path)
    bytes_path = all_path.encode("utf-8")
    str_url = base64.b64encode(bytes_path)  # 被编码的参数必须是二进制数据
    print(str_url)
    str_url = str_url.decode("utf-8")
    mongodb.ocr.insert_one({"path": str_url,"result": []})
    return ret_data(200, '请求成功', 1012, id=str_url)


@api.route('/acquisition/ocr', methods=['POST'])
def acquisition_getocr():
    get_path = request.form['id']
    all_path = base64.b64decode(get_path.encode('utf-8')).decode("utf-8")
    mongo_path = mongodb.ocr.find_one({"path": get_path})
    if mongo_path and mongo_path['result'] == []:
        img = cv2.imread(all_path, 0)
        lst = ocr.rowOCR(img)
        mongodb.ocr.update_one({"path": get_path}, {"$set": {"result": lst}})
        # if os.path.exists(all_path):  # 如果文件存在
        #    # 删除文件，可使用以下两种方法。
        #     os.remove(all_path)
    else:
        lst = mongo_path['result']
    return ret_data(200, '请求成功', 1011, result=lst)

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
