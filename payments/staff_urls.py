from django.urls import path, re_path
from .views import (tutor_earnings_view,
                    intake_view
                    )

urlpatterns = [
    re_path(r'^tutor_earnings/(?P<tutor_id>\d+)/(?P<request_date>\d{4}-\d{2}-\d{2})$', tutor_earnings_view, name='tutor_earnings'),
    re_path(r'^intake/(?P<request_date>\d{4}-\d{2}-\d{2})$', intake_view, name='get_intake'),
    ]