from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from datetime import datetime, date, timedelta
from .forms import ParentUserForm, ParentProfileForm, TutorUserForm, TutorProfileForm, TutorOccurrenceSessionForm
from accounts.models import User
from .models import TutorSession


# Create your views here.
def staff_dashboard_view(request):
    """Renders dashboard for staff user"""
    return render(request, "staff-dashboard.html")
    
def add_parent_profile_view(request, *args, **kwargs):
    """Renders page for parent profile information, using the user id to retrieve information about the parent user created"""
    parentuser = User.objects.get(pk=kwargs["parentuser_id"])
    parent_profile_form = ParentProfileForm(request.POST or None)
    if parent_profile_form.is_valid():
        parent_profile = parent_profile_form.save()
        parent_profile.user = parentuser
        parent_profile.save()
        messages.success(request, "Parent successfully created")
        return redirect(reverse('staffuser:dashboard'))
    return render(request, 'add-parent-profile.html', {'parentuser': parentuser, "parent_profile_form": parent_profile_form})

def add_parent_view(request):
    """Renders add parent page, creates form for registering a parent user"""
    parent_user_form = ParentUserForm(request.POST or None)
    if parent_user_form.is_valid():
        user = parent_user_form.save()
        user.parent=True
        user.centre = request.user.centre
        user.save()
        return redirect(reverse('staffuser:add-parent-profile', kwargs={"parentuser_id":user.pk}))
    return render(request, "add-parent-user.html", {'parent_user_form': parent_user_form})
    
    
def add_tutor_view(request):
    """Renders add tutor page, creates form for registering a tutor user"""
    tutor_user_form = TutorUserForm(request.POST or None)
    if tutor_user_form.is_valid():
        user = tutor_user_form.save()
        user.tutor=True
        user.centre = request.user.centre
        user.save()
        return redirect(reverse('staffuser:add-tutor-profile', kwargs={"tutoruser_id":user.pk}))
    return render(request, "add-tutor-user.html", {'tutor_user_form': tutor_user_form})
    
def add_tutor_profile_view(request, *args, **kwargs):
    """Renders page for parent profile information, using the user id to retrieve information about the parent user created"""
    tutoruser = User.objects.get(pk=kwargs["tutoruser_id"])
    tutor_profile_form = TutorProfileForm(request.POST or None)
    if tutor_profile_form.is_valid():
        tutor_profile = tutor_profile_form.save()
        tutor_profile.user = tutoruser
        tutor_profile.save()
        messages.success(request, "Tutor successfully created")
        return redirect(reverse('staffuser:dashboard'))
    return render(request, 'add-tutor-profile.html', {'tutoruser': tutoruser, "tutor_profile_form": tutor_profile_form})
    
def add_tutor_session_view(request):
    """Renders add session page with corresponding form"""
    tutor_session_form = TutorOccurrenceSessionForm(request.POST or None)
    if tutor_session_form.is_valid():
        if tutor_session_form.cleaned_data['occurrence'] == 'weekly':
            start_date = tutor_session_form.cleaned_data['date']
            while start_date < date(2020, 8, 1):
                TutorSession.objects.create(tutor=tutor_session_form.cleaned_data['tutor'], 
                                        subject=tutor_session_form.cleaned_data['subject'], 
                                        day=tutor_session_form.cleaned_data['day'], 
                                        time=tutor_session_form.cleaned_data['time'], 
                                        date=start_date, 
                                        duration=tutor_session_form.cleaned_data['duration'])
                start_date += timedelta(days=7)
        else:
            tutor_session_form.save()
        tutor_session_form = TutorOccurrenceSessionForm()
    return render(request, 'add-tutor-session.html', {'tutor_session_form': tutor_session_form})