from django.shortcuts import render, redirect
from datetime import datetime, date, timedelta
from accounts.forms import CreateUserForm
from accounts.models import User
from django.contrib.auth.decorators import login_required, user_passes_test


def staff_test(user):
    """Test to check if current user is solely a staff user"""
    return (user.is_staff and not user.is_admin)
    
def get_mondays_date():
    todays_date=date.today()
    mondays_date=todays_date - timedelta(days=todays_date.weekday())
    return mondays_date

#keep
@login_required
@user_passes_test(staff_test, redirect_field_name=None, login_url='/oops/')
def staff_dashboard_view(request):
    """Renders dashboard for staff user"""
    mondays_date = get_mondays_date()
    return render(request, "staff_dashboard.html", {'mondays_date': mondays_date})
    
