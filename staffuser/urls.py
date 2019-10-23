from django.urls import path, re_path, include
from .views import (staff_dashboard_view, 
                    add_parent_view,
                    add_tutor_view,
                    add_lesson_view,
                    add_student_lesson_view,
                    get_lessons_view,
                    get_lesson_details_view,
                    update_lesson_view,
                    delete_lesson_confirm_view,
                    delete_lesson_view,
                    remove_student_from_lesson_confirm_view,
                    remove_student_from_lesson_view
                    )
from profiles import urls as profile_urls

app_name = 'staffuser'
urlpatterns = [
    path('', staff_dashboard_view),
    path('', include(profile_urls)),
    path('dashboard/', staff_dashboard_view, name="dashboard"),
    path('addparent/', add_parent_view, name="add-parent"),
    path('addtutor/', add_tutor_view, name="add-tutor"),
    path('addlesson/', add_lesson_view, name='add-lesson'),
    path('addstudenttolesson/', add_student_lesson_view, name='add-student-lesson'),
    re_path(r'^viewlessons/(?P<mondays_date>\d{4}-\d{2}-\d{2})/$', get_lessons_view, name='get-lessons'),
    path('viewlesson/<int:lesson_id>/', get_lesson_details_view, name='get-lesson-detail'),
    path('updatelesson/<int:lesson_id>/', update_lesson_view, name='update-lesson-detail'),
    path('deletelesson/<int:lesson_id>/', delete_lesson_confirm_view, name='delete-lesson-confirm'),
    path('lessondeleted/<int:lesson_id>/', delete_lesson_view, name='delete-lesson'),
    path('removestudent/<int:lesson_id>/<int:student_id>', remove_student_from_lesson_confirm_view, name='remove-student-from-lesson-confirm'),
    path('studentremoved/<int:lesson_id>/<int:student_id>', remove_student_from_lesson_view, name='remove-student-from-lesson')
    ]