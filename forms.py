from django import forms
from .models import Client

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['username', 'email', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) > 128:
            raise forms.ValidationError("Password must be 128 characters or fewer.")
        return password

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Client.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Client.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email
