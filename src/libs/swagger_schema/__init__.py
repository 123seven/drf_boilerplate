# coreapi.Field(name, required, location, schema, description, type, example
from decimal import Decimal

from coreapi import Field as SchemaField
from rest_framework import parsers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.renderers import CoreJSONRenderer, JSONRenderer, encoders
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema as DrfAutoSchema
from rest_framework.views import APIView as DrfAPIView
from rest_framework_swagger import renderers


class JSONEncoderWithDecimal(encoders.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super().default(obj)


class JSONRendererWithDecimal(JSONRenderer):
    encoder_class = JSONEncoderWithDecimal


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class AutoSchema(DrfAutoSchema):
    def get_path_fields(self, path, method):
        ret = super().get_path_fields(path, method)
        return ret + getattr(self.view, 'fields', []) + self.get_method_fields(self.view, method, path)

    def get_serializer_fields(self, path, method):
        return []

    @staticmethod
    # 从类中取出我们自定义的参数, 交给 swagger 以生成接口文档.
    def get_method_fields(view, method, path):
        # 针对 ViewSet list 的fields
        if 'ViewSet' in str(view):
            if method.lower() == 'get' and 'id}' not in path:
                handler = getattr(view, f'list_fields', [])
                return handler
        handler = getattr(view, f'{method.lower()}_fields', [])
        return handler


class ActionSchema(DrfAutoSchema):
    def get_path_fields(self, path, method):
        ret = super().get_path_fields(path, method)
        return ret + getattr(self.view, 'fields', []) + self.get_method_fields(self.view, method, path)

    def get_serializer_fields(self, path, method):
        return []

    @staticmethod
    # 从类中取出我们自定义的参数, 交给 swagger 以生成接口文档.
    def get_method_fields(view, method, path):
        # 针对 ViewSet list 的fields

        if 'ViewSet' in str(view):
            # action 操作去调用对应的fields方法
            if hasattr(view, 'action'):
                handler = getattr(view, f'{view.action}_fields', [])
                if not handler:
                    handler = getattr(view, f'{method.lower()}_fields', [])
                return handler
        return []


class APIView(DrfAPIView):
    schema = AutoSchema()  # GenSchema()
    renderer_classes = [JSONRendererWithDecimal, ]
    # https://stackoverflow.com/a/30875830/41948
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)


class SwaggerView(DrfAPIView):
    _ignore_model_permissions = True
    exclude_from_schema = True
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = [AllowAny]
    # 设置渲染器
    renderer_classes = [
        CoreJSONRenderer,
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer,
    ]

    @classmethod
    def get(cls, request):
        generator = AutoSchema(title='Swagger')

        schema = generator.get_schema(request=request)
        return Response(schema)


__all__ = ('SchemaField', 'APIView', 'parsers', 'AutoSchema', 'ActionSchema')
