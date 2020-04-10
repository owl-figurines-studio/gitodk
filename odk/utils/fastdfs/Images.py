import os

from odk import fastdfs_client
from odk.utils.Returns import response_data


def save_image_path(path):
    """
    将路径对应的文件存入fastdfs中
    :param path: 文件路径+文件名
    :return: fastdfs的url地址,存储失败则为''
    """
    ret = fastdfs_client.upload_by_filename(path)
    print("---fastdfs 返回:", ret)
    # if os.path.exists(path):  # 如果文件存在
    #     # 删除文件，可使用以下两种方法。
    #     os.remove(path)
    #     # os.unlink(path)
    # else:
    #     print('no such file:%s' % file.filename)  # 则返回文件不存在
    if ret['Status'] == 'Upload successed.':
        url = 'http://' + ret['Storage IP'] + ':8888/' + ret['Remote file_id']
        print("---fastdfs 得到的url:", url)
        return url
    return ''


def save_image_local(file):
    """
    将表单发来的文件,存到本地
    :param file: request.file类型
    :return: 文件所在的相对路径+文件名
    """
    filename = file.filename
    dir_path = "./odk/images/"
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
    path = dir_path + filename  # 文件路径
    file.save(path)
    return path


def save_image_url(file):
    """
    将表单发来的文件,存到fastdfs中
    :param file: request.file类型
    :return: fastdfs的url地址,存储失败则为''
    """
    path = save_image_local(file)
    return save_image_path(path)


def save_Image(file):
    """
    用来保存文件上传
    :param file: request.files读取的对象
    :return:
    """
    url = save_image_url(file)
    if url == '':
        return response_data(2006)
    return response_data(1002, url=url)
