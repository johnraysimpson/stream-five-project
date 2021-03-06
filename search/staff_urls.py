from django.urls import path
from .views import add_or_search_parent_view, search_student_view, add_or_search_tutor_view

urlpatterns = [
    path('parent/search/', add_or_search_parent_view, name="parents"),
    path('student/search/', search_student_view, name="students"),
    path('tutor/search/', add_or_search_tutor_view, name="tutors")
    ]