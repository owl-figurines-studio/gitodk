import os

from odk import fastdfs_client
from odk.utils.Returns import ret_data

def save_Image(file):
    '''
    用来保存文件上传
    :param file: request.files读取的对象
    :return:
    '''
    filename = file.filename
    path = "./odk/images/"+filename  # 文件路径
    file.save(path)

    ret = fastdfs_client.upload_by_filename(path)
    print(ret)

    if os.path.exists(path):  # 如果文件存在
        # 删除文件，可使用以下两种方法。
        os.remove(path)
        # os.unlink(path)
    else:
        print('no such file:%s' % file.filename)  # 则返回文件不存在
    if ret['Status']=='Upload successed.':
        url = 'http://'+ret['Storage IP']+':8888/'+ret['Remote file_id']
        return ret_data(200,'请求成功',1002,url=url)
    return ret_data(200, '请求成功', 2006)