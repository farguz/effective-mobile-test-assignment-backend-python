from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin

from .models import CustomUser
from .utils_jwt import decode_token


class JWTAuthenticationMiddleware(MiddlewareMixin):

    def process_request(self, request):

        token = request.COOKIES.get('access_token')

        if not token:
            request.user = AnonymousUser()
            return

        try:
            payload = decode_token(token)
            user = CustomUser.objects.get(id=payload['user_id'])
            request.user = user
        except Exception:
            request.user = AnonymousUser()