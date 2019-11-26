from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserLoginForm, FirstPasswordChangeForm, CreateUserForm
from profiles.forms import ParentProfileForm, TutorProfileForm
from .models import User
from profiles.models import ParentProfile, Student, TutorProfile
from lessons.models import Lesson
from staffuser.views import staff_test


@login_required
def logout(request):
    """Logs out current user"""
    auth.logout(request)
    messages.success(request, "You have successfully been logged out!")
    return redirect('home')

def login_view(request):
    """A view to render the login page with the login form"""
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            login_form = UserLoginForm(request.POST)
            if login_form.is_valid():
                try:
                    user = User.objects.get(email=login_form.cleaned_data['email'])
                except User.DoesNotExist:
                    user = None
                    login_form.add_error(None, "Your username or password is incorrect.")
                if user:
                    if user.is_active:
                        try:
                            user = auth.authenticate(email=request.POST['email'],
                                            password=request.POST['password'])
                            auth.login(user=user, request=request)
                            messages.success(request, "You have successfully logged in")
                            if user.is_admin:
                                return redirect('adminuser:dashboard')
                            elif user.is_staff:
                                return redirect('staffuser:dashboard')
                            elif user.is_parent:
                                if user.password_changed:
                                    return redirect('parentuser:dashboard')
                                else:
                                    return redirect('first_password_change')
                            elif user.is_tutor:
                                if user.password_changed:
                                    return redirect('tutoruser:dashboard')
                                else:
                                    return redirect('first_password_change')
                        except:
                            login_form.add_error(None, "Your username or password is incorrect.")
                    else:
                        login_form.add_error(None, "Your account is not active, contact a member of staff to reenroll.")
        else:
            login_form = UserLoginForm()
        return render(request, 'login.html', {"login_form": login_form})
        
        
def first_password_change(request):
    """View to render a password change form for new parent or tutor users"""
    if request.method == 'POST':
        form = FirstPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            auth.update_session_auth_hash(request, user)  # Important!
            user.password_changed=True
            user.save()
            messages.success(request, 'Your password was successfully updated!')
            if request.user.is_parent:
                return redirect('parentuser:dashboard')
            elif request.user.is_tutor:
                return redirect('tutor:dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = FirstPasswordChangeForm(request.user)
    return render(request, 'first_password_change.html', {
        'form': form
    })
    
@login_required
@user_passes_test(staff_test, redirect_field_name=None, login_url='/oops/')
def add_parent_view(request):
    """Renders add parent page, creates form for registering a parent user and creating a profile"""
    if request.method=='POST':
        parent_user_form = CreateUserForm(request.POST)
        parent_profile_form = ParentProfileForm(request.POST)
        
        if parent_user_form.is_valid() and parent_profile_form.is_valid():
            user = parent_user_form.save(commit=False)
            user.parent=True
            user.centre = request.user.centre
            user.save()
            
            parent_profile = parent_profile_form.save(commit=False)
            parent_profile.user = user
            parent_profile.save()
            messages.success(request, "Parent successfully created")
            return redirect('staffuser:parent_profile', parent_id=parent_profile.id)
    else:
        parent_user_form = CreateUserForm()
        parent_profile_form = ParentProfileForm()
    return render(request, "add_parent_user.html", {'parent_user_form': parent_user_form, 'parent_profile_form': parent_profile_form})
  
#accounts 
@login_required
@user_passes_test(staff_test, redirect_field_name=None, login_url='/oops/')
def add_tutor_view(request):
    """Renders add tutor page, creates form for registering a tutor user and creating a profile"""
    if request.method == 'POST':
        
        tutor_user_form = CreateUserForm(request.POST)
        tutor_profile_form = TutorProfileForm(request.POST)
        if tutor_user_form.is_valid() and tutor_profile_form.is_valid():
            user = tutor_user_form.save()
            user.tutor=True
            user.centre = request.user.centre
            user.save()
            
            tutor_profile = tutor_profile_form.save()
            tutor_profile.user = user
            tutor_profile.save()
            messages.success(request, "Tutor successfully created")
            return redirect('staffuser:tutor_profile', tutor_id=tutor_profile.id)
    else:
        tutor_user_form = CreateUserForm()
        tutor_profile_form = TutorProfileForm()
    return render(request, "add_tutor_user.html", {'tutor_user_form': tutor_user_form, 'tutor_profile_form': tutor_profile_form})
    
@login_required
@user_passes_test(staff_test, redirect_field_name=None, login_url='/oops/')
def deactivate_user_view(request, user_id):
    """View to render a confirmation page to deactivate a user"""
    user = get_object_or_404(User, pk=user_id)
    try:
        profile = ParentProfile.objects.get(user=user)
    except ParentProfile.DoesNotExist:
        profile = TutorProfile.objects.get(user=user)
    return render(request, 'deactivate_user.html', {'user': user, 'profile': profile})
    
@login_required
@user_passes_test(staff_test, redirect_field_name=None, login_url='/oops/')
def deactivate_user_confirm_view(request, user_id):
    """View which deactivates a user and removes anything related to lessons"""
    user = get_object_or_404(User, pk=user_id)
    user.is_active=False
    user.save()
    try:
        parent_profile = ParentProfile.objects.get(user=user)
        students = Student.objects.filter(parent=parent_profile)
        for student in students:
            student.lessons.clear()
        messages.success(request, 'User '+parent_profile.first_name+' '+parent_profile.last_name+' has been deactivated.')
        return redirect('staffuser:parents')
    except ParentProfile.DoesNotExist:
        tutor_profile = TutorProfile.objects.get(user=user)
        lessons = Lesson.objects.filter(tutor=tutor_profile)
        for lesson in lessons:
            lesson.delete()
        messages.success(request, 'User '+tutor_profile.first_name+' '+tutor_profile.last_name+' has been deactivated.')
        return redirect('staffuser:tutors')
    
@login_required
@user_passes_test(staff_test, redirect_field_name=None, login_url='/oops/')
def reactivate_user_confirm_view(request, user_id):
    """View which reactivates a parent user"""
    user = get_object_or_404(User, pk=user_id)
    user.is_active=True
    user.save()
    messages.success(request, 'This user has been reactivated.')
    try:
        parent_profile = ParentProfile.objects.get(user=user)
        return redirect('staffuser:parents')
    except ParentProfile.DoesNotExist:
        tutor_profile = TutorProfile.objects.get(user=user)
        return redirect('staffuser:tutors')
    
@login_required
@user_passes_test(staff_test, redirect_field_name=None, login_url='/oops/')
def delete_user_view(request, user_id):
    """View to render a confirmation page to permenantly delete a parent user"""
    user_for_deletion = get_object_or_404(User, pk=user_id)
    try:
        user_profile = ParentProfile.objects.get(user=user_for_deletion)
    except ParentProfile.DoesNotExist:
        user_profile = TutorProfile.objects.get(user=user_for_deletion)
    return render(request, 'delete_user.html', {'user_for_deletion': user_for_deletion, 'user_profile': user_profile})

@login_required
@user_passes_test(staff_test, redirect_field_name=None, login_url='/oops/')
def delete_user_confirm_view(request, user_id):
    """View which permenantly deletes a user"""
    user = get_object_or_404(User, pk=user_id)
    try:
        user_profile = ParentProfile.objects.get(user=user)
        user.delete()
        messages.success(request, 'The user was permenantly deleted.')
        return redirect('staffuser:parents')
    except ParentProfile.DoesNotExist:
        user_profile = TutorProfile.objects.get(user=user)
        user.delete()
        messages.success(request, 'The user was permenantly deleted.')
        return redirect('staffuser:tutors')