from django.urls import path
from .views import *


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', CustomRegisterView.as_view(), name='register'),
    path('about/',AboutView.as_view(),name="about"),
    path('contact/',ContactView.as_view(),name="contact"),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    path('home/',Home.as_view(),name='home')

    

]

