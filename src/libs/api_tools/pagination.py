from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class StandardResultsSetPagination(PageNumberPagination):
    """ 自写分页，继承PageNumberPagination """
    # 默认每页显示的数据条数
    page_size = 15

    # 获取URL参数中设置的每页显示数据条数
    page_size_query_param = 'page_size'

    # 获取URL参数中传入的页码key
    page_query_param = 'page'

    # 最大支持的每页显示的数据条数
    max_page_size = 100


class StandardResultsSetLimitOffsetPagination(LimitOffsetPagination):
    # 默认每页显示的数据条数
    default_limit = 15
    # URL中传入的显示数据条数的参数
    limit_query_param = 'limit'
    # URL中传入的数据位置的参数
    offset_query_param = 'offset'
    # 最大每页显得条数
    max_limit = None
