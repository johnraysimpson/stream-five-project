from django.urls import path
from .views import (
                    get_tutoruser_profile,
                    get_student_profile_as_tutor
                    )

urlpatterns = [
        path('my_profile/', get_tutoruser_profile, name="tutor_profile"),
        path('student_profile/<student_id>', get_student_profile_as_tutor, name="student_profile"),
    ]