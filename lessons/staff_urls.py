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
    path('add_lesson/', add_lesson_view, name='add_lesson'),
    path('add_lesson_to_student/<student_id>', relate_via_student_view, name='add_student_lesson'),
    re_path(r'^viewlessons/(?P<mondays_date>\d{4}-\d{2}-\d{2})/$', get_lessons_view, name='get_lessons'),
    path('view_lesson/<int:lesson_id>/', get_lesson_details_view, name='get_lesson_detail'),
    path('update_lesson/<int:lesson_id>/', update_lesson_view, name='update_lesson_detail'),
    path('delete_lesson/<int:lesson_id>/', delete_lesson_confirm_view, name='delete_lesson_confirm'),
    path('lesson_deleted/<int:lesson_id>/', delete_lesson_view, name='delete_lesson'),
    path('add_student_to_lesson/<int:lesson_id>/', relate_via_lesson_view, name='add_student_to_lesson'),
    path('remove_student/<int:lesson_id>/<int:student_id>', remove_student_from_lesson_confirm_view, name='remove_student_from_lesson_confirm'),
    path('student_removed/<int:lesson_id>/<int:student_id>', remove_student_from_lesson_view, name='remove_student_from_lesson')
    ]