from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from profiles.models import ParentProfile

# Create your views here.
def parent_test(user):
    """Test to check if the user is a parent"""
    return user.is_parent
    
@login_required
@user_passes_test(parent_test, redirect_field_name=None, login_url='/oops/')
def parent_dashboard_view(request):
    """View to render the parent dashboard"""
    parent = ParentProfile.objects.get(user=request.user)
    return render(request, 'parent_dashboard.html', {'parent': parent})