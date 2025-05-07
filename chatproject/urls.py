"""URL configuration for chatproject."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def redirect_to_chat(request):
    return redirect('chat:index')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", redirect_to_chat, name="root"),  # Redirect root to chat index
    path("chat/", include("chatapp.urls", namespace="chat")),  # Include with namespace
    path("auth/", include("authapp.urls")),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
