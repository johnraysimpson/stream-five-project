from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.core.mail import send_mail
from .forms import ParentUserForm, ParentProfileForm
from accounts.models import User


# Create your views here.
def staff_dashboard_view(request):
    """Renders dashboard for admin user"""
    return render(request, "staff-dashboard.html", {"page_title": "staff"})
    
def add_parent_profile_view(request, *args, **kwargs):
    
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
    """Renders dashboard for admin user"""
    parent_user_form = ParentUserForm(request.POST or None)
    if parent_user_form.is_valid():
        user = parent_user_form.save()
        user.parent=True
        user.centre = request.user.centre
        user.save()
        send_mail(
                "Welcome to Zephyr Tuition",
                "Hello parent user,\nYou have been registered to our website, your randomly generated password is\n"+user.password+"\nYou will be required to change your password when you first login with your email address.\nThank you for choosing us as a tutoring company.\nThe Zephyr Team",
                'johnraysimpson92@gmail.com',
                ['johnraysimpson92@gmail.com']
                )
        return redirect(reverse('staffuser:add-parent-profile', kwargs={"parentuser_id":user.pk}))
    context = {
        'parent_user_form': parent_user_form
    }
    return render(request, "add-parent-user.html", context)