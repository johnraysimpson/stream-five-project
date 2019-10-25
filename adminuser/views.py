from django.shortcuts import render
from .forms import CentreForm, StaffUserForm
from django.contrib.auth.decorators import login_required, user_passes_test

def admin_test(user):
    return user.is_admin

@login_required()
@user_passes_test(admin_test, redirect_field_name=None, login_url='/oops/')
def admin_dashboard_view(request):
    """Renders dashboard for admin user"""
    return render(request, "admin_dashboard.html")

@login_required()
@user_passes_test(admin_test, redirect_field_name=None, login_url='/oops/')
def add_centre_view(request):
    """Renders the page for adding a centre with its corresponding form"""
    centre_form = CentreForm(request.POST or None)
    if centre_form.is_valid():
        centre_form.save()
        centre_form = CentreForm()
    return render(request, "add_centre.html", {'centre_form': centre_form})
 
@login_required()
@user_passes_test(admin_test, redirect_field_name=None, login_url='/oops/')
def add_staff_view(request):
    """Renders add staff page with corresponding form"""
    staff_user_form = StaffUserForm(request.POST or None)
    if staff_user_form.is_valid():
        user = staff_user_form.save()
        user.staff=True
        user.save()
        staff_user_form = StaffUserForm()
    return render(request, "add_staff_user.html", {'staff_user_form': staff_user_form})