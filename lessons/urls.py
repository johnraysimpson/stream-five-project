from django.urls import path, re_path
from .views import (
                    add_lesson_view,
                    update_lesson_view,
                    delete_lesson_confirm_view,
                    delete_lesson_view,
                    relate_via_student_view,
                    remove_student_from_lesson_confirm_view,
                    remove_student_from_lesson_view,
                    get_lessons_view,
                    get_lesson_details_view,
                    relate_via_lesson_view
                    )
                    
urlpatterns = [
    path('addlesson/', add_lesson_view, name='add-lesson'),
    path('addlessontostudent/<student_id>', relate_via_student_view, name='add-student-lesson'),
    re_path(r'^viewlessons/(?P<mondays_date>\d{4}-\d{2}-\d{2})/$', get_lessons_view, name='get-lessons'),
    path('viewlesson/<int:lesson_id>/', get_lesson_details_view, name='get-lesson-detail'),
    path('updatelesson/<int:lesson_id>/', update_lesson_view, name='update-lesson-detail'),
    path('deletelesson/<int:lesson_id>/', delete_lesson_confirm_view, name='delete-lesson-confirm'),
    path('lessondeleted/<int:lesson_id>/', delete_lesson_view, name='delete-lesson'),
    path('addstudenttolesson/<int:lesson_id>/', relate_via_lesson_view, name='add-student-to-lesson'),
    path('removestudent/<int:lesson_id>/<int:student_id>', remove_student_from_lesson_confirm_view, name='remove-student-from-lesson-confirm'),
    path('studentremoved/<int:lesson_id>/<int:student_id>', remove_student_from_lesson_view, name='remove-student-from-lesson')
    ]