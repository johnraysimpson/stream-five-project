from django.urls import path
from .views import (add_parent_profile_view,
                    add_tutor_profile_view,
                    add_student_view,
                    get_parent_profile_view,
                    update_parent_profile_view,
                    get_student_profile_view,
                    update_student_view,
                    delete_student_view,
                    delete_student_confirm_view
                    )

urlpatterns = [
    path('addparent/<parentuser_id>/', add_parent_profile_view, name="add-parent-profile"),
    path('parentprofile/<int:parent_id>', get_parent_profile_view, name='parent-profile'),
    path('parentprofile/update/<int:parent_id>', update_parent_profile_view, name='update-parent-profile'),
    
    path('addstudent/<parent_id>', add_student_view, name='add-student'),
    path('studentprofile/<int:student_id>', get_student_profile_view, name='student-profile'),
    path('updatestudent/<student_id>', update_student_view, name='update-student'),
    path('deletestudent/<student_id>', delete_student_view, name='delete-student'),
    path('deletestudent_confirm/<student_id>', delete_student_confirm_view, name='delete-student-confirm'),
    
    path('addtutor/<tutoruser_id>/', add_tutor_profile_view, name="add-tutor-profile"),
    ]