from flask import request
import random
import base64
import io
from PIL import Image

from . import api
from odk.utils.fastdfs.Images import save_Image

@api.route('/acquisition/image',methods=['POST'])
def test_image_base64():
    xxx = request.form['imageBase64']
    print(xxx)

    img_b64decode = base64.b64decode(xxx)  # base64解码

    image = io.BytesIO(img_b64decode)
    random_str = "%06d.jpg" % random.randint(0, 999999)
    img = Image.open(image)
    img = img.convert('RGB')
    img.filename = random_str
    return save_Image(img)