from rest_framework import status
from rest_framework.response import Response


def response(*args, data=None, err=None):
    response_data = {'retCode': args[0],
                     'retMsg': args[1]}
    if data is not None:
        response_data['data'] = data
    if err is not None:
        response_data['err'] = err
    return Response(response_data, status=status.HTTP_200_OK)


def success_response(data=None, kwargs: dict = None):
    response_data = {'retCode': 0,
                     'retMsg': u"成功 | Success"}
    if data is not None:
        response_data['data'] = data
    if kwargs:
        response_data.update(kwargs)

    if isinstance(data, Response):
        results = data.data.pop('results')
        data.data.update(response_data)
        data.data['data'] = results
        return data
    return Response(response_data, status=status.HTTP_200_OK)


def server_error_response(err=None):
    response_data = {'retCode': 50000,
                     'retMsg': u"服务器错误 | Fail"}
    if err:
        response_data['data'] = err
    return Response(response_data, status=status.HTTP_200_OK)


def parameter_error_response(err=None, kwargs: dict = None):
    response_data = {'retCode': 40000,
                     'retMsg': u"参数错误 | Fail"}
    if err is not None:
        response_data['err'] = err
    if kwargs:
        response_data.update(kwargs)
    return Response(response_data, status=status.HTTP_200_OK)
