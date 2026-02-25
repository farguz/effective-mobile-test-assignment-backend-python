from django.urls import path

from . import views_admin
from .views import (
    DeleteUserView,
    RegistrationView,
    UpdateUserView,
)

# ../users/
urlpatterns = [
    path('<int:pk>/update/', UpdateUserView.as_view(), name='user_update'),
    path('<int:pk>/delete/', DeleteUserView.as_view(), name='user_delete'),
    path('create/', RegistrationView.as_view(), name='user_create'),
]

# ../permissions/
urlpatterns += [
    path('permissions/', views_admin.permission_list, name='permission_list'),
    path('permissions/<int:permission_id>/update/', views_admin.permission_update, name='permission_update'),
    path('api/permissions/', views_admin.permission_list_api),
    path('api/permissions/<int:permission_id>/', views_admin.permission_update_api),
]