from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    # 调用原始的 DRF 异常处理器，拿到原始响应
    response = exception_handler(exc, context)

    if isinstance(exc, (AuthenticationFailed, NotAuthenticated)):
        return Response({
            "code": 401,
            "message": "未登录或Token无效"
        }, status=401)

    # 如果不是认证错误，就返回默认格式
    return response
