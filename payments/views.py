from django.shortcuts import render
from datetime import datetime, date, timedelta
from lessons.models import Lesson
from profiles.models import TutorProfile

def earnings_period(month):
    today = datetime.today()
    year = today.year
    # month = 1
    # year = 2020
    if month == 1:
        prev_month = 12
        return [(date(year-1, prev_month, 21)), (date(year, month, 21))]
    else:
        return [(date(year, month-1, 21)), (date(year, month, 21))]
    


# Create your views here.
def payments_view(request):
    return render(request, 'payments.html')

def tutor_earnings_view(request, tutor_id, request_date):
    tutor = TutorProfile.objects.get(id=tutor_id)
    view_date = datetime.strptime(request_date, "%Y-%m-%d")
    view_month = view_date.month
    print(view_month)
    payment_month = earnings_period(view_month)
    if view_month == 12:
        next_month = date(view_date.year + 1, 1, 1)
    else:
        next_month = date(view_date.year, view_month + 1, 1)
    if view_month == 1:
        last_month = date(view_date.year - 1, 12, 28)
    else:
        last_month = date(view_date.year, view_month - 1, 28)
    current_month_name = view_date.strftime("%B")
    lessons = Lesson.objects.filter(date__gt=payment_month[0], date__lte=payment_month[1])
    earnings = 0
    for lesson in lessons:
        duration = lesson.duration
        total_minutes = duration.total_seconds()
        earned = round((total_minutes / 60) * float(tutor.pay_per_hour), 2)
        earnings += earned
    rounded_earnings = '{0:.2f}'.format(earnings)
    return render(request, 'tutor_earnings.html', {'tutor': tutor, "current_month_name": current_month_name, 'lessons': lessons, 'rounded_earnings': rounded_earnings, 'last_month': last_month, 'next_month': next_month})