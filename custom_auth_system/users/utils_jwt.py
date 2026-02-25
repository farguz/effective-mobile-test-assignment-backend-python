from datetime import datetime, timedelta

import jwt
from django.conf import settings

ACCESS_TOKEN_LIFETIME = 15  # minutes
REFRESH_TOKEN_LIFETIME = 7  # days


def generate_access_token(user):
    payload = {
        "user_id": user.id,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_LIFETIME),
        "type": "access"
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def generate_refresh_token(user):
    payload = {
        "user_id": user.id,
        "exp": datetime.utcnow() + timedelta(days=REFRESH_TOKEN_LIFETIME),
        "type": "refresh"
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def decode_token(token):
    return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
