from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from staffuser.views import staff_test
from accounts.models import User
from .models import Student, ParentProfile, TutorProfile
from django.http import HttpResponse
from .forms import ParentProfileForm, TutorProfileForm, StudentForm

# Create your views here.
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