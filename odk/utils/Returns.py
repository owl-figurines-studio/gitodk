from odk.utils.ErrorMsg import ERRORMSG


def base_ret_data(code, message_http, **kwargs):
    return {'code': code,
            'message': message_http,
            'data': {**kwargs}
            }, code


def response_data(verify_state_code, code=200, message_http="请求成功", **kwargs):
    return base_ret_data(code, message_http,
                         userStateCode=verify_state_code,
                         userStateMessage=ERRORMSG[verify_state_code],
                         **kwargs)


