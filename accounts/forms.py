from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from .models import User
# User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    """User Registration Form"""

    class Meta:
        model = User
        fields = (
            'username', 'email',
            'password1', 'password2',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


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
