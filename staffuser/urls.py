from django.urls import path
from .views import staff_dashboard_view, add_parent_view, add_parent_profile_view

app_name = 'staffuser'
urlpatterns = [
    path('', staff_dashboard_view),
    path('dashboard/', staff_dashboard_view, name="dashboard"),
    path('addparent/', add_parent_view, name="add-parent"),
    path('addparent/<parentuser_id>', add_parent_profile_view, name="add-parent-profile"),
    ]