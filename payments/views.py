from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime, date, timedelta
from .models import Payment
from .forms import MakePaymentForm
from lessons.models import Lesson
from profiles.models import TutorProfile, ParentProfile, Student
from parentuser.views import parent_test
from staffuser.views import staff_test
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET

def earnings_period(month):
    """Function to declare that the earning period is always between the 21 of two consecutive months"""
    today = datetime.today()
    year = today.year
    if month == 1:
        prev_month = 12
        return [(date(year-1, prev_month, 21)), (date(year, month, 21))]
    else:
        return [(date(year, month-1, 21)), (date(year, month, 21))]

# Create your views here.
@login_required
@user_passes_test(staff_test, redirect_field_name=None, login_url='/oops/')
def tutor_earnings_view(request, tutor_id, request_date):
    """View to render page to show the earnings of a tutor within a month"""
    tutor = get_object_or_404(TutorProfile, id=tutor_id)
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
    
@login_required
@user_passes_test(parent_test, redirect_field_name=None, login_url='/oops/')
def make_payment_view(request, parent_id, student_id, lesson_id):
    """View that renders a make payment page with form"""
    parent = get_object_or_404(ParentProfile, id=parent_id)
    student = get_object_or_404(Student, id=student_id)
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if request.user == parent.user and student.parent == parent and lesson in student.lessons.all():
        if request.method == 'POST':
            payment_form = MakePaymentForm(request.POST)
            if payment_form.is_valid():
                try:
                    customer = stripe.Charge.create(amount = int(student.price_per_lesson*100), currency = 'GBP', description = request.user.email, card = payment_form.cleaned_data['stripe_id'],)
                except stripe.error.CardError:
                    messages.error(request, "Your card was declined")
            
                if customer.paid:
                    Payment.objects.create(
                                            parent_id = parent_id,
                                            first_name = parent.first_name,
                                            last_name = parent.last_name,
                                            student_id = student_id,
                                            student_first_name = student.first_name,
                                            student_last_name = student.last_name,
                                            lesson_id = lesson_id,
                                            subject = lesson.subject,
                                            centre_name = lesson.centre.centre_name,
                                            date = lesson.date,
                                            amount_paid = student.price_per_lesson,
                                            date_paid = datetime.today()
                                            )
                    messages.error(request, "You have successfully paid")
                    return redirect(reverse('parentuser:get_payments'))
                else:
                    messages.error(request, "Unable to take payment")
            else:
                print(payment_form.errors)
                messages.error(request, "We were unable to take payment with that card")
        else:
            payment_form = MakePaymentForm()
        return render(request, 'make_payment.html', {'payment_form': payment_form, 'parent': parent, 'lesson': lesson, 'student': student, 'publishable': settings.STRIPE_PUBLISHABLE})
    else:
        return redirect('/oops/')
        
@login_required
@user_passes_test(parent_test, redirect_field_name=None, login_url='/oops/')
def get_payments_view(request):
    parent = get_object_or_404(ParentProfile, user=request.user)
    payments = Payment.objects.filter(parent_id=parent.id).order_by('-date_paid')
    return render(request, 'get_payments.html', {'payments': payments})