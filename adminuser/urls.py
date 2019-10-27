from django.urls import path, re_path
from .views import admin_dashboard_view, add_centre_view, add_staff_view
from payments.views import whole_intake_view

app_name = 'adminuser'
urlpatterns = [
    path('', admin_dashboard_view),
    path('dashboard/', admin_dashboard_view, name="dashboard"),
    path('add_centre/', add_centre_view, name="add_centre"),
    path('add_staff_user/', add_staff_view, name="add_staff"),
    re_path(r'^intake/(?P<request_date>\d{4}-\d{2}-\d{2})$', whole_intake_view, name='get_intake'),
    ]