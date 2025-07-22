from django.db import models
from accounts.models.base_model import TimeStampedModel, SoftDeletableModel


class ArticleStatus(models.TextChoices):
    DRAFT = "DRAFT", "草稿"
    REVIEW = "REVIEW", "审核中"
    PUBLISHED = "PUBLISHED", "已发布"


class Tag(TimeStampedModel, SoftDeletableModel):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=7, default="#cccccc")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.name


class Article(TimeStampedModel, SoftDeletableModel):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
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
