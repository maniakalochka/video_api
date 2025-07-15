from django.db import models
from django.conf import settings


class Video(models.Model):
    owner = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            related_name="videos"
        )
    name = models.CharField(max_length=255, verbose_name="Название")
    is_published = models.BooleanField(default=False, verbose_name="Опубликовано")  # type: ignore
    total_likes = models.PositiveIntegerField(default=0, verbose_name="Всего лайков")  # type: ignore
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
