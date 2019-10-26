from django.urls import path
from .views import (
                    get_student_lessons_view,
                    remove_student_from_lesson_confirm_view,
                    remove_student_from_lesson_view,
                    )

urlpatterns = [
        path('view_lessons/', get_student_lessons_view, name="get_student_lessons"),
        path('remove_student/<int:lesson_id>/<int:student_id>', remove_student_from_lesson_confirm_view, name='remove_student_from_lesson_confirm'),
        path('student_removed/<int:lesson_id>/<int:student_id>', remove_student_from_lesson_view, name='remove_student_from_lesson'),
    ]