from django.urls import path, re_path
from .views import (add_parent_profile_view,
                    add_tutor_profile_view,
                    add_student_view,
                    )

urlpatterns = [
    path('addparent/<parentuser_id>/', add_parent_profile_view, name="add-parent-profile"),
    path('addtutor/<tutoruser_id>/', add_tutor_profile_view, name="add-tutor-profile"),
    path('addstudent/', add_student_view, name='add-student'),
    ]