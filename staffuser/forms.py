import os
if os.path.exists('env.py'):
    import env
from django import forms
from datetime import datetime, date, timedelta
from django.core.mail import send_mail
from accounts.models import User

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