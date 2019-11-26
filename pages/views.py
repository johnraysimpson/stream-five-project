from django.shortcuts import render
from adminuser.models import Centre


def home_view(request):
    """Renders home page"""
    return render(request, 'index.html')
    
def about_view(request):
    """Renders about page"""
    no_of_centres = Centre.objects.all().count()
    return render(request, 'about.html', {'no_of_centres': no_of_centres})
    
def contact_view(request):
    """Renders contact page and retrieves information about all centres in the database"""
    centres = Centre.objects.all()
    return render(request, 'contact.html', {'centres': centres})
    
def oops_view(request):
    "Renders a page for when a user doesn't have a particular permission to view a page"
    return render(request, 'oops.html')