from django.contrib import messages
from django.shortcuts import redirect, render

from custom_auth_system.users.decorators import (
    has_permission,
    permission_required_html,
)

# Create your views here.


def resources_index(request):
    resources = [
        {'name': 'Professions', 'url': 'professions_list'},
        {'name': 'Courses', 'url': 'courses_list'},
        {'name': 'Lessons', 'url': 'lessons_list'},
        {'name': 'Tests', 'url': 'tests_list'},
        {'name': 'Solutions', 'url': 'solutions_list'},
    ]

    return render(request, 'resources/index.html', {
        'resources': resources
    })


COURSES = [
    {'id': 1, 'name': 'Python Basics'},
    {'id': 2, 'name': 'Django Basics'},
]


@permission_required_html('course', 'read')
def courses_list(request):
    global COURSES

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add':
            if not has_permission(request.user, 'course', 'create'):
                messages.error(request, 'You cannot create courses.')
                return redirect('courses_list')

            name = request.POST.get('name')

            if name:
                new_id = max(c['id'] for c in COURSES) + 1 if COURSES else 1
                COURSES.append({'id': new_id, 'name': name})
                messages.success(request, 'Course added.')
            else:
                messages.error(request, 'Course name cannot be empty.')

            return redirect('courses_list')

        if action == 'delete':
            if not has_permission(request.user, 'course', 'delete'):
                messages.error(request, 'You cannot delete courses.')
                return redirect('courses_list')

            course_id = int(request.POST.get('course_id'))
            COURSES = [c for c in COURSES if c['id'] != course_id]

            messages.success(request, 'Course deleted.')
            return redirect('courses_list')

    return render(request, 'resources/courses_list.html', {
        'courses': COURSES,
        'can_create': has_permission(request.user, 'course', 'create'),
        'can_delete': has_permission(request.user, 'course', 'delete'),
    })


@permission_required_html('lesson', 'read')
def lessons_list(request):
    return render(request, 'resources/lessons_list.html')


@permission_required_html('test', 'read')
def tests_list(request):
    return render(request, 'resources/tests_list.html')


@permission_required_html('solution', 'read')
def solutions_list(request):
    return render(request, 'resources/solutions_list.html')


@permission_required_html('profession', 'read')
def professions_list(request):
    return render(request, 'resources/professions_list.html')