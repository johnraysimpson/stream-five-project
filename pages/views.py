from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
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