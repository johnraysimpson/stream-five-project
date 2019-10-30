from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from staffuser.views import staff_test
from parentuser.views import parent_test
from tutoruser.views import tutor_test
from .forms import LessonOccurrenceForm, LessonForm, LessonToStudentForm, StudentToLessonForm
from datetime import datetime, date, timedelta
from .models import Lesson
from profiles.models import Student, ParentProfile, TutorProfile
from payments.models import Payment
from operator import attrgetter

def get_next_august():
    """Function that returns the date of the next time it is August"""
    today = datetime.today()
    year = today.year
    month = today.month
    if month >= 8:
        year += 1
    return date(year, 8, 1)


@login_required
@user_passes_test(staff_test, redirect_field_name=None, login_url='/oops/')
def add_lesson_view(request):
    """Renders add session page with corresponding form"""
    dates=[]
    if request.method == 'POST':
        lesson_form = LessonOccurrenceForm(request.POST)
        if lesson_form.is_valid():
            tutor = lesson_form.cleaned_data['tutor']
            earning = (lesson_form.cleaned_data['duration'].total_seconds() / 60) * float(tutor.pay_per_hour)
            if lesson_form.cleaned_data['occurrence'] == 'weekly':
                start_date = lesson_form.cleaned_data['date']
                try:
                    existing_lessons = Lesson.objects.filter(tutor=tutor,
                                                            subject=lesson_form.cleaned_data['subject'], 
                                                            day=lesson_form.cleaned_data['day'], 
                                                            time=lesson_form.cleaned_data['time'],
                                                            date__gte=start_date)
                    if existing_lessons:
                        for lesson in existing_lessons:
                            dates.append(lesson.date)
                        lesson_form.add_error(None, 'There is at least one date where this lesson exists, dates are listed below this form.')
                except:
                    while start_date < get_next_august():
                        Lesson.objects.create(tutor=tutor, 
                                                subject=lesson_form.cleaned_data['subject'], 
                                                day=lesson_form.cleaned_data['day'], 
                                                time=lesson_form.cleaned_data['time'], 
                                                date=start_date, 
                                                duration=lesson_form.cleaned_data['duration'],
                                                centre=request.user.centre,
                                                earning=earning
                                                )
                        start_date += timedelta(days=7)
                    messages.success(request, 'Lessons successfully created')
                    return redirect('staffuser:dashboard')
            else:
                try:
                    existing_lesson = Lesson.objects.get(tutor=tutor,
                                                            subject=lesson_form.cleaned_data['subject'], 
                                                            day=lesson_form.cleaned_data['day'], 
                                                            time=lesson_form.cleaned_data['time'],
                                                            date=lesson_form.cleaned_data['date'])
                    if existing_lesson:
                        lesson_form.add_error(None, 'This lesson already exists.')
                except:
                    lesson = lesson_form.save()
                    lesson.centre = request.user.centre
                    lesson.earning = earning
                    lesson.save()
                    messages.success(request, 'Lesson successfully created')
                    return redirect('staffuser:dashboard')
    else:
        lesson_form = LessonOccurrenceForm()
    return render(request, 'add_lesson.html', {'lesson_form': lesson_form, 'dates': dates})


@login_required
@user_passes_test(staff_test, redirect_field_name=None, login_url='/oops/')
def update_lesson_view(request, lesson_id):
    """View that renders an instance of the lesson form that has already been created for editing"""
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    if request.method == 'POST':
        update_lesson_form = LessonForm(request.POST, instance=lesson)
        if update_lesson_form.is_valid():
            update_lesson_form.save()
            return redirect('staffuser:get_lesson_detail', lesson_id=lesson_id)
    else:
        update_lesson_form = LessonForm(instance=lesson)
    return render(request, 'update_lesson_detail.html', {'update_lesson_form': update_lesson_form})
    
def delete_lesson_confirm_view(request, lesson_id):
    """View to render page confirming deletion particular lesson"""
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    return render(request, 'delete_lesson_confirm.html', {'lesson': lesson})
    
def delete_lesson_view(request, lesson_id):
    """View to delete particular lesson"""
    get_object_or_404(Lesson, pk=lesson_id).delete()
    messages.success(request, "Lesson deleted")
    return redirect('staffuser:dashboard')

  
