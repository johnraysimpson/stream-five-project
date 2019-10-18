import os
if os.path.exists('env.py'):
    import env
from django import forms
from datetime import datetime, date, timedelta
from django.core.mail import send_mail
from accounts.models import User
from .models import ParentProfile, TutorProfile, TutorSession

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
            
class TutorSessionForm(forms.ModelForm):
    """Form for creating a tutor session"""
    DAY_CHOICES = [('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'), ('thursday', 'Thursday'), ('friday', 'Friday'), ('saturday', 'Saturday')]
    SUBJECT_CHOICES = [('maths', 'Maths'), ('english', 'English'), ('science', 'Science')]
    tutor = forms.ModelChoiceField(queryset=TutorProfile.objects.all(), empty_label="Choose Tutor", required=True)
    day = forms.ChoiceField(choices=DAY_CHOICES)
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES)
    time = forms.TimeField(widget=forms.TimeInput(format="%H:%M"))
    date = forms.DateField(label="Start date",
        widget=forms.DateInput(format='%d/%m/%Y'),
        input_formats=('%d/%m/%Y', )
        )
    
    class Meta:
        model = TutorSession
        fields = (
            'tutor',
            'subject',
            'day',
            'time',
            'date',
            'duration'
            )

class TutorOccurrenceSessionForm(TutorSessionForm):
    """Form that includes occurrence field to TutorSessionForm"""
    OCCURRENCE_CHOICES = [('one_off', 'One Off'), ('weekly', 'Weekly')]
    occurrence = forms.ChoiceField(choices=OCCURRENCE_CHOICES, widget=forms.RadioSelect)
    class Meta(TutorSessionForm.Meta):
        fields = TutorSessionForm.Meta.fields + ('occurrence', )