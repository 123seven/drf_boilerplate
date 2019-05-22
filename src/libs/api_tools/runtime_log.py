# @Time         : 19-1-8 上午10:48
# @Author       : Seven
# @File         : runtime_log.py
# @Description  : 得到运行时间模块

import logging
import time
from functools import wraps


def runtime(func):
    """
    装饰器: 得到运行时间
    :param func: function
    """

    @wraps(func)
    def inner(*args, **kwargs):
        start = time.time()
        ret = func(*args, **kwargs)
        end = time.time()
        logging.info(f'{func.__name__} Cost {end - start} seconds')
        print(f'Cost {end - start} seconds')
        return ret

    return inner