@login_required
@user_passes_test(staff_test, redirect_field_name=None, login_url='/oops/')
def relate_via_student_view(request, student_id):
    """View to render page and more for creating relationship between lesson and student via the student"""
    student = get_object_or_404(Student, pk=student_id)
    if request.method == "POST":
        lesson_form = LessonToStudentForm(request.POST)
        if lesson_form.is_valid():
            
                start_date = lesson_form.cleaned_data['date']
                matched_lessons = []
                
                while start_date < get_next_august():
                    
                    try: 
                        matched_lesson = Lesson.objects.get(tutor = lesson_form.cleaned_data['tutor'],
                                                                day = lesson_form.cleaned_data['day'],
                                                                time = lesson_form.cleaned_data['time'],
                                                                subject = lesson_form.cleaned_data['subject'],
                                                                date = start_date,
                                                                )
                    except Lesson.DoesNotExist:
                        matched_lesson = None
                        
                    if matched_lesson:
                        matched_lessons.append(matched_lesson)
                        
                    if lesson_form.cleaned_data['occurrence'] == 'one_off':
                        break
                    
                    elif lesson_form.cleaned_data['occurrence'] == 'weekly':
                        start_date += timedelta(days=7)
                        
                    else:
                        start_date += timedelta(days=14)
                print(matched_lessons) 
                if not matched_lessons:
                    lesson_form.add_error(None, 'lesson(s) do not exist')
                else:
                    for lesson in matched_lessons:
                        student.lessons.add(lesson)
                    messages.success(request, 'Student successfully added to lesson')
                    return redirect('staffuser:dashboard')
    else:
        lesson_form = LessonToStudentForm()
    return render(request, 'add_student_lesson.html', {'lesson_form': lesson_form, 'student': student})

@login_required
@user_passes_test(staff_test, redirect_field_name=None, login_url='/oops/')
def relate_via_lesson_view(request, lesson_id):
    """View to render page and more for creating relationship between lesson and student via the lesson"""
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    if request.method == "POST":
        student_lesson_form = StudentToLessonForm(request.POST, request=request)
        if student_lesson_form.is_valid():
            
                start_date = lesson.date
                matched_lessons = []
                
                while start_date < get_next_august():
                    
                    try:
                        matched_lesson = Lesson.objects.get(tutor = lesson.tutor,
                                                                day = lesson.day,
                                                                time = lesson.time,
                                                                subject = lesson.subject,
                                                                date = start_date,
                                                                )
                    except Lesson.DoesNotExist:
                        matched_lesson = None
                        
                    if matched_lesson:
                        matched_lessons.append(matched_lesson)
                        
                    if student_lesson_form.cleaned_data['occurrence'] == 'one_off':
                        break
                    
                    elif student_lesson_form.cleaned_data['occurrence'] == 'weekly':
                        start_date += timedelta(days=7)
                        
                    else:
                        start_date += timedelta(days=14)
                
                student = student_lesson_form.cleaned_data['student']
                for lesson in matched_lessons:
                    student.lessons.add(lesson)
                return redirect('staffuser:get_lesson_detail', lesson_id=lesson_id)
    else:
        student_lesson_form = StudentToLessonForm(request=request)
    return render(request, 'add_student_to_lesson.html', {'lesson': lesson, 'student_lesson_form': student_lesson_form})

@login_required
@user_passes_test(staff_test, redirect_field_name=None, login_url='/oops/')
def remove_student_from_lesson_confirm_view(request, lesson_id, student_id):
    """View to render a confirmation page for removing the relationship between a lesson and a student"""
    student = get_object_or_404(Student, pk=student_id)
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    return render(request, 'remove_student_from_lesson_confirm.html', {'student': student, 'lesson': lesson})
    
@login_required
@user_passes_test(staff_test, redirect_field_name=None, login_url='/oops/')
def remove_student_from_lesson_view(request, lesson_id, student_id):
    """View that removes the relationship between a lesson and a student"""
    student = get_object_or_404(Student, pk=student_id)
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    student.lessons.remove(lesson)
    return redirect('staffuser:get_lesson_detail', lesson_id=lesson_id)

   
