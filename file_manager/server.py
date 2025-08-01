from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils import timezone
from PIL import Image
import uuid
import os
import mimetypes
from .models import UploadedFile, FileAccessLog


class FileManagerService:
    """文件管理服务类"""

    @staticmethod
    def upload_file(
        file, user, category=None, is_public=True, related_model=None, related_id=None
    ):
        """上传文件"""
        try:
            # 生成唯一文件名
            file_extension = os.path.splitext(file.name)[1]
            unique_filename = f"{uuid.uuid4()}{file_extension}"

            # 根据分类确定存储路径
            if category:
                file_path = f"{category}/{unique_filename}"
            else:
                file_path = f"uploads/{unique_filename}"

            # 保存文件到存储后端
            saved_path = default_storage.save(file_path, file)
            file_url = default_storage.url(saved_path)

            # 获取文件信息
            file_size = file.size
            mimetype, _ = mimetypes.guess_type(file.name)
            file_type = mimetype or "application/octet-stream"

            # 自动确定分类
            if not category:
                uploaded_file = UploadedFile()
                category = uploaded_file.get_category_from_mimetype(file_type)

            # 处理图片信息
            width, height = None, None
            if file_type.startswith("image/"):
                try:
                    with Image.open(file) as img:
                        width, height = img.size
                except Exception:
                    pass

            # 创建文件记录
            uploaded_file = UploadedFile.objects.create(
                original_name=file.name,
                file_name=unique_filename,
                file_path=saved_path,
                file_url=file_url,
                file_size=file_size,
                file_type=file_type,
                category=category,
                width=width,
                height=height,
                uploaded_by=user,
                is_public=is_public,
                related_model=related_model,
                related_id=related_id,
                is_processed=True,
            )

            return uploaded_file

        except Exception as e:
            raise Exception(f"文件上传失败: {str(e)}")

    @staticmethod
    def delete_file(file_id, user):
        """删除文件"""
        try:
            uploaded_file = UploadedFile.objects.get(id=file_id, uploaded_by=user)

            # 从存储后端删除文件
            if default_storage.exists(uploaded_file.file_path):
                default_storage.delete(uploaded_file.file_path)

            # 软删除文件记录
            uploaded_file.delete()

            return True

        except UploadedFile.DoesNotExist:
            raise Exception("文件不存在或无权限删除")
        except Exception as e:
            raise Exception(f"文件删除失败: {str(e)}")

    @staticmethod
    def log_file_access(file_id, user, ip_address, user_agent, action="view"):
        """记录文件访问日志"""
        try:
            uploaded_file = UploadedFile.objects.get(id=file_id)

            # 记录访问日志
            FileAccessLog.objects.create(
                file=uploaded_file,
                user=user,
                ip_address=ip_address,
                user_agent=user_agent,
                action=action,
            )

            # 更新访问统计
            if action == "view":
                uploaded_file.view_count += 1
            elif action == "download":
                uploaded_file.download_count += 1
            uploaded_file.save(update_fields=["view_count", "download_count"])

        except UploadedFile.DoesNotExist:
            pass

    @staticmethod
    def get_user_files(user, category=None, is_public=None):
        """获取用户文件列表"""
        queryset = UploadedFile.objects.filter(uploaded_by=user)

        if category:
            queryset = queryset.filter(category=category)

        if is_public is not None:
            queryset = queryset.filter(is_public=is_public)

        return queryset

    @staticmethod
    def cleanup_orphaned_files():
        """清理孤立文件（定时任务使用）"""
        # 查找没有关联的文件
        orphaned_files = UploadedFile.objects.filter(
            related_model__isnull=True,
            created_at__lt=timezone.now() - timezone.timedelta(days=7),
        )

        for file in orphaned_files:
            try:
                if default_storage.exists(file.file_path):
                    default_storage.delete(file.file_path)
                file.delete()
            except Exception:
                continue
