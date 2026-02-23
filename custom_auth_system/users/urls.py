from django.urls import path

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