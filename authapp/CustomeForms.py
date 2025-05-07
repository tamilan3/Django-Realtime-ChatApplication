from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser

class EmailAuthenticationForm(AuthenticationForm):
    """Form for email-based authentication."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Change the label to 'Email'
        self.fields['username'].label = 'Email'


class CustomUserCreationForm(UserCreationForm):
    """Form for creating new users."""
    
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'gender', 'profile_pic', 'address')
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'profile_pic': forms.FileInput(attrs={'class': 'form-control-file'})
        }

    def clean_profile_pic(self):
        """Validate profile picture upload."""
        profile_pic = self.cleaned_data.get('profile_pic')
        if profile_pic:
            # Check file size (max 5MB)
            if profile_pic.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image file too large ( > 5MB )")
            
            # Check file type
            allowed_types = ['image/jpeg', 'image/png', 'image/gif']
            if profile_pic.content_type not in allowed_types:
                raise forms.ValidationError("Please upload a valid image file (JPEG, PNG, or GIF)")
            
        return profile_pic
