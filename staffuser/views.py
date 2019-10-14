from django.shortcuts import render, redirect, reverse
from .forms import ParentUserForm
from accounts.models import User

# Create your views here.
def staff_dashboard_view(request):
    """Renders dashboard for admin user"""
    return render(request, "staff-dashboard.html", {"page_title": "staff"})
    
def add_parent_profile_view(request, *args, **kwargs):
    print(kwargs)
    parentuser = User.objects.get(pk=kwargs["parentuser_id"])
    return render(request, 'add-parent-profile.html', {'parentuser': parentuser})

def add_parent_view(request):
    """Renders dashboard for admin user"""
    parent_user_form = ParentUserForm(request.POST or None)
    if parent_user_form.is_valid():
        user = parent_user_form.save()
        user.parent=True
        user.centre = request.user.centre
        user.save()
        return redirect(reverse('staffuser:add-parent-profile', kwargs={"parentuser_id":user.pk}))
    context = {
        'parent_user_form': parent_user_form
    }
    return render(request, "add-parent-user.html", context)