from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from adminuser.models import Centre

# Create your views here.
def home_view(request):
    """Renders home page"""
    return render(request, 'index.html')
    
def about_view(request):
    """Renders about page"""
    return render(request, 'about.html')
    
def contact_view(request):
    """Renders contact page and sends information about all centres in the database"""
    centres = Centre.objects.all()
    return render(request, 'contact.html', {'centres': centres})
    
def oops_view(request):
    "Renders a page for when a user doesn't have a particular permission to view a page"
    return render(request, 'oops.html')