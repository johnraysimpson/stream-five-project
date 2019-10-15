from django.shortcuts import render
from .forms import CentreForm, StaffUserForm

# Create your views here.

def admin_dashboard_view(request):
    """Renders dashboard for admin user"""
    return render(request, "admin-dashboard.html")
    
def add_centre_view(request):
    """Renders the page for adding a centre with its corresponding form"""
    centre_form = CentreForm(request.POST or None)
    if centre_form.is_valid():
        centre_form.save()
        centre_form = CentreForm()
    return render(request, "add-centre.html", {'centre_form': centre_form})
    
def add_staff_view(request):
    """Renders add staff page with corresponding form"""
    staff_user_form = StaffUserForm(request.POST or None)
    if staff_user_form.is_valid():
        user = staff_user_form.save()
        user.staff=True
        user.save()
        staff_user_form = StaffUserForm()
    return render(request, "add-staff-user.html", {'staff_user_form': staff_user_form})