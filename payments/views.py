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
from tutoruser.views import tutor_test
from adminuser.views import admin_test
from django.conf import settings
import stripe
from django.core.paginator import Paginator

stripe.api_key = settings.STRIPE_SECRET

def earnings_period(view_date):
    """Function to declare that the earning period is always between the 21 of two consecutive months"""
    year = view_date.year
    month = view_date.month
    if month == 1:
        prev_month = 12
        return [(date(year-1, prev_month, 21)), (date(year, month, 21))]
    else:
        return [(date(year, month-1, 21)), (date(year, month, 21))]
        
        
def intake_period(view_date):
    year = view_date.year
    month = view_date.month
    if month == 12:
        next_month = 1
        return [(date(year, month, 1)), (date(year+1, next_month, 1))]
    else:
        return [(date(year, month, 1)), (date(year, month+1, 1))]
        
def get_next_month(request_date, month):
    if month == 12:
        next_month = date(request_date.year + 1, 1, 1)
    else:
        next_month = date(request_date.year, month + 1, 1)
    return next_month
    
def get_last_month(request_date, month):
    if month == 1:
        last_month = date(request_date.year - 1, 12, 28)
    else:
        last_month = date(request_date.year, month - 1, 28)
    return last_month
        
def get_earnings(request_date, tutor):
    view_date = datetime.strptime(request_date, "%Y-%m-%d")
    view_month = view_date.month
    print(view_month)
    payment_month = earnings_period(view_date)
    next_month = get_next_month(view_date, view_month)
    last_month = get_last_month(view_date, view_month)
    current_month_name = view_date.strftime("%B")
    current_year = view_date.strftime("%Y")
    lessons = Lesson.objects.filter(tutor=tutor, date__gt=payment_month[0], date__lte=payment_month[1]).order_by('date')
    earnings = 0
    for lesson in lessons:
        duration = lesson.duration
        total_minutes = duration.total_seconds()
        earned = round((total_minutes / 60) * float(tutor.pay_per_hour), 2)
        earnings += earned
    rounded_earnings = '{0:.2f}'.format(earnings)
    print(payment_month)
    return {'tutor': tutor, "current_month_name": current_month_name, 'current_year': current_year, 'lessons': lessons, 'rounded_earnings': rounded_earnings, 'last_month': last_month, 'next_month': next_month}


def get_intake(payments):
    intake = 0
    for payment in payments:
        paid_amount = float(payment.amount_paid)
        intake += paid_amount
        print(intake)
    rounded_intake = '{0:.2f}'.format(intake)
    return rounded_intake

@login_required
@user_passes_test(staff_test, redirect_field_name=None, login_url='/oops/')
def intake_view(request, request_date):
    view_date = datetime.strptime(request_date, "%Y-%m-%d")
    view_month = view_date.month
    print(view_month)
    intake_month = intake_period(view_date)
    next_month = get_next_month(view_date, view_month)
    last_month = get_last_month(view_date, view_month)
    current_month_name = view_date.strftime("%B")
    payments = Payment.objects.filter(date_paid__gte=intake_month[0], date_paid__lt=intake_month[1], centre_name=request.user.centre.centre_name)
    rounded_intake = get_intake(payments)
    return render(request, 'get_intake.html', {"current_month_name": current_month_name, 'payments': payments, 'rounded_intake': rounded_intake, 'last_month': last_month, 'next_month': next_month})
    
@login_required
@user_passes_test(admin_test, redirect_field_name=None, login_url='/oops/')
def whole_intake_view(request, request_date):
    view_date = datetime.strptime(request_date, "%Y-%m-%d")
    view_month = view_date.month
    print(view_month)
    intake_month = intake_period(view_month)
    next_month = get_next_month(view_date, view_month)
    last_month = get_last_month(view_date, view_month)
    current_month_name = view_date.strftime("%B")
    payments = Payment.objects.filter(date_paid__gte=intake_month[0], date_paid__lt=intake_month[1])
    rounded_intake = get_intake(payments)
    return render(request, 'get_intake.html', {"current_month_name": current_month_name, 'payments': payments, 'rounded_intake': rounded_intake, 'last_month': last_month, 'next_month': next_month})
    
@login_required
@user_passes_test(staff_test, redirect_field_name=None, login_url='/oops/')
def tutor_earnings_view(request, tutor_id, request_date):
    """View to render page to show the earnings of a tutor within a month"""
    tutor = get_object_or_404(TutorProfile, id=tutor_id)
    context = get_earnings(request_date, tutor)
    return render(request, 'tutor_earnings.html', context)
    
@login_required
@user_passes_test(tutor_test, redirect_field_name=None, login_url='/oops/')
def tutoruser_earnings_view(request, request_date):
    """View to render page to show the earnings of a tutor within a month"""
    tutor = get_object_or_404(TutorProfile, user=request.user)
    context = get_earnings(request_date, tutor)
    return render(request, 'tutor_earnings.html', context)
    
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
                        messages.error(request, "Payment successful")
                        return redirect(reverse('parentuser:get_student_lessons'))
                    else:
                        messages.error(request, "Unable to take payment")
                except stripe.error.CardError:
                    messages.error(request, "Your card was declined")
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
    payments_list = Payment.objects.filter(parent_id=parent.id).order_by('-date_paid')
    paginator = Paginator(payments_list, 20)
    page = request.GET.get('page')
    payments = paginator.get_page(page)
    return render(request, 'get_payments.html', {'payments': payments})