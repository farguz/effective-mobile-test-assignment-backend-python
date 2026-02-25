import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

from .forms import PermissionForm
from .models import Permission


def permission_list(request):
    if not request.user.is_authenticated:
        return render(request, '403.html', status=401)

    if not (request.user.is_superuser or 
            (request.user.role and request.user.role.name == 'admin')):
        return render(request, '403.html', status=403)

    permissions = Permission.objects.select_related('role', 'resource')
    return render(request, 'users/permission_list.html', {
        'permissions': permissions
    })


def permission_update(request, permission_id):
    if not request.user.is_authenticated:
        return render(request, '403.html', status=401)

    if not (request.user.is_superuser or 
            (request.user.role and request.user.role.name == 'admin')):
        return render(request, '403.html', status=403)

    permission = get_object_or_404(Permission, id=permission_id)

    if request.method == 'POST':
        form = PermissionForm(request.POST, instance=permission)
        if form.is_valid():
            form.save()
            return redirect('permission_list')
    else:
        form = PermissionForm(instance=permission)

    return render(request, 'users/permission_update.html', {
        'form': form,
        'permission': permission
    })


def permission_list_api(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    if not request.user.role or request.user.role.name != 'admin':
        return JsonResponse({'error': 'Forbidden'}, status=403)

    permissions = Permission.objects.select_related('role', 'resource')

    data = []
    for p in permissions:
        data.append({
            'id': p.id,
            'role': p.role.name,
            'resource': p.resource.name,
            'can_read': p.can_read,
            'can_create': p.can_create,
            'can_update': p.can_update,
            'can_delete': p.can_delete,
            'can_soft_delete': p.can_soft_delete,
        })

    return JsonResponse(data, safe=False)


@csrf_exempt
def permission_update_api(request, permission_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    if not request.user.role or request.user.role.name != 'admin':
        return JsonResponse({'error': 'Forbidden'}, status=403)

    if request.method != 'PUT':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        permission = Permission.objects.get(id=permission_id)
    except Permission.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)

    data = json.loads(request.body)

    permission.can_read = data.get('can_read', permission.can_read)
    permission.can_create = data.get('can_create', permission.can_create)
    permission.can_update = data.get('can_update', permission.can_update)
    permission.can_delete = data.get('can_delete', permission.can_delete)
    permission.can_soft_delete = data.get('can_soft_delete', permission.can_soft_delete)

    permission.save()

    return JsonResponse({'message': 'Permission updated'})