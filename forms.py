from django import forms
from .models import Client
from django.utils.translation import gettext_lazy as _

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['username', 'email', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError(_("Password must be at least 8 characters long."))
        return password

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Check for case-insensitive username
        if Client.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError(_("Username already exists."))
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Check for case-insensitive email
        if Client.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(_("Email already exists."))
        return email


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label='Username', required=True)
    password = forms.CharField(widget=forms.PasswordInput, label='Password', required=True)