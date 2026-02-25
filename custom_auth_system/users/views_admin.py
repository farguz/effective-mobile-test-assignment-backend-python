import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

from .decorators import admin_required_api, admin_required_html
from .forms import PermissionForm
from .models import Permission


@admin_required_html
def permission_list(request):
    permissions = Permission.objects.select_related('role', 'resource')
    return render(request, 'users/permission_list.html', {
        'permissions': permissions
    })


@admin_required_html
def permission_update(request, permission_id):

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


@admin_required_api
def permission_list_api(request):

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


@admin_required_api
@csrf_exempt
def permission_update_api(request, permission_id):

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