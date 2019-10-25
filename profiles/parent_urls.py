from django.urls import path
from .views import (
                    get_parentuser_profile,
                    get_parents_student_profile_view
                    )

urlpatterns = [
        path('my_profile/', get_parentuser_profile, name="parent_profile"),
        path('my_student/<student_id>', get_parents_student_profile_view, name="student_profile"),
    ]