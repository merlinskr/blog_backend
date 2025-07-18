from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created_time")  # 记录创建时间
    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated_time")      # 记录更新时间

    class Meta:
        abstract = True 


class SoftDeletableModel(models.Model):
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="deleted_time")

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    class Meta:
        abstract = True  