from django.shortcuts import render
from profiles.models import TutorProfile
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import date

def tutor_test(user):
    """Check to test if the current user is a tutor"""
    return user.is_tutor

# Create your views here.
@login_required
@user_passes_test(tutor_test, redirect_field_name=None, login_url='/oops/')
def tutor_dashboard_view(request):
    """View to render the dahsboard page for a tutor user"""
    tutor = TutorProfile.objects.get(user=request.user)
    todays_date = date.today()
    return render(request, 'tutor_dashboard.html', {'tutor': tutor, 'todays_date': todays_date})