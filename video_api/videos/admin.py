from django.contrib import admin

from .models import Video


@admin.register(Video)
class ContentAdmin(admin.ModelAdmin):
    model = Video
    list_display = ("name", "is_published", "total_likes", "created_at")
    list_filter = ("is_published", "created_at")
    search_fields = ("name",)
    ordering = ("-created_at",)
    readonly_fields = ("total_likes",)
