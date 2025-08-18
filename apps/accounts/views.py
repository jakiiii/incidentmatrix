import random
import datetime
from datetime import timedelta

from django.views import View
from django.conf import settings
from django.utils import timezone
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.utils.timezone import now
from django.core.mail import send_mail
from django.utils.encoding import force_str
from django.shortcuts import redirect, reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import FormView, TemplateView, UpdateView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.messages.views import messages, SuccessMessageMixin
from django.contrib.auth.tokens import default_token_generator

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.contrib.auth import logout

from apps.accounts.forms import (
    UserLoginForm, CustomPasswordChangeForm, UserRegistrationForm, ForgetPasswordForm, PasswordResetForm,
    UserUpdateForm, OTPForm
)

from core.mixins import RateLimitMixin

User = get_user_model()


class RequestFormAttachMixin(object):
    def get_form_kwargs(self):
        kwargs = super(RequestFormAttachMixin, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class NextUrlMixin(object):
    default_next = '/'

    def get_next_url(self):
        next_ = self.request.GET.get('next')
        next_post = self.request.POST.get('next')
        redirect_path = next_ or next_post or None

        if url_has_allowed_host_and_scheme(redirect_path, self.request.get_host()):
            return redirect_path
        return self.default_next


class LoginView(NextUrlMixin, FormView):
    form_class = UserLoginForm
    template_name = "accounts/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return redirect('home:home')
        elif request.user.is_authenticated and request.user.is_operator:
            return redirect('terminal:terminal_dashboard')

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.user)
        next_path = self.get_next_url()
        return redirect(next_path)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Sign In"
        return context

    def get_success_url(self):
        return reverse('home:home')


# class CustomPasswordChangeView(RateLimitMixin, LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
class CustomPasswordChangeView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'accounts/password_change.html'
    success_message = "Your password was successfully updated!"
    max_requests = 3  # Optional: Specific rate limit for password change
    rate_limit_period = timedelta(hours=1)  # Optional: Customize rate limit period for this view

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Change Password'
        return context

    def get_success_url(self):
        return reverse('accounts:password_changed')


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "accounts/profile.html"
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Your profile has been updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error updating your profile.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_object().get_full_name()
        return context


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        # Log the user out
        logout(request)

        # Create a response to redirect to login page
        response = redirect('accounts:login')

        # Delete the otp_verified cookie
        response.delete_cookie('otp_verified')
        return response


class PermissionDeniedView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/permission_denied.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Permission Denied"
        return context
