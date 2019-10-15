from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import ParentUserForm, ParentProfileForm
from accounts.models import User


# Create your views here.
def staff_dashboard_view(request):
    """Renders dashboard for staff user"""
    return render(request, "staff-dashboard.html")
    
def add_parent_profile_view(request, *args, **kwargs):
    """Renders page for parent profile information, using the user id to retrieve information about the parent user created"""
    parentuser = User.objects.get(pk=kwargs["parentuser_id"])
    parent_profile_form = ParentProfileForm(request.POST or None)
    if parent_profile_form.is_valid():
        parent_profile = parent_profile_form.save()
        parent_profile.user = parentuser
        parent_profile.save()
        messages.success(request, "Parent successfully created")
        return redirect(reverse('staffuser:dashboard'))
    return render(request, 'add-parent-profile.html', {'parentuser': parentuser, "parent_profile_form": parent_profile_form})

def add_parent_view(request):
    """Renders add parent page, creates form for registering a parent user"""
    parent_user_form = ParentUserForm(request.POST or None)
    if parent_user_form.is_valid():
        user = parent_user_form.save()
        user.parent=True
        user.centre = request.user.centre
        user.save()
        return redirect(reverse('staffuser:add-parent-profile', kwargs={"parentuser_id":user.pk}))
    return render(request, "add-parent-user.html", {'parent_user_form': parent_user_form})