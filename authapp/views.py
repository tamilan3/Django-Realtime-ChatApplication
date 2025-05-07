"""Authentication views module.

This module contains views for handling user authentication, registration,
and profile management.
"""

from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, UpdateView

from .CustomeForms import CustomUserCreationForm, EmailAuthenticationForm
from .models import CustomUser


class CustomLoginView(LoginView):
    """View for handling user login with email authentication."""

    authentication_form = EmailAuthenticationForm
    template_name = "authapp/login.html"

    def get_success_url(self):
        """Return the success URL after login."""
        return settings.LOGIN_REDIRECT_URL

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('chat:index')
        return super().dispatch(request, *args, **kwargs)


class CustomRegisterView(CreateView):
    """View for handling new user registration."""

    form_class = CustomUserCreationForm
    template_name = "authapp/register.html"
    success_url = reverse_lazy("login")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('chat:index')  # Update to use namespaced URL
        return super().dispatch(request, *args, **kwargs)


class LogoutView(View):
    """View for handling user logout."""

    def get(self, request):
        """Handle GET request to log out user."""
        logout(request)
        return redirect("login")


class AboutView(View):
    """View for about page."""

    def get(self, request):
        """Handle GET request for about page."""
        return render(request, "authapp/about.html")


class ContactView(LoginRequiredMixin, View):
    """View for contact form."""

    login_url = "/auth/login/"  # Redirect to login page if not authenticated

    def get(self, request):
        """Handle GET request for contact form."""
        return render(request, "authapp/contact.html")

    def post(self, request):
        """Handle POST request for contact form submission."""
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        send_mail(
            f"Contact Form Submission from {name}",
            f"Name: {name}\nEmail: {email}\nMessage: {message}",
            settings.DEFAULT_FROM_EMAIL,
            [settings.CONTACT_FORM_RECIPIENT],
            fail_silently=False,
        )

        return HttpResponse("Thank you! We've received your message.")


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """View for updating user profile."""

    login_url = "/auth/login/"
    model = CustomUser
    fields = ["username", "gender", "profile_pic", "address"]
    template_name = "authapp/profile.html"
    success_url = reverse_lazy("profile")
    context_object_name = "user_profile"

    def get_object(self, queryset=None):
        """Return the current user's profile."""
        return self.request.user

    def form_valid(self, form):
        """Process the form if valid."""
        # Delete old profile picture if it exists and a new one is uploaded
        if form.cleaned_data.get("profile_pic"):
            old_pic = self.get_object().profile_pic
            if old_pic and old_pic.name != "profile_pics/default.png":
                try:
                    old_pic.delete(save=False)
                except Exception:
                    pass  # Don't fail if file is missing
        return super().form_valid(form)


class Home(View):
    """View for home page."""

    def get(self, request):
        """Handle GET request for home page."""
        return render(request, "authapp/home.html")
