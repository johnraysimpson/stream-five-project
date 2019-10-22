from django.urls import path, re_path
from .views import (staff_dashboard_view, 
                    add_parent_view, 
                    add_parent_profile_view, 
                    add_tutor_view,
                    add_tutor_profile_view,
                    add_tutor_session_view,
                    add_student_view,
                    add_student_session_view,
                    get_lessons_view
                    )

app_name = 'staffuser'
urlpatterns = [
    path('', staff_dashboard_view),
    path('dashboard/', staff_dashboard_view, name="dashboard"),
    path('addparent/', add_parent_view, name="add-parent"),
    path('addparent/<parentuser_id>/', add_parent_profile_view, name="add-parent-profile"),
    path('addtutor/', add_tutor_view, name="add-tutor"),
    path('addtutor/<tutoruser_id>/', add_tutor_profile_view, name="add-tutor-profile"),
    path('addtutorsession/', add_tutor_session_view, name='add-session'),
    path('addstudent/', add_student_view, name='add-student'),
    path('addstudentsession/', add_student_session_view, name='add-student-session'),
    re_path(r'^viewsessions/(?P<mondays_date>\d{4}-\d{2}-\d{2})/$', get_lessons_view, name='get-lessons'),
    ]