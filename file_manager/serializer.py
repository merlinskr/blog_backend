from rest_framework import serializers
from .models import UploadedFile, FileAccessLog, FileCategory


class UploadedFileSerializer(serializers.ModelSerializer):
    file_size_human = serializers.ReadOnlyField()
    vite_compatible_url = serializers.ReadOnlyField()
    uploaded_by_name = serializers.CharField(
        source="uploaded_by.username", read_only=True
    )

    class Meta:
        model = UploadedFile
        fields = [
            "id",
            "original_name",
            "file_name",
            "file_path",
            "file_url",
            "vite_compatible_url",
            "file_size",
            "file_size_human",
            "file_type",
            "category",
            "width",
            "height",
            "duration",
            "uploaded_by",
            "uploaded_by_name",
            "download_count",
            "view_count",
            "is_public",
            "is_processed",
            "related_model",
            "related_id",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "file_path",
            "file_url",
            "file_size",
            "file_type",
            "uploaded_by",
            "download_count",
            "view_count",
            "created_at",
            "updated_at",
        ]


class FileUploadSerializer(serializers.Serializer):
    """文件上传序列化器"""

    file = serializers.FileField()
    category = serializers.ChoiceField(choices=FileCategory.choices, required=False)
    is_public = serializers.BooleanField(default=True)
    related_model = serializers.CharField(max_length=100, required=False)
    related_id = serializers.CharField(max_length=100, required=False)


class FileAccessLogSerializer(serializers.ModelSerializer):
    file_name = serializers.CharField(source="file.original_name", read_only=True)
    user_name = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = FileAccessLog
        fields = [
            "id",
            "file",
            "file_name",
            "user",
            "user_name",
            "ip_address",
            "user_agent",
            "action",
            "created_at",
        ]
