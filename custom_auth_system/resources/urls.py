from django.urls import path

from . import views

# ../resources/
urlpatterns = [
    path('', views.resources_index, name='resources_index'),
    path('courses/', views.courses_list, name='courses_list'),
    path('lessons/', views.lessons_list, name='lessons_list'),
    path('tests/', views.tests_list, name='tests_list'),
    path('solutions/', views.solutions_list, name='solutions_list'),
    path('professions/', views.professions_list, name='professions_list'),
]