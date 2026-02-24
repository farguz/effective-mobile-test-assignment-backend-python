from django.contrib import messages
from django.contrib.auth import (
    get_user_model,
    logout,
    update_session_auth_hash,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import Role

User = get_user_model()


class RegistrationView(CreateView):

    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')

    def get_success_url(self):
        messages.success(self.request, 'User created successfully')
        return super().get_success_url()
    
    def form_valid(self, form):
        '''
        set default role as student
        '''
        response = super().form_valid(form)
        guest_role = Role.objects.filter(name='guest').first()
        self.object.role = guest_role
        self.object.save()
        return response


class UpdateUserView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('index_page')
    context_object_name = 'user'

    def test_func(self):    
        user = self.get_object()
        return self.request.user == user or self.request.user.is_superuser

    def get_success_url(self):
        messages.success(self.request, 'User updated successfully')
        return super().get_success_url()

    def handle_no_permission(self):
        messages.error(self.request, 'Forbidden. Not enough rights')
        return redirect('index_page')
    
    def form_valid(self, form):
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        if password:
            user.set_password(password)
        user.save()
        update_session_auth_hash(self.request, user)
        return super().form_valid(form)


class DeleteUserView(DeleteView):

    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('index_page')

    def get_success_url(self):
        messages.success(self.request, 'User deleted successfully')
        return super().get_success_url()
    
    def post(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = False
        user.save()
        logout(request)
        return redirect(self.success_url)