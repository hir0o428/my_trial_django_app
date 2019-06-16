from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import resolve_url

from .models import User
from .forms import LoginForm, UserProfileUpdateForm, UserRegistrationForm


# Create your views here.
class TopLoginView(LoginView):
    form_class = LoginForm
    template_name = "top/login.html"


class TopLogoutView(LogoutView):
    template_name = "top/logout.html"


class TopView(LoginRequiredMixin, TemplateView):
    template_name = "top/top.html"


class UserRegistrationView(CreateView):
    """User Registration"""
    model = User
    template_name = 'accounts/user_registration.html'
    form_class = UserRegistrationForm
    success_url = '/accounts/user_registration/complete'


class UserRegistrationCompView(TemplateView):
    """Account Registration Complete"""
    template_name = 'accounts/user_registration_complete.html'


class UserOnlyMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser


class UserProfileView(UserOnlyMixin, DetailView):
    """User Profile"""
    model = User
    template_name = 'accounts/user_profile.html'

class UserProfileUpdateView(UserOnlyMixin, UpdateView):
    """User Profile Update"""
    model = User
    form_class = UserProfileUpdateForm
    template_name = 'accounts/user_profile_update.html'

    def get_success_url(self):
        return resolve_url('accounts:profile', pk=self.kwargs['pk'])


class UserPasswordChangeView(UserOnlyMixin, PasswordChangeView):
    """User Password Change"""
    model = User
    template_name = 'accounts/user_password_change.html'

    def get_success_url(self):
        return resolve_url('accounts:password_complete', pk=self.kwargs['pk'])


class UserPasswordChangeCompleteView(UserOnlyMixin, PasswordChangeDoneView):
    """User Password Change Complete"""
    template_name = 'accounts/user_password_change_complete.html'
