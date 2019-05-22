# @Time         : 19-1-8 上午10:47
# @Author       : Seven
# @File         : token.py
# @Description  : 生成token
import redis
from django.conf import settings
from itsdangerous import SignatureExpired, BadSignature
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

token_redis = redis.Redis.from_url(settings.TOKEN_REDIS_URL)


def get_token(user, expiration=10 * 3 * 24 * 60 * 60):
    """
    生成token,存入redis
    :param user: user obj
    :param expiration: limit time
    :return: token
    """
    # 使用settings.SECRET_KEY作为密钥
    ser = Serializer(settings.SECRET_KEY, expires_in=expiration)
    user_info = dict(user_id=str(user.pk))
    token = ser.dumps(user_info).decode()
    # 这一步是用来做token过期用的
    # token_redis.set(str(user.pk), token, ex=expiration)
    return token


def token_expired(user_id):
    """
    保证一个用户同时只能使用一个token
    :param user_id:
    """
    token_redis.delete(user_id)


def get_key(secret_key, expiration=5 * 60, **kwargs):
    """
    生成一个加密key
    :param secret_key: 加密字符串
    :param expiration: 过期时间,默认5分钟
    :param kwargs: 需加密的dict
    :return:
    """
    ser = Serializer(secret_key, expires_in=expiration)
    return ser.dumps(kwargs).decode()


def get_key_data(secret_key, key):
    """
    通过加密key解密数据
    :param secret_key: 加密字符串,注意加密和解密的secret_key必须一致
    :param key: 加密过后的key
    :return: data:加密之前的数据
    """

    s = Serializer(secret_key)
    try:
        data = s.loads(key)
    except (SignatureExpired, BadSignature):
        return False
    return data
