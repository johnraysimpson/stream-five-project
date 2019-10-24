from django.urls import path
from .views import add_parent_view, add_tutor_view, deactivate_user_view, deactivate_user_confirm_view, reactivate_user_confirm_view, delete_user_view, delete_user_confirm_view


urlpatterns = [
    path('add_parent/', add_parent_view, name="add-parent"),
    path('add_tutor/', add_tutor_view, name="add-tutor"),
    path('deactivate_user/<user_id>', deactivate_user_view, name='deactivate-user'),
    path('deactivate_user_confirm/<user_id>', deactivate_user_confirm_view, name='deactivate-user-confirm'),
    path('reactivate_user_confirm/<user_id>', reactivate_user_confirm_view, name='reactivate-user-confirm'),
    path('delete_user/<user_id>', delete_user_view, name='delete-user'),
    path('delete_user_confirm/<user_id>', delete_user_confirm_view, name='delete-user-confirm'),
    ]