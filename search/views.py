from django.shortcuts import render
from django.db.models import Q
from django.db.models import Value as V
from django.db.models.functions import Concat
from profiles.models import ParentProfile, Student, TutorProfile

# Create your views here.
def add_or_search_parent_view(request):
    parents = ParentProfile.objects.annotate(full_name=Concat('first_name', V(' '), 'last_name')).filter(Q(first_name__icontains=request.GET.get('q', ''))|
                                                                                                            Q(last_name__icontains=request.GET.get('q', ''))|
                                                                                                            Q(full_name__icontains=request.GET.get('q', ''))|
                                                                                                            Q(user__centre=request.user.centre))
    return render(request, 'parents.html', {'parents': parents})
    
def search_student_view(request):
    students = Student.objects.annotate(full_name=Concat('first_name', V(' '), 'last_name')).filter(Q(first_name__icontains=request.GET.get('q', ''))|
                                                                                                    Q(last_name__icontains=request.GET.get('q', ''))|
                                                                                                    Q(full_name__icontains=request.GET.get('q', ''))|
                                                                                                    Q(parent__user__centre=request.user.centre))
    return render(request, 'students.html', {'students': students})
    
def search_tutor_view(request):
    tutors = TutorProfile.objects.annotate(full_name=Concat('first_name', V(' '), 'last_name')).filter(Q(first_name__icontains=request.GET.get('q', ''))|
                                                                                                    Q(last_name__icontains=request.GET.get('q', ''))|
                                                                                                    Q(full_name__icontains=request.GET.get('q', ''))|
                                                                                                    Q(user__centre=request.user.centre))
    return render(request, 'tutors.html', {'tutors': tutors})