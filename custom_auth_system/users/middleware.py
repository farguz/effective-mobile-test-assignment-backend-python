from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin

from .models import CustomUser
from .utils_jwt import decode_token


class JWTAuthenticationMiddleware(MiddlewareMixin):

    def process_request(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return

        try:
            prefix, token = auth_header.split(" ")

            if prefix != "Bearer":
                return

            payload = decode_token(token)
            user = CustomUser.objects.get(id=payload["user_id"])
            request.user = user

        except Exception:
            request.user = AnonymousUser()