from django.conf import settings
from django.db import models


class Video(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="videos"
    )
    name = models.CharField(max_length=255, verbose_name="Название")
    is_published = models.BooleanField(default=False, verbose_name="Опубликовано")  # type: ignore
    total_likes = models.PositiveIntegerField(default=0, verbose_name="Всего лайков")  # type: ignore
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return str(self.name)


class VideoFile(models.Model):
    class Quality(models.TextChoices):
        HD = "HD", "High Definition"
        FHD = "FHD", "Full High Definition"
        UHD = "UHD", "Ultra High Definition"

    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(blank=True, null=True, verbose_name="Видео файл")
    quality = models.CharField(
        choices=Quality.choices,
        default=Quality.HD,
        verbose_name="Качество видео",
        max_length=3,
    )

    class Meta:
        verbose_name = "Видео файл"
        verbose_name_plural = "Видео файлы"
        unique_together = ("video", "quality")
        constraints = [
            models.UniqueConstraint(
                fields=["video", "quality"], name="unique_video_quality"
            )
        ]

    def __str__(self) -> str:
        return f"{self.video.name} - {self.file.name if self.file else 'No file'}"


class Like(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="likes"
    )

    class Meta:
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"
        constraints = [
            models.UniqueConstraint(
                fields=["video", "user"], name="unique_video_like"
            )
        ]

    def __str__(self) -> str:
        return f"{self.user.username} liked {self.video.name}"  # type: ignore
