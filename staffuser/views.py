from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse
from datetime import datetime, date, timedelta
from .forms import ParentUserForm, ParentProfileForm, TutorUserForm, TutorProfileForm, StudentForm
from lessons.forms import TutorOccurrenceSessionForm, SessionMatchForm
from accounts.models import User
from lessons.models import TutorSession, StudentSession
from .models import ParentProfile, TutorProfile
from django.contrib.auth.decorators import login_required, user_passes_test


def staff_test(user):
    """Test to check if current user is solely a staff user"""
    return (user.is_staff and not user.is_admin)
    
def get_next_august():
    """Function that returns the date of the next time it is August"""
    today = datetime.today()
    year = today.year
    month = today.month
    if month >= 8:
        year += 1
    return date(year, 8, 1)
    
def get_mondays_date():
    todays_date=date.today()
    mondays_date=todays_date - timedelta(days=todays_date.weekday())
    return mondays_date

@login_required
@user_passes_test(staff_test, redirect_field_name=None, login_url='/oops/')
def staff_dashboard_view(request):
    """Renders dashboard for staff user"""
    mondays_date = get_mondays_date()
    return render(request, "staff-dashboard.html", {'mondays_date': mondays_date})

@login_required
@user_passes_test(staff_test, redirect_field_name=None, login_url='/oops/')
def add_parent_view(request):
    """Renders add parent page, creates form for registering a parent user"""
    parent_user_form = ParentUserForm(request.POST or None)
    if parent_user_form.is_valid():
        user = parent_user_form.save()
        user.parent=True
        user.centre = request.user.centre
        user.save()
        return redirect('staffuser:add-parent-profile', parentuser_id=user.pk)
    return render(request, "add-parent-user.html", {'parent_user_form': parent_user_form})
    
@login_required
@user_passes_test(staff_test, redirect_field_name=None, login_url='/oops/')
def add_parent_profile_view(request, parentuser_id):
    """Renders page for parent profile information, using the user id to retrieve information about the parent user created"""
    parentuser = User.objects.get(pk=parentuser_id)
    try:
        ParentProfile.objects.get(user=parentuser)
        return HttpResponse('This user already has a profile')
    except ParentProfile.DoesNotExist:
        parent_profile_form = ParentProfileForm(request.POST or None)
        if parent_profile_form.is_valid():
            parent_profile = parent_profile_form.save()
            parent_profile.user = parentuser
            parent_profile.save()
            messages.success(request, "Parent successfully created")
            return redirect(reverse('staffuser:dashboard'))
        return render(request, 'add-parent-profile.html', {'parentuser': parentuser, "parent_profile_form": parent_profile_form})
    
@login_required
@user_passes_test(staff_test, redirect_field_name=None, login_url='/oops/')
def add_tutor_view(request):
    """Renders add tutor page, creates form for registering a tutor user"""
    tutor_user_form = TutorUserForm(request.POST or None)
    if tutor_user_form.is_valid():
        user = tutor_user_form.save()
        user.tutor=True
        user.centre = request.user.centre
        user.save()
        return redirect('staffuser:add-tutor-profile', tutoruser_id=user.pk)
    return render(request, "add-tutor-user.html", {'tutor_user_form': tutor_user_form})
    
@login_required
@user_passes_test(staff_test, redirect_field_name=None, login_url='/oops/')
def add_tutor_profile_view(request, tutoruser_id):
    """Renders page for parent profile information, using the user id to retrieve information about the parent user created"""
    tutoruser = User.objects.get(pk=tutoruser_id)
    try:
        TutorProfile.objects.get(user=tutoruser)
    except TutorProfile.DoesNotExist:
        tutor_profile_form = TutorProfileForm(request.POST or None)
        if tutor_profile_form.is_valid():
            tutor_profile = tutor_profile_form.save()
            tutor_profile.user = tutoruser
            tutor_profile.save()
            messages.success(request, "Tutor successfully created")
            return redirect(reverse('staffuser:dashboard'))
        return render(request, 'add-tutor-profile.html', {'tutoruser': tutoruser, "tutor_profile_form": tutor_profile_form})



