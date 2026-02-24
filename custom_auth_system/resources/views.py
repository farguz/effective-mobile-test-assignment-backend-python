from django.shortcuts import render

from custom_auth_system.users.decorators import check_permission

# Create your views here.


@check_permission('course', action='can_read')
def course_list(request):
    courses = [
        {'id': 1, 'name': 'Python basics'},
        {'id': 2, 'name': 'Django basics'},
    ]
    return render(request, 'resources/index.html', {
        'title': 'Courses List',
        'items': courses
    })


@check_permission('solution', action='can_read')
def solution_detail(request):
    return render(request, 'resources/solution.html', {
        'content': 'Solution: print("Hello World")'
    })