
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages

from .forms import JWTLoginForm
from .models import CustomUser
from .utils_jwt import (
    decode_token,
    generate_access_token,
    generate_refresh_token,
)


def login_view(request):

    if request.method == 'POST':
        form = JWTLoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                form.add_error(None, 'Invalid credentials')
                return render(request, 'users/login.html', {'form': form})

            if not check_password(password, user.password):
                form.add_error(None, 'Invalid credentials')
                return render(request, 'users/login.html', {'form': form})
            
            if not user.is_active:
                form.add_error(None, 'Your account has been deleted, contact admin if you want to restore it')
                return render(request, 'users/login.html', {'form': form})

            access = generate_access_token(user)
            refresh = generate_refresh_token(user)

            response = redirect('index_page')

            response.set_cookie(
                key='access_token',
                value=access,
                httponly=True,
                secure=False,
                samesite='Lax'
            )

            response.set_cookie(
                key='refresh_token',
                value=refresh,
                httponly=True,
                secure=False,
                samesite='Lax'
            )
            
            messages.success(request, 'You has been logged in successfully')
            return response

    else:
        form = JWTLoginForm()

    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    response = redirect('login')
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    messages.success(request, 'You has been logged out successfully')
    return response


def refresh_view(request):
    refresh_token = request.COOKIES.get('refresh_token')

    if not refresh_token:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    try:
        payload = decode_token(refresh_token)

        if payload['type'] != 'refresh':
            return JsonResponse({'error': 'Invalid token'}, status=400)

        user = CustomUser.objects.get(id=payload['user_id'])
        new_access = generate_access_token(user)

        response = JsonResponse({'message': 'Access refreshed'})

        response.set_cookie(
            key='access_token',
            value=new_access,
            httponly=True,
            secure=False,
            samesite='Lax'
        )

        return response

    except Exception:
        return JsonResponse({'error': 'Invalid token'}, status=401)