# @Time         : 19-1-8 上午10:36
# @Author       : Seven
# @File         : authentication.py
# @Description  : 用户认证模块

import logging
from functools import wraps

import redis
from django.conf import settings
from django.utils import timezone
from itsdangerous import SignatureExpired, BadSignature
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication


from apps.c.models import Admin
from apps.api.models import User

token_redis = redis.Redis.from_url(settings.TOKEN_REDIS_URL)


class Authentication(BaseAuthentication):
    """ 自写 token 认证类 """

    def authenticate(self, request):
        # 1. 验证是否带有token
        try:
            token = request.META['HTTP_AUTHORIZATION']
        except (ValueError, KeyError):
            raise exceptions.AuthenticationFailed({'retCode': 40000, 'retMsg': "参数错误 | Fail", 'err': 'TOKEN错误'})

        # 2. 验证token是否能解析
        s = Serializer(settings.SECRET_KEY)
        try:
            data = s.loads(token)
        except (SignatureExpired, BadSignature):
            logging.error('token Serializer error')
            raise exceptions.AuthenticationFailed({'retCode': 40003, 'retMsg': "参数错误 | Fail", 'err': 'TOKEN错误'})

        # # 3. redis验证token是否过期
        # redis_token = token_redis.get(data['user_id'])
        # if not redis_token or redis_token.decode() != token:
        #     logging.error('Token expired')
        #     raise exceptions.AuthenticationFailed({'retCode': 40005, 'retMsg': "参数错误 | Fail", 'err': 'TOKEN已过期'})

        # 4. 验证user是否存在
        try:
            user = User.objects.get(pk=data['user_id'], enabled=True)
        except (User.DoesNotExist, KeyError)as e:
            logging.error(e)
            raise exceptions.AuthenticationFailed({'retCode': 40003, 'retMsg': "参数错误 | Fail", 'err': 'TOKEN错误'})

        # 5. 接口访问log记录
        logging.debug(f"API interface access: "
                      f"user_id: {data['user_id']} "
                      f"method: {request.method} "
                      f"api: {request.META.get('PATH_INFO')} "
                      f"time: {timezone.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        return user, token


class AdminAuthentication(BaseAuthentication):
    """ 自写 token 认证类 """

    def authenticate(self, request):
        # 1. 验证是否带有token
        try:
            token = request.META['HTTP_AUTHORIZATION']
        except (ValueError, KeyError):
            raise exceptions.AuthenticationFailed({'retCode': 40000, 'retMsg': "参数错误 | Fail", 'err': 'TOKEN错误'})

        # 2. 验证token是否能解析
        s = Serializer(settings.SECRET_KEY)
        try:
            data = s.loads(token)
        except (SignatureExpired, BadSignature):
            logging.error('token Serializer error')
            raise exceptions.AuthenticationFailed({'retCode': 40003, 'retMsg': "参数错误 | Fail", 'err': 'TOKEN错误'})

        # # 3. redis验证token是否过期
        # redis_token = token_redis.get(data['user_id'])
        # if not redis_token or redis_token.decode() != token:
        #     logging.error('Token expired')
        #     raise exceptions.AuthenticationFailed({'retCode': 40005, 'retMsg': "参数错误 | Fail", 'err': 'TOKEN已过期'})

        # 4. 验证user是否存在
        try:
            admin = Admin.objects.get(pk=data['user_id'], enabled=True, deleted=False)
        except (Admin.DoesNotExist, KeyError)as e:
            logging.error(e)
            raise exceptions.AuthenticationFailed({'retCode': 40003, 'retMsg': "参数错误 | Fail", 'err': 'TOKEN错误'})

        # 5. 接口访问log记录
        logging.debug(f"API interface access: "
                      f"user_id: {data['user_id']} "
                      f"method: {request.method} "
                      f"api: {request.META.get('PATH_INFO')} "
                      f"time: {timezone.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        return admin, token


def login_view(func):
    """validate token 装饰器认证"""

    @wraps(func)
    def wrapper(view, request, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')
        if token:
            s = Serializer(settings.SECRET_KEY)
            try:
                data = s.loads(token)
            except (SignatureExpired, BadSignature):
                raise exceptions.AuthenticationFailed({'retCode': 40003, 'retMsg': "参数错误 | Fail", 'err': 'TOKEN错误'})
            try:
                user = Admin.objects.get(pk=data['user_id'], enabled=True, deleted=False)
            except (Admin.DoesNotExist, KeyError):
                raise exceptions.AuthenticationFailed({'retCode': 40003, 'retMsg': "参数错误 | Fail", 'err': 'TOKEN错误'})
            # 认证成功
            request.user = user
        else:
            raise exceptions.AuthenticationFailed({'retCode': 40003, 'retMsg': "参数错误 | Fail", 'err': 'TOKEN错误'})
        return func(view, request, **kwargs)

    return wrapper


def token_authenticate(token):
    """
    其他接口token验证
    :param token:
    :return:
    """
    s = Serializer(settings.SECRET_KEY)
    try:
        data = s.loads(token)
    except (SignatureExpired, BadSignature):
        return False
    try:
        user = Admin.objects.get(pk=data['user_id'], enabled=True, deleted=False)
    except (Admin.DoesNotExist, KeyError):
        user = User.objects.get(pk=data['user_id'], enabled=True)
    except (User.DoesNotExist, KeyError):
        return False
    return user


__all__ = ('Authentication', 'AdminAuthentication', 'login_view', 'token_authenticate')
