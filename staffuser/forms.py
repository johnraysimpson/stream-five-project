import os
if os.path.exists('env.py'):
    import env
from django import forms
from django.core.mail import send_mail
from accounts.models import User
from .models import ParentProfile

class ParentUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)
        
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(ParentUserForm, self).save(commit=False)
        password = User.objects.make_random_password(length=10, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
        print(password) #delete this when email is set up
        send_mail(
                "Welcome to Zephyr Tuition",
                ("Hello "+user.email+",\n\nYou have been registered to our website, your randomly generated password is\n\n"
                +password+"\n\nYou will be required to change your password when you first login with your email address.\n\nThank you for choosing us as a tutoring company.\n\nThe Zephyr Team"),
                os.environ.get('EMAIL_ADDRESS'),
                [user.email]
                )
        user.set_password(password)
        if commit:
            user.save()
        return user
        
class ParentProfileForm(forms.ModelForm):
    address1 = forms.CharField(label='Address Line 1')
    address2 = forms.CharField(label='Address Line 2', required=False)
    class Meta:
        model = ParentProfile
        fields = (
            'first_name',
            'last_name',
            'address1',
            'address2',
            'town_or_city',
            'county',
            'post_code',
            'telephone',
            )