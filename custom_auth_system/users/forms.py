from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'middle_name',
            'last_name',
            'password1',
            'password2',
            'email',
        ]


class CustomUserChangeForm(forms.ModelForm):

    password1 = forms.CharField(
        widget=forms.PasswordInput(),
        label=('Password'),
        required=False,
        help_text=('Leave blank to keep the old password.'),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label=('Password confirmation'),
        required=False,
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if (password1 or password2) and password1 != password2:
            raise forms.ValidationError(('Passwords are not the same'))
        return cleaned_data

    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'middle_name',
            'last_name',
            'email',
        ]