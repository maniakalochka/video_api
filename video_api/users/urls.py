from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserRegisterAPIView, UserLoginAPIView

urlpatterns = [
    path("register/", UserRegisterAPIView.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    # path('logout', UserLogoutAPIView.as_view(), name='logout'),
]
