from django.urls import path
from .views import admin_dashboard_view, add_centre_view, add_staff_view

app_name = 'adminuser'
urlpatterns = [
    path('', admin_dashboard_view),
    path('dashboard/', admin_dashboard_view, name="dashboard"),
    path('add_centre/', add_centre_view, name="add_centre"),
    path('add_staff_user/', add_staff_view, name="add_staff"),
    ]