@login_required
@user_passes_test(staff_test, redirect_field_name=None, login_url='/oops/')
def add_tutor_session_view(request):
    """Renders add session page with corresponding form"""
    tutor_session_form = TutorOccurrenceSessionForm(request.POST or None)
    if tutor_session_form.is_valid():
        if tutor_session_form.cleaned_data['occurrence'] == 'weekly':
            start_date = tutor_session_form.cleaned_data['date']
            while start_date < get_next_august():
                TutorSession.objects.create(tutor=tutor_session_form.cleaned_data['tutor'], 
                                        subject=tutor_session_form.cleaned_data['subject'], 
                                        day=tutor_session_form.cleaned_data['day'], 
                                        time=tutor_session_form.cleaned_data['time'], 
                                        date=start_date, 
                                        duration=tutor_session_form.cleaned_data['duration'],
                                        centre=request.user.centre)
                start_date += timedelta(days=7)
        else:
            tutor_session = tutor_session_form.save()
            tutor_session.centre = request.user.centre
            tutor_session.save()
        tutor_session_form = TutorOccurrenceSessionForm()
    return render(request, 'add-tutor-session.html', {'tutor_session_form': tutor_session_form})
    
@login_required
@user_passes_test(staff_test, redirect_field_name=None, login_url='/oops/')
def add_student_view(request):
    """Renders add student page and form"""
    if request.method == 'POST':
        student_form = StudentForm(request.POST, request=request)
        if student_form.is_valid():
            student_form.save()
            student_form = StudentForm(request=request)
    else:
        student_form = StudentForm(request=request)
    return render(request, 'add-student.html', {'student_form': student_form})
    
@login_required
@user_passes_test(staff_test, redirect_field_name=None, login_url='/oops/')
def add_student_session_view(request):
    if request.method == "POST":
        session_form = SessionMatchForm(request.POST, request=request)
        if session_form.is_valid():
            
                start_date = session_form.cleaned_data['date']
                matched_sessions = []
                
                while start_date < get_next_august():
                    
                    try: 
                        matched_session = TutorSession.objects.get(tutor = session_form.cleaned_data['tutor'],
                                                                day = session_form.cleaned_data['day'],
                                                                time = session_form.cleaned_data['time'],
                                                                subject = session_form.cleaned_data['subject'],
                                                                date = start_date,
                                                                )
                    except TutorSession.DoesNotExist:
                        matched_session = None
                        
                    if matched_session:
                        matched_sessions.append(matched_session)
                        
                    if session_form.cleaned_data['occurrence'] == 'one_off':
                        break
                    
                    elif session_form.cleaned_data['occurrence'] == 'weekly':
                        start_date += timedelta(days=7)
                        
                    else:
                        start_date += timedelta(days=14)
                        
                if not matched_sessions:
                    session_form.add_error(None, 'Sessions do not exist')
                else:
                    session, created = StudentSession.objects.get_or_create(
                        student = session_form.cleaned_data['student']
                        )
                    for newsession in matched_sessions:
                        session.sessions.add(newsession)
                    print(session.sessions.all())
                    session_form = SessionMatchForm(request=request)
    else:
        session_form = SessionMatchForm(request=request)
    return render(request, 'add-student-session.html', {'session_form': session_form})
    
@login_required
@user_passes_test(staff_test, redirect_field_name=None, login_url='/oops/')
def get_lessons_view(request, mondays_date):
    """View to retrieve sessions on a weekly basis"""
    try:
        view_date = datetime.strptime(mondays_date, "%Y-%m-%d")
        if view_date.weekday() == 0:
            sundays_date = view_date + timedelta(days=6)
            this_weeks_lessons = TutorSession.objects.filter(date__gte=mondays_date,
                                                                date__lt=sundays_date)
            days_of_the_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
            next_week = (view_date + timedelta(days=7)).date
            previous_week = (view_date - timedelta(days=7)).date
            print(view_date.strftime("%A"))
            return render(request, 'get-sessions.html', {'lessons': this_weeks_lessons, 
                                                        'days_of_the_week': days_of_the_week, 
                                                        'view_date': view_date, 
                                                        'next_week': next_week, 
                                                        'previous_week': previous_week}
                                                        )
        else:
            return render(request, 'get-sessions.html', {"wrong_view_date": True})
    except:
        return render(request, 'get-sessions.html', {"wrong_view_date": True})
    
