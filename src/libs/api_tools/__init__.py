# @Time        : 2019-04-25 17:18
# @Author      : Seven
# @File        : __init__.py.py
# @Description : api tools

from .api_response import response, success_response, server_error_response, parameter_error_response
from .authentication import Authentication, AdminAuthentication, login_view, token_authenticate
from .pagination import StandardResultsSetPagination, StandardResultsSetLimitOffsetPagination
from .runtime_log import runtime
from .token import get_token, token_expired, get_key, get_key_data
from .datetime_tools import str_time_to_datetime, TimeStampField


def str_to_bool(bool_str):
    """
    转换 bool
    :param bool_str: bool 的字符串
    :return: True/False
    """
    return True if bool_str.lower() == 'true' else False


__all__ = [
    'str_to_bool', 'runtime',
    'response', 'success_response', 'server_error_response', 'parameter_error_response',
    'Authentication', 'AdminAuthentication', 'login_view', 'token_authenticate',
    'StandardResultsSetPagination', 'StandardResultsSetLimitOffsetPagination',
    'get_token', 'token_expired', 'get_key', 'get_key_data', 'str_time_to_datetime',
    'TimeStampField',
]
