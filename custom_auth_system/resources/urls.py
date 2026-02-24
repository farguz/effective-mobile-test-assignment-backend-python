from django.urls import path

from . import views

# ../resources/
urlpatterns = [
    path('courses/', views.course_list, name='course_list'),
    path('solutions/', views.solution_detail, name='solution_detail'),
]
