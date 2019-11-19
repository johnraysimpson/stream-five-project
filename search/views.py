from django.shortcuts import render
from django.db.models import Q
from django.db.models import Value as V
from django.db.models.functions import Concat
from profiles.models import ParentProfile, Student, TutorProfile

# Create your views here.
def add_or_search_parent_view(request):
    """A view that renders page for adding a new parent user or searching for an existing one"""
    try:
        parents = ParentProfile.objects.annotate(full_name=Concat('first_name', V(' '), 'last_name')).filter(   Q(first_name__icontains=request.GET.get('q'))|
                                                                                                                Q(last_name__icontains=request.GET.get('q'))|
                                                                                                                Q(full_name__icontains=request.GET.get('q')),
                                                                                                                user__centre=request.user.centre
                                                                                                                ).order_by('last_name')
    except:
        parents = ParentProfile.objects.filter(user__centre=request.user.centre).order_by('last_name')
    print(request.GET.get('q'))
    return render(request, 'parents.html', {'parents': parents})
    
def search_student_view(request):
    """A view that renders page for searching for a student"""
    try:
        students = Student.objects.annotate(full_name=Concat('first_name', V(' '), 'last_name')).filter(Q(first_name__icontains=request.GET.get('q', ''))|
                                                                                                        Q(last_name__icontains=request.GET.get('q', ''))|
                                                                                                        Q(full_name__icontains=request.GET.get('q', '')),
                                                                                                        parent__user__centre=request.user.centre
                                                                                                        ).order_by('last_name')
    except:
        students = Student.objects.filter(parent__user__centre=request.user.centre).order_by('last_name')
    return render(request, 'students.html', {'students': students})
    
def add_or_search_tutor_view(request):
    """A view that renders page for adding a new tutor user or searching for an existing one"""
    try:
        tutors = TutorProfile.objects.annotate(full_name=Concat('first_name', V(' '), 'last_name')).filter( Q(first_name__icontains=request.GET.get('q', ''))|
                                                                                                            Q(last_name__icontains=request.GET.get('q', ''))|
                                                                                                            Q(full_name__icontains=request.GET.get('q', '')),
                                                                                                            user__centre=request.user.centre
                                                                                                            ).order_by('last_name')
    except:
        tutors = TutorProfile.objects.filter(user__centre=request.user.centre).order_by('last_name')
    return render(request, 'tutors.html', {'tutors': tutors})