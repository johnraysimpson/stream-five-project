import os
if os.path.exists('env.py'):
    import env
from django import forms
from django.core.mail import send_mail
from django.contrib.auth.forms import ReadOnlyPasswordHashField, SetPasswordForm
from .models import User
from collections import OrderedDict

class UserLoginForm(forms.Form):
    """Form for logging in users"""
    email = forms.CharField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput)
    
class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on the user, but replaces the password field with admin's password hash display field."""
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
        
class FirstPasswordChangeForm(SetPasswordForm):
    """A form that makes user change their password on their first time logging in"""
    def __init__(self, *args, **kwargs):
        super(FirstPasswordChangeForm, self).__init__(*args, **kwargs)

        for fieldname in ['new_password1', 'new_password2']:
            self.fields[fieldname].help_text = None

FirstPasswordChangeForm.base_fields = OrderedDict(
    (k, FirstPasswordChangeForm.base_fields[k])
    for k in ['new_password1', 'new_password2']
)

class CreateUserForm(forms.ModelForm):
    """Form for creating a parent or tutor user. Assigns a random password and an email is sent to the user with this information"""
    class Meta:
        model = User
        fields = ('email',)
        
    def clean_email(self):
        return self.cleaned_data['email'].lower()
    
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(CreateUserForm, self).save(commit=False)
        password = User.objects.make_random_password(length=10, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
        print(password)
        # send_mail(
        #         "Welcome to Zephyr Tuition",
        #         ("Hello "+user.email+",\n\nYou have been registered to our website, your randomly generated password is\n\n"
        #         +password+"\n\nYou will be required to change your password when you first login with your email address.\n\nThank you for choosing us as a tutoring company.\n\nThe Zephyr Team"),
        #         os.environ.get('EMAIL_ADDRESS'),
        #         [user.email]
        #         )
        user.set_password(password)
        if commit:
            user.save()
        return user