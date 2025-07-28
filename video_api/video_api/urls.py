from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('videos.urls')),
    path('', include('users.urls')),
    path('api/schema', SpectacularAPIView.as_view(), name='schema'),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name='docs'),
]
