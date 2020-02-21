from django.http import JsonResponse


class Code(object):

    ok = 200
    params_error = 400
    unauth = 401
    method_error = 405
    server_error = 500


def response(code=Code.ok, message='', data=None, kwargs=None):
    json_dict = {"code": code, "message": message, "data": data}
    if kwargs and isinstance(kwargs, dict) and kwargs.keys():
        json_dict.update(kwargs)

    return JsonResponse(json_dict)


def params_error(message='', data=None):
    return response(code=Code.params_error, message=message, data=data)


def unauth(message='', data=None):
    return response(code=Code.unauth, message=message, data=data)


def method_error(message='', data=None):
    return response(code=Code.method_error, message=message, data=data)


def server_error(message='', data=None):
    return response(code=Code.server_error, message=message, data=data)