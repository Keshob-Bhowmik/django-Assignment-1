from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Group, Permission
import re
from event.forms import StyledForMixin

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'email']
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        for fieldName in ['username', 'password1', 'password2']:
            self.fields[fieldName].help_text = None


class CustomRegistrationForm(StyledForMixin,forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'confirm_password', 'email']
    
    def clean_password1(self):
        errors = []
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            errors.append("The password length must be 8 or more")

        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).+$'
        if not re.match(pattern, password1):
            errors.append("Password must contain uppercase, lowercase, number, and special character")
        
        if errors:
            raise forms.ValidationError(errors)
        
        return password1
    

    def clean_email(self):
        errors = []
        email = self.cleaned_data.get('email')
        user_email = User.objects.filter(email=email)
        if user_email.exists():
            errors.append("the email is already used")
        if errors:
            raise forms.ValidationError(errors)
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        confirm_password = cleaned_data.get('confirm_password')
        if password1 != confirm_password:
            raise forms.ValidationError("password do not match")
        return cleaned_data

    

class LoginForm(StyledForMixin,AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)