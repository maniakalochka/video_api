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

    def has_view_permission(self, request, obj=None):
        return self._has_video_access(request)

    def has_change_permission(self, request, obj=None):
        return self._has_video_access(request)

    def has_delete_permission(self, request, obj=None):
        return self._has_video_access(request)

    def has_add_permission(self, request):
        return self._has_video_access(request)

    def _has_video_access(self, request):
        user = request.user
        return (
            user.is_superuser
            or user.groups.filter(name="Content Managers").exists()
        )

    def has_module_permission(self, request):
        return self._has_video_access(request)
