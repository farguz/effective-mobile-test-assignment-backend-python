from django.contrib import messages
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import CustomUserChangeForm, CustomUserCreationForm

User = get_user_model()


class RegistrationView(CreateView):

    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')

    def get_success_url(self):
        messages.success(self.request, 'User created successfully')
        return super().get_success_url()


class UpdateUserView(UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'users/update.html'
    pass


class DeleteUserView(DeleteView):

    model = User
    template_name = 'users/delete.html'
    pass