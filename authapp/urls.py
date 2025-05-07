"""URL configuration for authentication app.

This module defines the URL patterns for authentication-related views.
"""

from django.urls import path

from .views import (
    AboutView,
    ContactView,
    CustomLoginView,
    CustomRegisterView,
    Home,
    LogoutView,
    ProfileUpdateView,
)

urlpatterns = [
    path("", Home.as_view(), name="index"),  # Root URL pattern
    path("login/", CustomLoginView.as_view(), name="login"),  # Added trailing slash
    path("logout/", LogoutView.as_view(), name="logout"),  # Added trailing slash
    path("register/", CustomRegisterView.as_view(), name="register"),  # Added trailing slash
    path("about/", AboutView.as_view(), name="about"),  # Added trailing slash
    path("contact/", ContactView.as_view(), name="contact"),  # Added trailing slash
    path("profile/", ProfileUpdateView.as_view(), name="profile"),  # Added trailing slash
    path("home/", Home.as_view(), name="home"),  # Added trailing slash
]
