from django.urls import path, re_path
from .views import (staff_dashboard_view, 
                    add_parent_view, 
                    add_parent_profile_view, 
                    add_tutor_view,
                    add_tutor_profile_view,
                    add_tutor_session_view,
                    add_student_view,
                    add_student_session_view,
                    get_lessons_view,
                    get_lesson_details_view,
                    update_tutor_session_view,
                    delete_tutor_session_confirm_view,
                    delete_tutor_session_view,
                    remove_student_from_session_confirm_view,
                    remove_student_from_session_view
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
    path('viewlesson/<int:lesson_id>/', get_lesson_details_view, name='get-lesson-detail'),
    path('updatelesson/<int:lesson_id>/', update_tutor_session_view, name='update-lesson-detail'),
    path('deletelesson/<int:lesson_id>/', delete_tutor_session_confirm_view, name='delete-lesson-confirm'),
    path('lessondeleted/<int:lesson_id>/', delete_tutor_session_view, name='delete-lesson'),
    path('removestudent/<int:lesson_id>/<int:student_id>', remove_student_from_session_confirm_view, name='remove-student-from-session-confirm'),
    path('studentremoved/<int:lesson_id>/<int:student_id>', remove_student_from_session_view, name='remove-student-from-session')
    ]