from django.shortcuts import render
from .forms import CentreForm, StaffUserForm

# Create your views here.

def admin_dashboard_view(request):
    """Renders dashboard for admin user"""
    return render(request, "admin-dashboard.html", {"page_title": "admin"})
    
def add_centre_view(request):
    centre_form = CentreForm(request.POST or None)
    if centre_form.is_valid():
        centre_form.save()
        centre_form = CentreForm()
    context = {
        'centre_form': centre_form
    }
    return render(request, "add-centre.html", context)
    
def add_staff_view(request):
    staff_user_form = StaffUserForm(request.POST or None)
    if staff_user_form.is_valid():
        staff_user_form.save()
        staff_user_form = StaffUserForm()
    context = {
        'staff_user_form': staff_user_form
    }
    return render(request, "add-staff-user.html", context)