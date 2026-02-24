from django.http import HttpResponseForbidden

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