@login_required
@user_passes_test(staff_test, redirect_field_name=None, login_url='/oops/')
def get_lessons_view(request, mondays_date):
    """View to retrieve sessions on a weekly basis"""
    try:
        view_date = datetime.strptime(mondays_date, "%Y-%m-%d")
        if view_date.weekday() == 0:
            sundays_date = view_date + timedelta(days=6)
            this_weeks_lessons = Lesson.objects.filter(date__gte=mondays_date,
                                                                date__lt=sundays_date)
            days_of_the_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
            next_week = (view_date + timedelta(days=7)).date
            previous_week = (view_date - timedelta(days=7)).date
            return render(request, 'get_lessons.html', {'lessons': this_weeks_lessons, 
                                                        'days_of_the_week': days_of_the_week, 
                                                        'view_date': view_date, 
                                                        'next_week': next_week, 
                                                        'previous_week': previous_week}
                                                        )
        else:
            return render(request, 'get_lessons.html', {"wrong_view_date": True})
    except:
        return render(request, 'get_lessons.html', {"wrong_view_date": True})

@login_required
@user_passes_test(staff_test, redirect_field_name=None, login_url='/oops/')    
def get_lesson_details_view(request, lesson_id):
    """View for retrieving a lesson and displaying details"""
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    return render(request, 'get_lesson_detail.html', {'lesson': lesson})
    
@login_required
@user_passes_test(parent_test, redirect_field_name=None, login_url='/oops/')
def get_student_lessons_view(request):
    """View for retrieving lessons that a parent's students are attending"""
    todays_date = date.today()
    parent = ParentProfile.objects.get(user=request.user)
    students = Student.objects.filter(parent=parent)
    payments = Payment.objects.filter(parent_id=parent.id)
    prev_payments = Payment.objects.filter(parent_id=parent.id, date__lt=todays_date)
    
    queryset = Lesson.objects.none()
    for student in students:
        lessons = student.lessons.filter(student=student, date__gte=todays_date)
        queryset |= lessons
    future_lessons = queryset.distinct().order_by('date')
    
    queryset = Lesson.objects.none()
    for student in students:
        lessons = student.lessons.filter(student=student, date__lt=todays_date)
        queryset |= lessons
    past_lessons = queryset.distinct().order_by('date')
    
    unpaid_lessons = []
    for student in students:
        for lesson in past_lessons:
            if student in lesson.student_set.all():
                unpaid_lessons.append((student, lesson))
                
    for student in students:
        for payment in prev_payments:
            for lesson in past_lessons:
                if payment.lesson_id == lesson.id and payment.student_id == student.id:
                    unpaid_lessons.remove((student, lesson))
    
    return render(request, 'get_student_lessons.html', {'payments': payments, 'future_lessons': future_lessons, 'students': students, 'unpaid_lessons': unpaid_lessons})
    
@login_required
@user_passes_test(parent_test, redirect_field_name=None, login_url='/oops/')
def parent_remove_student_from_lesson_confirm_view(request, lesson_id, student_id):
    """View to render a confirmation page for removing the relationship between a lesson and a student"""
    student = get_object_or_404(Student, pk=student_id)
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    if request.user.is_parent:
        parent = ParentProfile.objects.get(user=request.user)
        if student.parent != parent:
            return redirect('/oops/')
        else:
            return render(request, 'remove_student_from_lesson_confirm.html', {'student': student, 'lesson': lesson})
            
@login_required
@user_passes_test(parent_test, redirect_field_name=None, login_url='/oops/')
def parent_remove_student_from_lesson_view(request, lesson_id, student_id):
    """View that removes the relationship between a lesson and a student"""
    student = get_object_or_404(Student, pk=student_id)
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    if request.user.is_parent:
        parent = ParentProfile.objects.get(user=request.user)
        if student.parent != parent:
            return redirect('/oops/')
        else:
            student.lessons.remove(lesson)
            return redirect('parentuser:get_student_lessons')
            
            
@login_required
@user_passes_test(tutor_test, redirect_field_name=None, login_url='/oops/')
def get_tutor_lessons_view(request):
    """View that renders page displaying a tutor's upcoming lessons"""
    tutor = TutorProfile.objects.get(user=request.user)
    lessons = Lesson.objects.filter(tutor=tutor)
    print(lessons)
    return render(request, 'get_tutor_lessons.html', {'tutor': tutor, 'lessons': lessons})