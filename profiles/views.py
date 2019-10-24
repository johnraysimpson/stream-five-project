from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from staffuser.views import staff_test
from lessons.views import get_next_august
from accounts.models import User
from .models import Student, ParentProfile, TutorProfile
from django.http import HttpResponse
from datetime import datetime, date, timedelta
from .forms import ParentProfileForm, TutorProfileForm, StudentForm

def get_next_september():
    """Function that returns the date of the next time it is September"""
    today = datetime.today()
    year = today.year
    month = today.month
    if month >= 9:
        year += 1
    return date(year, 9, 1)

def get_year_group(date):
    age = (get_next_september() - date).days // 365.5
    year_group = int(age - 5)
    print(year_group)
    return year_group

# Create your views here.
@login_required
@user_passes_test(staff_test, redirect_field_name=None, login_url='/oops/')
def add_parent_profile_view(request, parentuser_id):
    """Renders page for parent profile information, using the user id to retrieve information about the parent user created"""
    parentuser = User.objects.get(pk=parentuser_id)
    try:
        if parentuser.is_parent:
            ParentProfile.objects.get(user=parentuser)
            return render(request, 'add-parent-profile.html', {'parentuser': parentuser, "parent_profile_exists": True})
        else:
            return redirect('staffuser:dashboard')
    except ParentProfile.DoesNotExist:
        parent_profile_form = ParentProfileForm(request.POST or None)
        if parent_profile_form.is_valid():
            parent_profile = parent_profile_form.save()
            parent_profile.user = parentuser
            parent_profile.save()
            messages.success(request, "Parent successfully created")
            return redirect('staffuser:add-student', parent_id = parent_profile.id)
        return render(request, 'add-parent-profile.html', {'parentuser': parentuser, "parent_profile_form": parent_profile_form})
        
@login_required
@user_passes_test(staff_test, redirect_field_name=None, login_url='/oops/')
def add_tutor_profile_view(request, tutoruser_id):
    """Renders page for parent profile information, using the user id to retrieve information about the parent user created"""
    tutoruser = User.objects.get(pk=tutoruser_id)
    try:
        if tutoruser.is_tutor:
            TutorProfile.objects.get(user=tutoruser)
            return render(request, 'add-tutor-profile.html', {'tutoruser': tutoruser, "tutor_profile_exists": True})
        else:
            return redirect('staffuser:dashboard')
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
def add_student_view(request, parent_id):
    """Renders add student page and form"""
    parent = ParentProfile.objects.get(id=parent_id)
    if request.method == 'POST':
        student_form = StudentForm(request.POST)
        if student_form.is_valid():
            student = student_form.save()
            student.parent = parent
            student.save()
            return redirect('staffuser:student-profile', student_id=student.id)
    else:
        student_form = StudentForm()
    return render(request, 'add-student.html', {'student_form': student_form, 'parent': parent})
    
@login_required
@user_passes_test(staff_test, redirect_field_name=None, login_url='/oops/')
def update_student_view(request, student_id):
    """Renders page for displaying profile information about a parent user"""
    student = Student.objects.get(id=student_id)
    if request.method == 'POST':
        student_form = StudentForm(request.POST, instance=student)
        if student_form.is_valid():
            student_form.save()
            return redirect('staffuser:student-profile', student_id=student_id)
    else:
        student_form = StudentForm(instance=student)
    return render(request, 'update-student.html', {'student_form': student_form})
    
@login_required
@user_passes_test(staff_test, redirect_field_name=None, login_url='/oops/')
def get_parent_profile_view(request, parent_id):
    """Renders page for displaying profile information about a parent user"""
    parent = ParentProfile.objects.get(id=parent_id)
    students = Student.objects.filter(parent=parent)
    return render(request, 'get-parent-profile.html', {'parent': parent, 'students': students})
    
@login_required
@user_passes_test(staff_test, redirect_field_name=None, login_url='/oops/')
def update_parent_profile_view(request, parent_id):
    """Renders page for displaying profile information about a parent user"""
    parentprofile = ParentProfile.objects.get(id=parent_id)
    if request.method == 'POST':
        parent_profile_form = ParentProfileForm(request.POST, instance=parentprofile)
        if parent_profile_form.is_valid():
            parent_profile_form.save()
            return redirect('staffuser:parent-profile', parent_id=parent_id)
    else:
        parent_profile_form = ParentProfileForm(instance=parentprofile)
    return render(request, 'update-parent-profile.html', {'parent_profile_form': parent_profile_form})
    
@login_required
@user_passes_test(staff_test, redirect_field_name=None, login_url='/oops/')
def get_student_profile_view(request, student_id):
    """Renders page for displaying profile information about a parent user"""
    student = Student.objects.get(id=student_id)
    parent = ParentProfile.objects.get(student=student)
    year_group = get_year_group(student.date_of_birth)
    return render(request, 'get-student-profile.html', {'parent': parent, 'student': student, 'year_group': year_group})
    
@login_required
@user_passes_test(staff_test, redirect_field_name=None, login_url='/oops/')
def delete_student_view(request, student_id):
    student = Student.objects.get(id=student_id)
    return render(request, 'delete-student.html', {'student': student})
    
@login_required
@user_passes_test(staff_test, redirect_field_name=None, login_url='/oops/')
def delete_student_confirm_view(request, student_id):
    Student.objects.get(pk=student_id).delete()
    messages.success(request, 'The student was permenantly deleted.')
    return redirect('staffuser:students')