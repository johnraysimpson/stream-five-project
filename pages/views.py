from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm
from adminuser.models import Centre

# Create your views here.
def home_view(request):
    """Renders home page"""
    page = {
        'page_title': 'Home'
    }
    return render(request, 'index.html', page)
    
def about_view(request):
    """Renders about page"""
    page = {
        'page_title': 'About'
    }
    return render(request, 'about.html', page)
    
def contact_view(request):
    """Renders contact page"""
    centres = Centre.objects.all()
    context = {
        'page_title': 'Contact',
        'centres': centres
    }
    return render(request, 'contact.html', context)
    
@login_required
def logout(request):
    """Logs out current user"""
    auth.logout(request)
    messages.success(request, "You have successfully been logged out!")
    return redirect(reverse('home'))
    
def login_view(request):
    """Renders login page"""
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)
        
        if login_form.is_valid():
            user = auth.authenticate(username=request.POST['username'],
                                    password=request.POST['password'])
            messages.success(request, "You have successfully logged in")
            if user:
                auth.login(user=user, request=request)
                if user.is_superuser:
                    return redirect(reverse('adminuser:dashboard'), {'user': user, "page_title": "admin"})
                else:
                    return redirect(reverse('home'))
            else:
                login_form.add_error(None, "Your username or password is incorrect.")
    else:
        login_form = UserLoginForm()
    return render(request, 'login.html', {"login_form": login_form, "page_title": "Login"})