from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView,UpdateView
from .CustomeForms import EmailAuthenticationForm, CustomUserCreationForm
from .models import CustomUser
from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    authentication_form = EmailAuthenticationForm
    template_name = 'authapp/login.html' 
    success_url = reverse_lazy('index')
    
# class CustomLogoutView(LogoutView):
#     pass

class CustomRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'authapp/register.html'  
    success_url = 'login'  



# class LoginView(View):
#     def get(self, request):
#         form = AuthenticationForm()
#         return render(request, 'authapp/login.html', {'form': form})

#     def post(self, request):
#         form = AuthenticationForm(request, request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('index')  # Redirect to your desired URL after login
#             else:
#                 messages.error(request, 'Invalid username or password.')
#         return render(request, 'authapp/login.html', {'form': form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')  # Redirect to login page after logout

# class RegisterView(View):
#     def get(self, request):
#         form = UserCreationForm()
#         return render(request, 'authapp/register.html', {'form': form})

#     def post(self, request):
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('login')  # Redirect to your desired URL after registration/login
#         return render(request, 'authapp/register.html', {'form': form})

class AboutView(View):
    def get(self, request):
        return render(request, 'authapp/about.html')

class ContactView(View):
    def get(self, request):
        return render(request, 'authapp/contact.html')

    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Send email using send_mail() function
        send_mail(
            'Subject: Contact Form Submission',  # Email subject
            f'Name: {name}\nEmail: {email}\nMessage: {message}',  # Email body
            'your_email@example.com',  # Sender's email address (replace with yours)
            ['destination@example.com'],  # List of recipient(s) email address
            fail_silently=False,  # Set to True to fail silently (no error raised)
        )
        print(name, email, message)

        return HttpResponse("Thank you! We've received your message and sent an email.")


class ProfileUpdateView(UpdateView):
    model = CustomUser
    fields = ['username', 'gender', 'profile_pic', 'address']
    template_name = 'authapp/profile.html'
    success_url = reverse_lazy('profile')  # Update with your success URL name
    context_object_name = 'user_profile'

    def get_object(self, queryset=None):
        return self.request.user
    

class Home(View):
    def get(self, request):
        return render(request, 'authapp/home.html')