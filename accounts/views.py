from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserLoginForm, FirstPasswordChangeForm, CreateUserForm
from .models import User
from profiles.models import ParentProfile, Student
from staffuser.views import staff_test

# Create your views here.

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
                    if user.is_active:
                        user = auth.authenticate(email=request.POST['email'],
                                                password=request.POST['password'])
                        if user:
                                auth.login(user=user, request=request)
                                messages.success(request, "You have successfully logged in")
                                if user.is_admin:
                                    return redirect('adminuser:dashboard')
                                elif user.is_staff:
                                    return redirect('staffuser:dashboard')
                                elif user.is_parent:
                                    if user.password_changed:
                                        return redirect('home')
                                    else:
                                        return redirect('first_password_change')
                    else:
                        login_form.add_error(None, 'Your account is not active, contact a member of staff to reenroll')
                except User.DoesNotExist:
                    login_form.add_error(None, "Your username or password is incorrect.")
        else:
            login_form = UserLoginForm()
        return render(request, 'login.html', {"login_form": login_form})
        
        
def first_password_change(request):
    if request.method == 'POST':
        form = FirstPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            auth.update_session_auth_hash(request, user)  # Important!
            user.password_changed=True
            user.save()
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
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
    """Renders add parent page, creates form for registering a parent user"""
    parent_user_form = CreateUserForm(request.POST or None)
    if parent_user_form.is_valid():
        user = parent_user_form.save()
        user.parent=True
        user.centre = request.user.centre
        user.save()
        return redirect('staffuser:add-parent-profile', parentuser_id=user.pk)
    return render(request, "add-parent-user.html", {'parent_user_form': parent_user_form})
  
#accounts 
@login_required
@user_passes_test(staff_test, redirect_field_name=None, login_url='/oops/')
def add_tutor_view(request):
    """Renders add tutor page, creates form for registering a tutor user"""
    tutor_user_form = CreateUserForm(request.POST or None)
    if tutor_user_form.is_valid():
        user = tutor_user_form.save()
        user.tutor=True
        user.centre = request.user.centre
        user.save()
        return redirect('staffuser:add-tutor-profile', tutoruser_id=user.pk)
    return render(request, "add-tutor-user.html", {'tutor_user_form': tutor_user_form})
    
@login_required
@user_passes_test(staff_test, redirect_field_name=None, login_url='/oops/')
def deactivate_user_view(request, user_id):
    parent_user = User.objects.get(pk=user_id)
    parent_profile = ParentProfile.objects.get(user=parent_user)
    return render(request, 'deactivate-user.html', {'parent_user': parent_user, 'parent_profile': parent_profile})
    
@login_required
@user_passes_test(staff_test, redirect_field_name=None, login_url='/oops/')
def deactivate_user_confirm_view(request, user_id):
    user = User.objects.get(pk=user_id)
    parent_profile = parent_profile = ParentProfile.objects.get(user=user)
    user.active=False
    user.save()
    students = Student.objects.filter(parent=parent_profile)
    for student in students:
        student.lessons.clear()
    messages.success(request, 'User '+parent_profile.first_name+' '+parent_profile.last_name+' has been deactivated.')
    return redirect('staffuser:parents')
    
@login_required
@user_passes_test(staff_test, redirect_field_name=None, login_url='/oops/')
def reactivate_user_confirm_view(request, user_id):
    user = User.objects.get(pk=user_id)
    parent_profile = parent_profile = ParentProfile.objects.get(user=user)
    user.active=True
    user.save()
    messages.success(request, 'This user has been reactivated.')
    return redirect('staffuser:parent-profile', parent_id=parent_profile.id)
    
@login_required
@user_passes_test(staff_test, redirect_field_name=None, login_url='/oops/')
def delete_user_view(request, user_id):
    parent_user = User.objects.get(pk=user_id)
    parent_profile = ParentProfile.objects.get(user=parent_user)
    return render(request, 'delete-user.html', {'parent_user': parent_user, 'parent_profile': parent_profile})

@login_required
@user_passes_test(staff_test, redirect_field_name=None, login_url='/oops/')
def delete_user_confirm_view(request, user_id):
    User.objects.get(pk=user_id).delete()
    messages.success(request, 'The user was permenantly deleted.')
    return redirect('staffuser:parents')