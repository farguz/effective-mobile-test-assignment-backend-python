from django.contrib import messages
from django.shortcuts import redirect, render

from custom_auth_system.users.decorators import (
    has_permission,
    permission_required_html,
)

# Create your views here.
resources = [
        {'name': 'Professions', 'url': 'professions_list'},
        {'name': 'Courses', 'url': 'courses_list'},
        {'name': 'Lessons', 'url': 'lessons_list'},
        {'name': 'Tests', 'url': 'tests_list'},
        {'name': 'Solutions', 'url': 'solutions_list'},
    ]

courses = [
    {'id': 1, 'name': 'Python Basics'},
    {'id': 2, 'name': 'Django Fundamentals'},
    {'id': 3, 'name': 'REST API Development'},
    {'id': 4, 'name': 'Database Design with PostgreSQL'},
    {'id': 5, 'name': 'Authentication & JWT'},
    {'id': 6, 'name': 'Docker for Backend Developers'},
]

professions = [
    {'id': 1, 'name': 'Backend Developer'},
    {'id': 2, 'name': 'Fullstack Developer'},
    {'id': 3, 'name': 'DevOps Engineer'},
    {'id': 4, 'name': 'Data Engineer'},
    {'id': 5, 'name': 'QA Automation Engineer'},
    {'id': 6, 'name': 'Machine Learning Engineer'},
]

lessons = [
    {'id': 1, 'name': 'Variables and Data Types'},
    {'id': 2, 'name': 'Functions and Scope'},
    {'id': 3, 'name': 'OOP in Python'},
    {'id': 4, 'name': 'Django Models and ORM'},
    {'id': 5, 'name': 'Working with Forms'},
    {'id': 6, 'name': 'Middleware and Authentication'},
]

tests = [
    {'id': 1, 'name': 'Python Basics Test'},
    {'id': 2, 'name': 'OOP Knowledge Check'},
    {'id': 3, 'name': 'Django ORM Test'},
    {'id': 4, 'name': 'REST API Concepts Test'},
    {'id': 5, 'name': 'JWT Authentication Test'},
    {'id': 6, 'name': 'Database Fundamentals Test'},
]

solutions = [
    {'id': 1, 'name': 'FizzBuzz Solution'},
    {'id': 2, 'name': 'CRUD API Implementation'},
    {'id': 3, 'name': 'User Authentication System'},
    {'id': 4, 'name': 'Role-Based Access Control'},
    {'id': 5, 'name': 'Soft Delete Implementation'},
    {'id': 6, 'name': 'Dockerized Django App'},
]

DATA_STORAGE = {
    'course': {
        'items': courses,
        'template': 'resources/courses_list.html',
        'context_name': 'courses',
    },
    'lesson': {
        'items': lessons,
        'template': 'resources/lessons_list.html',
        'context_name': 'lessons',
    },
    'test': {
        'items': tests,
        'template': 'resources/tests_list.html',
        'context_name': 'tests',
    },
    'solution': {
        'items': solutions,
        'template': 'resources/solutions_list.html',
        'context_name': 'solutions',
    },
    'profession': {
        'items': professions,
        'template': 'resources/professions_list.html',
        'context_name': 'professions',
    },
}


@permission_required_html('profession', 'read')
def resources_index(request):

    return render(request, 'resources/index.html', {
        'resources': resources
    })


def resource_crud_view(request, resource_key):
    config = DATA_STORAGE[resource_key]
    items = config['items']

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add':
            if not has_permission(request.user, resource_key, 'create'):
                messages.error(request, f'You cannot create {resource_key}s')
                return redirect(f'{resource_key}s_list')

            name = request.POST.get('name')

            if name:
                new_id = max(i['id'] for i in items) + 1 if items else 1
                items.append({'id': new_id, 'name': name})
                messages.success(request, f'{resource_key.capitalize()} added')
            else:
                messages.error(request, 'Name cannot be empty')

            return redirect(f'{resource_key}s_list')

        if action == 'delete':
            if not has_permission(request.user, resource_key, 'delete'):
                messages.error(request, f'You cannot delete {resource_key}s')
                return redirect(f'{resource_key}s_list')

            item_id = int(request.POST.get('item_id'))
            config['items'] = [i for i in items if i['id'] != item_id]

            messages.success(request, f'{resource_key.capitalize()} deleted')
            return redirect(f'{resource_key}s_list')

    return render(request, config['template'], {
        config['context_name']: config['items'],
        'can_create': has_permission(request.user, resource_key, 'create'),
        'can_delete': has_permission(request.user, resource_key, 'delete'),
    })


@permission_required_html('course', 'read')
def courses_list(request):
    return resource_crud_view(request, 'course')


@permission_required_html('lesson', 'read')
def lessons_list(request):
    return resource_crud_view(request, 'lesson')


@permission_required_html('test', 'read')
def tests_list(request):
    return resource_crud_view(request, 'test')


@permission_required_html('solution', 'read')
def solutions_list(request):
    return resource_crud_view(request, 'solution')


@permission_required_html('profession', 'read')
def professions_list(request):
    return resource_crud_view(request, 'profession')