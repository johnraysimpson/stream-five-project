import os
if os.path.exists('env.py'):
    import env
from django import forms
from datetime import datetime, date, timedelta
from django.core.mail import send_mail
from accounts.models import User
from .models import ParentProfile, TutorProfile, Student

class ParentUserForm(forms.ModelForm):
    """Form for creating a parent user. Assigns a random password and an email is sent to the user with this information"""
    class Meta:
        model = User
        fields = ('email',)
        
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(ParentUserForm, self).save(commit=False)
        password = User.objects.make_random_password(length=10, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
        print(password)
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
    """A form for adding profile information for the parent user that had been created on the previous page"""
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
            
class TutorUserForm(forms.ModelForm):
    """Form for creating a parent user. Assigns a random password and an email is sent to the user with this information"""
    class Meta:
        model = User
        fields = ('email',)
        
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(TutorUserForm, self).save(commit=False)
        password = User.objects.make_random_password(length=10, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
        print(password)
        send_mail(
                "Welcome to Zephyr Tuition",
                ("Hello "+user.email+",\n\nYou have been registered to our website, your randomly generated password is\n\n"
                +password+"\n\nYou will be required to change your password when you first login with your email address.\n\nThank you for choosing to work with us.\n\nThe Zephyr Team"),
                os.environ.get('EMAIL_ADDRESS'),
                [user.email]
                )
        user.set_password(password)
        if commit:
            user.save()
        return user
        
class TutorProfileForm(forms.ModelForm):
    """A form for adding profile information for the parent user that had been created on the previous page"""
    address1 = forms.CharField(label='Address Line 1')
    address2 = forms.CharField(label='Address Line 2', required=False)
    pay_per_hour = forms.CharField(label="Hourly rate (£)")
    class Meta:
        model = TutorProfile
        fields = (
            'first_name',
            'last_name',
            'address1',
            'address2',
            'town_or_city',
            'county',
            'post_code',
            'telephone',
            'pay_per_hour',
            )
            
        
class StudentForm(forms.ModelForm):
    """Form for creating a student"""
    parent = forms.ModelChoiceField(queryset=None, empty_label="Choose parent user", required=True)
    date_of_birth = forms.DateField(
        widget=forms.DateInput(format='%d/%m/%Y'),
        input_formats=('%d/%m/%Y', )
        )
    relationship = forms.CharField(label="Relationship to Student")
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields["parent"].queryset = ParentProfile.objects.filter(user__centre = self.request.user.centre)
    class Meta:
        model = Student
        fields = ('parent', 'relationship', 'first_name', 'last_name', 'date_of_birth', 'price_per_session', 'notes')