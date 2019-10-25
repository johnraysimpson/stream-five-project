from django.urls import path
from .views import (
                    get_student_lessons_view,
                    )

urlpatterns = [
        path('view_lessons/', get_student_lessons_view, name="get_student_lessons")
    ]