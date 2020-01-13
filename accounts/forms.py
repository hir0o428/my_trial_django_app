from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model

from .models import User
# User = get_user_model()


class LoginForm(AuthenticationForm):
    """Login Form"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


class UserRegistrationForm(UserCreationForm):
    """User Registration Form"""

    class Meta:
        model = User
        fields = (
            'email',
            'password1', 'password2',
        )

    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
    '''

    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()
        return email


class UserProfileUpdateForm(forms.ModelForm):
    """User Profile Update Form"""

    class Meta:
        model = User
        fields = (
            'username', 'email',
            'last_name', 'first_name',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

