from django import forms

class UserLoginForm(forms.Form):
    """Form for logging in users"""
    username = forms.CharField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput)