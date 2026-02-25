import json

from django.contrib.auth import authenticate
from django.http import JsonResponse

from .models import CustomUser
from .utils_jwt import (
    decode_token,
    generate_access_token,
    generate_refresh_token,
)


def login_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    data = json.loads(request.body)
    email = data.get("email")
    password = data.get("password")

    user = authenticate(request, email=email, password=password)

    if not user:
        return JsonResponse({"error": "Invalid credentials"}, status=401)

    access = generate_access_token(user)
    refresh = generate_refresh_token(user)

    return JsonResponse({
        "access": access,
        "refresh": refresh
    })


def refresh_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    data = json.loads(request.body)
    refresh_token = data.get("refresh")

    try:
        payload = decode_token(refresh_token)

        if payload["type"] != "refresh":
            return JsonResponse({"error": "Invalid token type"}, status=400)

        user = CustomUser.objects.get(id=payload["user_id"])
        new_access = generate_access_token(user)

        return JsonResponse({"access": new_access})

    except Exception:
        return JsonResponse({"error": "Invalid token"}, status=401)