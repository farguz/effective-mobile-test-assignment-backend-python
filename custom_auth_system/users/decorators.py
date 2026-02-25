from functools import wraps

from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render

from .models import Permission


def check_permission(resource_name, action='can_read'):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden(
                    '401 Unauthorized: Please login',
                    status=401
                    )
            
            if request.user.is_superuser or (request.user.role and request.user.role.name == 'admin'):
                return view_func(request, *args, **kwargs)

            user_role = request.user.role
            permission = Permission.objects.filter(
                role=user_role, 
                resource__name=resource_name
            ).first()

            if permission and getattr(permission, action):
                return view_func(request, *args, **kwargs)
            
            return HttpResponseForbidden(
                f'403 Forbidden: Not enough rights to access {resource_name}',
                status=403
                )
        return _wrapped_view
    return decorator


def _is_admin(user):
    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    if user.role and user.role.name == 'admin':
        return True

    return False


# html
def admin_required_html(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, '403.html', status=401)

        if not _is_admin(request.user):
            return render(request, '403.html', status=403)

        return view_func(request, *args, **kwargs)

    return wrapper


# api
def admin_required_api(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

        if not _is_admin(request.user):
            return JsonResponse({'error': 'Forbidden'}, status=403)

        return view_func(request, *args, **kwargs)

    return wrapper


def has_permission(user, resource_name, action):
    if user.is_superuser:
        return True

    if not user.role:
        return False

    try:
        permission = Permission.objects.get(
            role=user.role,
            resource__name=resource_name
        )
    except Permission.DoesNotExist:
        return False

    return getattr(permission, f'can_{action}', False)