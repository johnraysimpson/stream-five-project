from django.shortcuts import render

# Create your views here.
def home_view(request):
    """Renders home page"""
    return render(request, 'index.html')
    
def about_view(request):
    """Renders about page"""
    return render(request, 'about.html')
    
def contact_view(request):
    """Renders contact page"""
    return render(request, 'contact.html')
    
def login_view(request):
    """Renders login page"""
    return render(request, 'login.html')