import base64


def base64_encode(all_path):
    # base64被编码的参数必须是二进制数据
    byte_all_path = all_path.encode("utf-8")
    # 进行base64编码
    based_byte_all_path = base64.b64encode(byte_all_path)
    # 将二进制装换成str类型
    based_str_all_path = based_byte_all_path.decode("utf-8")
    return based_str_all_path


def base64_decode(based_all_path):
    # base64被解码的参数必须是二进制数据
    based_byte_all_path = based_all_path.encode("utf-8")
    # 进行base64解码
    byte_all_path = base64.b64decode(based_byte_all_path)
    # 将二进制装换成str类型
    all_path = byte_all_path.decode("utf-8")
    return all_path
