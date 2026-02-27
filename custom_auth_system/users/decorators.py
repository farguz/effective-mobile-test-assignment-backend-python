from functools import wraps

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect

from .models import Permission


def _is_admin(user):
    return (
        user.is_authenticated and
        (
            user.is_superuser or
            (user.role and user.role.name == 'admin')
        )
    )


def has_permission(user, resource_name, action):
    if _is_admin(user):
        return True

    if not user.is_authenticated or not user.role:
        return False

    try:
        permission = Permission.objects.get(
            role=user.role,
            resource__name=resource_name
        )
    except Permission.DoesNotExist:
        return False

    return getattr(permission, f'can_{action}', False)


# htmls
def admin_required_html(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in.')
            return redirect('login')

        if not _is_admin(request.user):
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('index_page')

        return view_func(request, *args, **kwargs)

    return wrapper


def permission_required_html(resource_name, action):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                messages.error(request, 'You must be logged in.')
                return redirect('login')

            if not has_permission(request.user, resource_name, action):
                messages.error(
                    request,
                    'You do not have permission to access this page.'
                )
                return redirect('index_page')

            return view_func(request, *args, **kwargs)

        return wrapper
    return decorator


# apis
def admin_required_api(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

        if not _is_admin(request.user):
            return JsonResponse({'error': 'Forbidden'}, status=403)

        return view_func(request, *args, **kwargs)

    return wrapper


def permission_required_api(resource_name, action):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return JsonResponse({'error': 'Unauthorized'}, status=401)

            if not has_permission(request.user, resource_name, action):
                return JsonResponse({'error': 'Forbidden'}, status=403)

            return view_func(request, *args, **kwargs)

        return wrapper
    return decorator