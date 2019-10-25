from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from staffuser.views import staff_test
from .forms import LessonOccurrenceForm, LessonForm, LessonToStudentForm, StudentToLessonForm
from datetime import datetime, date, timedelta
from .models import Lesson
from profiles.models import Student


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
    lesson_form = LessonOccurrenceForm(request.POST or None)
    if lesson_form.is_valid():
        tutor = lesson_form.cleaned_data['tutor']
        earning = (lesson_form.cleaned_data['duration'].total_seconds() / 60) * float(tutor.pay_per_hour)
        if lesson_form.cleaned_data['occurrence'] == 'weekly':
            start_date = lesson_form.cleaned_data['date']
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
        else:
            lesson = lesson_form.save()
            lesson.centre = request.user.centre
            lesson.earning = earning
            lesson.save()
        lesson_form = LessonOccurrenceForm()
    return render(request, 'add_lesson.html', {'lesson_form': lesson_form})



def update_lesson_view(request, lesson_id):
    """"""
    lesson = Lesson.objects.get(pk=lesson_id)
    if request.method == 'POST':
        update_lesson_form = LessonForm(request.POST, instance=lesson)
        if update_lesson_form.is_valid():
            update_lesson_form.save()
            return redirect('staffuser:get_lesson_detail', lesson_id=lesson_id)
    else:
        update_lesson_form = LessonForm(instance=lesson)
    return render(request, 'update_lesson_detail.html', {'update_lesson_form': update_lesson_form})
    
def delete_lesson_confirm_view(request, lesson_id):
    """"""
    lesson = Lesson.objects.get(pk=lesson_id)
    return render(request, 'delete_lesson_confirm.html', {'lesson': lesson})
    
def delete_lesson_view(request, lesson_id):
    Lesson.objects.get(pk=lesson_id).delete()
    messages.success(request, "Lesson deleted")
    return redirect('staffuser:dashboard')

  
@login_required
@user_passes_test(staff_test, redirect_field_name=None, login_url='/oops/')
def relate_via_student_view(request, student_id):
    student = Student.objects.get(pk=student_id)
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
                    lesson_form = LessonToStudentForm()
    else:
        lesson_form = LessonToStudentForm()
    return render(request, 'add_student_lesson.html', {'lesson_form': lesson_form, 'student': student})

def relate_via_lesson_view(request, lesson_id):
    lesson = Lesson.objects.get(pk=lesson_id)
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
                student_lesson_form = StudentToLessonForm(request=request)
    else:
        student_lesson_form = StudentToLessonForm(request=request)
    return render(request, 'add_student_to_lesson.html', {'lesson': lesson, 'student_lesson_form': student_lesson_form})

def remove_student_from_lesson_confirm_view(request, lesson_id, student_id):
    student = Student.objects.get(pk=student_id)
    lesson = Lesson.objects.get(pk=lesson_id)
    return render(request, 'remove_student_from_lesson_confirm.html', {'student': student, 'lesson': lesson})
    

def remove_student_from_lesson_view(request, lesson_id, student_id):
    student = Student.objects.get(pk=student_id)
    lesson = Lesson.objects.get(pk=lesson_id)
    student.sessions.remove(lesson)
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
        
def get_lesson_details_view(request, lesson_id):
    """View for retrieving a lesson and displaying details"""
    lesson = Lesson.objects.get(pk=lesson_id)
    return render(request, 'get_lesson_detail.html', {'lesson': lesson})