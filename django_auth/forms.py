from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class PasswordResetConfirmationForm(UserCreationForm):
    password1 = forms.CharField(label="Password", widget = forms.PasswordInput)
    password2 = forms.CharField(
        label="Password Confirmation",
        widget = forms.PasswordInput)
        
    class Meta:
        model = User
        fields = ['password1', 'password2']
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if not password1 or not password2:
            raise forms.ValidationError("Please confirm the email address!")
        if password1 != password2:
            raise forms.ValidationError("Passwords must match!")
        return password2