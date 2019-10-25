from django.urls import path
from .views import (add_parent_profile_view,
                    add_tutor_profile_view,
                    add_student_view,
                    get_parent_profile_view,
                    update_parent_profile_view,
                    get_student_profile_view,
                    update_student_view,
                    delete_student_view,
                    delete_student_confirm_view,
                    get_tutor_profile_view,
                    update_tutor_profile_view,
                    )

urlpatterns = [
    path('add_parent/<parentuser_id>/', add_parent_profile_view, name="add_parent_profile"),
    path('parent_profile/<int:parent_id>', get_parent_profile_view, name='parent_profile'),
    path('parent_profile/update/<int:parent_id>', update_parent_profile_view, name='update_parent_profile'),
    
    path('add_student/<parent_id>', add_student_view, name='add_student'),
    path('student_profile/<int:student_id>', get_student_profile_view, name='student_profile'),
    path('update_student/<student_id>', update_student_view, name='update_student'),
    path('delete_student/<student_id>', delete_student_view, name='delete_student'),
    path('delete_student_confirm/<student_id>', delete_student_confirm_view, name='delete_student_confirm'),
    
    path('add_tutor/<tutoruser_id>/', add_tutor_profile_view, name="add_tutor_profile"),
    path('tutor_profile/<tutor_id>/', get_tutor_profile_view, name="tutor_profile"),
    path('tutor_profile/update/<int:tutor_id>', update_tutor_profile_view, name='update_tutor_profile'),
    ]