from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.http import require_GET

from .forms import LoginForm


@require_GET
def index(request):
    return render(
        request,
        'index.html',
    )


class AuthSystemLoginView(LoginView):
    form_class = LoginForm
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        messages.success(self.request, 'Login successful')
        return reverse_lazy('index_page')
         

class AuthSystemLogoutView(LoginRequiredMixin, LogoutView):

    next_page = reverse_lazy('index_page')

    def post(self, request, *args, **kwargs):
        messages.info(request, 'Logout successful')
        return super().post(request, *args, **kwargs)