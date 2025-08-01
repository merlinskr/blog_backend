from django.db import models
from django.conf import settings
from accounts.models.base_model import TimeStampedModel, SoftDeletableModel


class ArticleStatus(models.TextChoices):
    DRAFT = "DRAFT", "草稿"
    REVIEW = "REVIEW", "审核中"
    PUBLISHED = "PUBLISHED", "已发布"


class Tag(TimeStampedModel, SoftDeletableModel):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=7)
    is_active = models.BooleanField()

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.name


class Article(TimeStampedModel, SoftDeletableModel):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="articles"
    )
    tags = models.ManyToManyField(Tag, related_name="articles")
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    slug = models.SlugField(max_length=255, unique=True)
    favorites = models.PositiveIntegerField(default=0)
    cover_image = models.ImageField(upload_to="articles/covers/", blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)
    published = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20, choices=ArticleStatus.choices, default=ArticleStatus.DRAFT
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
