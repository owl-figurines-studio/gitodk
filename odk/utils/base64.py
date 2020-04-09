import base64


def base64_encode(path):
    """
    将path进行编码加密
    :param path: 需要加密的字符串
    :return: 编码加密后的path
    """
    # base64被编码的参数必须是二进制数据
    byte_path = path.encode("utf-8")
    # 进行base64编码
    based_byte_path = base64.b64encode(byte_path)
    # 将二进制装换成str类型
    based_str_all_path = based_byte_path.decode("utf-8")
    return based_str_all_path


def base64_decode(based_path):
    """
    将based_path进行解密
    :param based_path:需要解密的字符串
    :return: 解密后的字符串
    """
    # base64被解码的参数必须是二进制数据
    based_byte_path = based_path.encode("utf-8")
    # 进行base64解码
    byte_path = base64.b64decode(based_byte_path)
    # 将二进制装换成str类型
    path = byte_path.decode("utf-8")
    return path
