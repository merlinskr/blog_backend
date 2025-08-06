from django.db import models
from django.conf import settings
from accounts.models.base_model import TimeStampedModel, SoftDeletableModel
import uuid
import os


class FileCategory(models.TextChoices):
    IMAGE = "image", "图片"
    DOCUMENT = "document", "文档"
    VIDEO = "video", "视频"
    AUDIO = "audio", "音频"
    OTHER = "other", "其他"


class UploadedFile(TimeStampedModel, SoftDeletableModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    original_name = models.CharField(max_length=255, verbose_name="原始文件名")
    file_name = models.CharField(max_length=255, verbose_name="存储文件名")
    file_path = models.CharField(max_length=500, verbose_name="文件路径")
    file_url = models.URLField(verbose_name="文件访问URL", max_length=1000)
    file_size = models.BigIntegerField(verbose_name="文件大小(字节)")
    file_type = models.CharField(max_length=100, verbose_name="文件类型")
    category = models.CharField(
        max_length=20,
        choices=FileCategory.choices,
        default=FileCategory.OTHER,
        verbose_name="文件分类",
    )
    width = models.PositiveIntegerField(null=True, blank=True, verbose_name="图片宽度")
    height = models.PositiveIntegerField(null=True, blank=True, verbose_name="图片高度")
    duration = models.FloatField(null=True, blank=True, verbose_name="音视频时长")
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="uploaded_files",
        verbose_name="上传者",
    )

    # 使用统计
    download_count = models.PositiveIntegerField(default=0, verbose_name="下载次数")
    view_count = models.PositiveIntegerField(default=0, verbose_name="查看次数")

    # 文件状态
    is_public = models.BooleanField(default=True, verbose_name="是否公开")
    is_processed = models.BooleanField(default=False, verbose_name="是否已处理")

    # 关联信息
    related_model = models.CharField(
        max_length=100, blank=True, verbose_name="关联模型", null=True
    )
    related_id = models.CharField(
        max_length=100, blank=True, verbose_name="关联ID", null=True
    )

    @property
    def vite_compatible_url(self):
        """返回Vite兼容的URL"""
        if self.file_url and self.file_url.lower().endswith(".svg"):
            return f"{self.file_url}?react"
        return self.file_url

    @property
    def file_size_human(self):
        """人类可读的文件大小"""
        size = self.file_size
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"

    def get_category_from_mimetype(self, mimetype):
        """根据MIME类型确定文件分类"""
        if mimetype.startswith("image/"):
            return FileCategory.IMAGE
        elif mimetype.startswith("video/"):
            return FileCategory.VIDEO
        elif mimetype.startswith("audio/"):
            return FileCategory.AUDIO
        elif mimetype in ["application/pdf", "application/msword", "text/plain"]:
            return FileCategory.DOCUMENT
        else:
            return FileCategory.OTHER

    class Meta:
        verbose_name = "上传文件"
        verbose_name_plural = "上传文件"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["uploaded_by", "category"]),
            models.Index(fields=["file_type"]),
            models.Index(fields=["is_public"]),
        ]

    def __str__(self):
        return f"{self.original_name} ({self.file_size_human})"


class FileAccessLog(TimeStampedModel):
    """文件访问日志"""

    file = models.ForeignKey(
        UploadedFile, on_delete=models.CASCADE, related_name="access_logs"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="访问用户",
    )
    ip_address = models.GenericIPAddressField(verbose_name="IP地址")
    user_agent = models.TextField(blank=True, verbose_name="用户代理")
    action = models.CharField(
        max_length=20,
        choices=[
            ("view", "查看"),
            ("download", "下载"),
        ],
        verbose_name="操作类型",
    )

    class Meta:
        verbose_name = "文件访问日志"
        verbose_name_plural = "文件访问日志"
        ordering = ["-created_at"]
