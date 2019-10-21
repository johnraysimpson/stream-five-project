from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm, FirstPasswordChangeForm
from .models import User

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