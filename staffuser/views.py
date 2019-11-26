from django.shortcuts import render
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required, user_passes_test


def staff_test(user):
    """Test to check if current user is solely a staff user"""
    return (user.is_staff and not user.is_admin)
    
def get_mondays_date():
    """Function to find the date of the most recent Monday"""
    todays_date=date.today()
    mondays_date=todays_date - timedelta(days=todays_date.weekday())
    return mondays_date

@login_required
@user_passes_test(staff_test, redirect_field_name=None, login_url='/oops/')
def staff_dashboard_view(request):
    """Renders dashboard for staff user"""
    mondays_date = get_mondays_date()
    todays_date = date.today()
    return render(request, "staff_dashboard.html", {'mondays_date': mondays_date, 'todays_date': todays_date})
    
