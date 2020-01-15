from .ErrorMsg import ERRORMSG
def base_ret_data(code,messagehttp,**kwargs):
    return {'code': code,
            'message': messagehttp,
            'data': {**kwargs}
            }, code



def ret_data(code,messagehttp,verifyStateCode,**kwargs):
    return base_ret_data(code, messagehttp,
                         userStateCode=verifyStateCode,
                         **kwargs)

# def ret_user_data(code,messagehttp,userStateCode,**kwargs):
#     return base_ret_data(code, messagehttp,
#                          userStateCode=userStateCode,
#                          **kwargs)
#
#
# def ret_upload_data(code,messagehttp,uploadStateCode,**kwargs):
#     return base_ret_data(code, messagehttp,
#                          uploadStateCode=uploadStateCode,
#                          **kwargs)

