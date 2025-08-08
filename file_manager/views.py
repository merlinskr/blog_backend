from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from django.http import Http404, HttpResponse
from django.core.files.storage import default_storage
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control

from .models import UploadedFile, FileAccessLog
from .serializer import (
    UploadedFileSerializer,
    FileUploadSerializer,
    FileAccessLogSerializer,
)
from .server import FileManagerService


def get_client_ip(request):
    """获取客户端IP地址"""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


class FileUploadView(APIView):
    """文件上传接口"""

    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        request=FileUploadSerializer,
        responses={201: UploadedFileSerializer, 400: "Bad Request"},
        description="上传文件到云存储",
        tags=["文件管理"],
    )
    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # 使用服务类上传文件
                uploaded_file = FileManagerService.upload_file(
                    file=serializer.validated_data["file"],
                    user=request.user,
                    category=serializer.validated_data.get("category"),
                    is_public=serializer.validated_data.get("is_public", True),
                    related_model=serializer.validated_data.get("related_model"),
                    related_id=serializer.validated_data.get("related_id"),
                )

                # 记录上传日志
                FileManagerService.log_file_access(
                    file_id=uploaded_file.id,
                    user=request.user,
                    ip_address=get_client_ip(request),
                    user_agent=request.META.get("HTTP_USER_AGENT", ""),
                    action="upload",
                )

                # 返回文件信息
                response_serializer = UploadedFileSerializer(uploaded_file)
                return Response(
                    response_serializer.data, status=status.HTTP_201_CREATED
                )

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileListView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="category",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="文件分类过滤",
            ),
            OpenApiParameter(
                name="is_public",
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description="是否公开",
            ),
        ],
        responses={200: UploadedFileSerializer(many=True)},
        description="获取用户上传的文件列表",
        tags=["文件管理"],
    )
    def get(self, request):
        category = request.query_params.get("category")
        is_public = request.query_params.get("is_public")

        if is_public is not None:
            is_public = is_public.lower() in ["true", "1"]

        files = FileManagerService.get_user_files(
            user=request.user,
            category=category,
            is_public=is_public,
        )

        files = files.select_related("uploaded_by")

        serializer = UploadedFileSerializer(files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
