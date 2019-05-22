# @Time        : 2019-05-16 15:25
# @Author      : Seven
# @File        : exceptions.py
# @Description : 验证类 全局异常处理

from rest_framework.serializers import ValidationError
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        if isinstance(exc, ValidationError) and not response.data.get('retMsg'):
            for k, v in response.data.items():
                try:
                    response.data['retMsg'] = str(v[0]).replace(' ', '')
                except IndexError:
                    response.data['retMsg'] = v
                response.data.pop(k)
                break
        if 'detail' in response.data.keys():
            response.data['retMsg'] = 'Not found'
            response.data.pop('detail')
        response.data['retCode'] = response.status_code * 100
    return response
