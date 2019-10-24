from django.urls import path
from .views import (add_parent_profile_view,
                    add_tutor_profile_view,
                    add_student_view,
                    get_parent_profile_view,
                    update_parent_profile_view,
                    )

urlpatterns = [
    path('addparent/<parentuser_id>/', add_parent_profile_view, name="add-parent-profile"),
    path('addtutor/<tutoruser_id>/', add_tutor_profile_view, name="add-tutor-profile"),
    path('addstudent/', add_student_view, name='add-student'),
    path('parentprofile/<int:parent_id>', get_parent_profile_view, name='parent-profile'),
    path('parentprofile/update/<int:parent_id>', update_parent_profile_view, name='update-parent-profile'),
    ]