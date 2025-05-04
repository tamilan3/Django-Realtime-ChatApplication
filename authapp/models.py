"""Authentication app models module.

This module defines the custom user model and its manager for the authentication system.
"""

from django.contrib.auth.models import AbstractUser, Group, Permission, UserManager
from django.db import models


class CustomUserManager(UserManager):
    """Custom user manager for email-based authentication."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a user with the given email and password."""
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular user with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        assert extra_fields["is_staff"]
        assert extra_fields["is_superuser"]
        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """Custom user model that uses email for authentication.

    This model extends Django's AbstractUser to use email as the primary
    identifier instead of username, and adds additional fields for user profiles.
    """

    USER_TYPE = ((1, "ADMIN"), (2, "CUSTOMER"))
    GENDER = [("M", "Male"), ("F", "Female")]

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20, null=True)
    user_type = models.CharField(default=1, choices=USER_TYPE, max_length=1)
    gender = models.CharField(max_length=1, choices=GENDER)
    profile_pic = models.ImageField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CustomUserManager()

    REQUIRED_FIELDS = ["username", "user_type", "gender", "profile_pic", "address"]
    USERNAME_FIELD = "email"

    groups = models.ManyToManyField(
        Group, verbose_name="groups", blank=True, related_name="custom_user_groups"
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="user permissions",
        blank=True,
        related_name="custom_user_permissions",
    )

    def __str__(self):
        """Return a string representation of the user."""
        return f"{self.last_name}, {self.first_name}"
