from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import dumps, loads, SignatureExpired, BadSignature
from django.shortcuts import resolve_url, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.http import Http404, HttpResponseBadRequest
from django.conf import settings

from .forms import LoginForm, UserProfileUpdateForm, UserRegistrationForm

from .models import User
#User = get_user_model()


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
    #success_url = reverse_lazy('accounts:user_registration_complete')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # Send Mail
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }
        subject = render_to_string('accounts/email/user_registration_subject.txt', context)
        message = render_to_string('accounts/email/user_registration_message.txt', context)

        user.email_user(subject.strip(), message)
        return redirect('accounts:user_registration_send_mail')


class UserRegistrationMailView(TemplateView):
    """User Registration(Send Mail)"""
    template_name = 'accounts/user_registration_send_mail.html'


class UserRegistrationCompView(TemplateView):
    """Account Registration Complete"""
    template_name = 'accounts/user_registration_complete.html'


class UserRegistrationCompleteView(TemplateView):
    """Account Registration Complete"""
    template_name = 'accounts/user_registration_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # 1day=60*60*24 sec

    def get(self, request, **kwargs):
        # Check token
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # Timeout
        except SignatureExpired:
            return HttpResponseBadRequest()
        # Bad Token
        except BadSignature:
            return HttpResponseBadRequest()
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)
        return HttpResponseBadRequest()


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
        return resolve_url('accounts:password_change_complete', pk=self.kwargs['pk'])


class UserPasswordChangeCompleteView(UserOnlyMixin, PasswordChangeDoneView):
    """User Password Change Complete"""
    template_name = 'accounts/user_password_change_complete.html'


class UserPasswordResetView(PasswordResetView):
    """User Password Reset Request"""
    subject_template_name = 'accounts/email/user_password_reset_subject.txt'
    email_template_name = 'accounts/email/user_password_reset_message.txt'
    template_name = 'accounts/user_password_reset.html'
    success_url = reverse_lazy('accounts:password_reset_send_mail')


class UserPasswordResetMailView(PasswordResetDoneView):
    """User Password Reset(Send Reset Mail)"""
    template_name = 'accounts/user_password_reset_send_mail.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    """User Password Reset"""
    template_name = 'accounts/user_password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    """User Password Reset Complete"""
    template_name = 'accounts/user_password_reset_complete.html'
