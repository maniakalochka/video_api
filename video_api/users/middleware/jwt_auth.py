from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser


class JWTAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        jwt_authenticator = JWTAuthentication()

        try:
            user_auth_tuple = jwt_authenticator.authenticate(request)
            if user_auth_tuple is not None:
                request.user, request.auth = user_auth_tuple
            else:
                request.user = AnonymousUser()
        except Exception:
            request.user = AnonymousUser()
